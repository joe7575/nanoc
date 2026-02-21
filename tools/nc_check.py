#!/usr/bin/env python3
"""
NanoC Syntax Checker
====================
Checks NanoC (.nc) scripts for syntax errors before uploading to embedded hardware.
This mirrors the parser logic of the NanoC C compiler (nc_compiler.c).

Usage: python nc_check.py <script.nc> [-v]
  -v  Verbose mode: show parsed structure

Copyright (C) 2024-2026 Joachim Stolberg
MIT License
"""

import sys
import re
import os

# ============================================================================
# Token types (matching nc_int.h)
# ============================================================================
NC_INT32 = 128; DIM = 129; FOR = 130; TO = 131
STEP = 132; NEXT = 133; IF = 134; THEN = 135
PRINT = 136; GOTO = 137; GOSUB = 138; RETURN = 139
END = 140; REM = 141; AND = 142; OR = 143
NOT = 144; MOD = 145; NUM = 146; STR = 147
ID = 148; STRID = 149; EQ = 150; NQ = 151
LE = 152; LQ = 153; GR = 154; GQ = 155
XFUNC = 156; ARR = 157; BREAK = 158; LABEL = 159
SET1 = 160; SET2 = 161; SET4 = 162; GET1 = 163
GET2 = 164; GET4 = 165; LEFTS = 166; RIGHTS = 167
MIDS = 168; LEN = 169; VAL = 170; STRS = 171
SPC = 172; PARAM = 173; COPY = 174; NC_CONST = 175
ERASE = 176; ELSE = 177; HEXS = 178; NIL = 179
INSTR = 180; ON = 181; TRON = 182; TROFF = 183
FREE = 184; RND = 185; PARAMS = 186; STRINGS = 187
WHILE = 188; LOOP = 189; ENDIF = 190; DATA = 191
READ = 192; RESTORE = 193; REF = 194; RETI = 195
ELSEIF = 196; SEMICOLON = 197
LBRACE = 198; RBRACE = 199
PRINTF = 200; STR8 = 201
LBRACKET = 202; RBRACKET = 203
NC_UINT32 = 204; NC_VOID = 205
U8 = 206; U16 = 207; U32 = 208
INC = 209; DEC = 210
LOCAL = 211; FUNC = 212; RET = 213
DISPATCH = 214
SHL = 215; SHR = 216
e_CNST = 250  # Internal: compile-time constant

# Special single-char tokens returned as ord(char)
TOK_EOF = 0

# ============================================================================
# Keywords
# ============================================================================
KEYWORDS = {
    "int32": NC_INT32, "str8": STR8, "func": FUNC, "return": RET,
    "for": FOR, "to": TO, "step": STEP,
    "if": IF, "else": ELSE, "end": END,
    "while": WHILE, "and": AND, "or": OR, "not": NOT, "mod": MOD,
    "break": BREAK, "reti": RETI,
    "copy": COPY, "u8": U8, "u16": U16, "u32": U32,
    "left$": LEFTS, "right$": RIGHTS, "mid$": MIDS,
    "len": LEN, "str$": STRS, "hex$": HEXS,
    "NULL": NIL, "string$": STRINGS,
    "const": NC_CONST, "instr": INSTR, "free": FREE, "rnd": RND,
    "printf": PRINTF, "dispatch": DISPATCH,
    "val": VAL, "param": PARAM, "params": PARAMS,
}

# Known external functions (from test/main.c) — user can extend this list
EXTERNAL_FUNCTIONS = {
    "setcur": (2, ["num", "num"]),
    "clrscr": (0, []),
    "clrline": (1, ["num"]),
    "time": (0, []),
    "sleep": (1, ["num"]),
    "input": (1, ["str"]),
    "input$": (1, ["str"]),
    "cmd": (3, ["num", "any", "any"]),
    "sgn": (1, ["num"]),
    "kvs_create": (2, ["num", "num"]),
    "kvs_set": (3, ["num", "num", "num"]),
    "kvs_get": (2, ["num", "num"]),
    "fire_on_can": (4, ["num", "num", "num", "ref"]),
}


class NcError(Exception):
    pass


# ============================================================================
# Scanner — tokenizes one line at a time (like nc_scanner.c)
# ============================================================================
class Token:
    __slots__ = ("type", "value", "text")

    def __init__(self, type, value=None, text=""):
        self.type = type
        self.value = value
        self.text = text

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, {self.text!r})"


def is_alpha(c):
    return c.isalpha() or c == '_'


def is_alnum(c):
    return c.isalnum() or c == '_'


def tokenize_line(line):
    """Tokenize a single line, yields Token objects."""
    i = 0
    n = len(line)

    while i < n:
        c = line[i]

        # Skip whitespace
        if c in (' ', '\t', '\r', '\n'):
            i += 1
            continue

        # Comments: // or '
        if c == '/' and i + 1 < n and line[i + 1] == '/':
            return
        if c == '\'':
            return

        # Semicolon
        if c == ';':
            yield Token(SEMICOLON, None, ";")
            i += 1
            continue

        # String literal
        if c == '"':
            j = i + 1
            while j < n and line[j] != '"':
                j += 1
            if j >= n:
                yield Token(STR, line[i + 1:], line[i:])  # unterminated
            else:
                yield Token(STR, line[i + 1:j], line[i:j + 1])
                j += 1
            i = j
            continue

        # Number
        if c.isdigit():
            j = i
            while j < n and line[j].isdigit():
                j += 1
            text = line[i:j]
            yield Token(NUM, int(text), text)
            i = j
            continue

        # Identifier / keyword
        if is_alpha(c):
            j = i
            while j < n and is_alnum(line[j]):
                j += 1
            # Check for $ suffix (string var/func)
            if j < n and line[j] == '$':
                j += 1
            text = line[i:j]
            # Check keywords
            if text in KEYWORDS:
                yield Token(KEYWORDS[text], None, text)
            elif text.endswith('$'):
                yield Token(STRID, text, text)
            else:
                yield Token(ID, text, text)
            i = j
            continue

        # Two-character operators
        if i + 1 < n:
            two = line[i:i + 2]
            if two == '==':
                yield Token(EQ, None, "=="); i += 2; continue
            if two == '!=':
                yield Token(NQ, None, "!="); i += 2; continue
            if two == '<=':
                yield Token(LQ, None, "<="); i += 2; continue
            if two == '>=':
                yield Token(GQ, None, ">="); i += 2; continue
            if two == '<>':
                yield Token(NQ, None, "<>"); i += 2; continue
            if two == '&&':
                yield Token(AND, None, "&&"); i += 2; continue
            if two == '||':
                yield Token(OR, None, "||"); i += 2; continue
            if two == '++':
                yield Token(INC, None, "++"); i += 2; continue
            if two == '--':
                yield Token(DEC, None, "--"); i += 2; continue
            if two == '<<':
                yield Token(SHL, None, "<<"); i += 2; continue
            if two == '>>':
                yield Token(SHR, None, ">>"); i += 2; continue

        # Single-character operators and punctuation
        if c == '<':
            yield Token(LE, None, "<"); i += 1; continue
        if c == '>':
            yield Token(GR, None, ">"); i += 1; continue
        if c == '=':
            yield Token(EQ, None, "="); i += 1; continue
        if c == '!':
            yield Token(NOT, None, "!"); i += 1; continue

        # Braces / brackets
        if c == '{':
            yield Token(LBRACE, None, "{"); i += 1; continue
        if c == '}':
            yield Token(RBRACE, None, "}"); i += 1; continue
        if c == '[':
            yield Token(LBRACKET, None, "["); i += 1; continue
        if c == ']':
            yield Token(RBRACKET, None, "]"); i += 1; continue

        # Everything else as single-char token
        yield Token(ord(c), c, c)
        i += 1


# ============================================================================
# Parser — recursive descent, checking structure without generating code
# ============================================================================
class NcChecker:
    def __init__(self, filename, verbose=False):
        self.filename = filename
        self.verbose = verbose
        self.errors = []
        self.warnings = []
        self.linenum = 0
        self.tokens = []
        self.pos = 0
        self.lines = []

        # Symbol table
        self.symbols = {}  # name -> {"type": ..., "is_local": bool, "is_array": bool, "param_count": int or None}
        self.functions = {}  # func_name -> param_count
        self.constants = {}  # const_name -> value

        # Context
        self.in_func = False
        self.func_name = ""
        self.func_return_type = 0
        self.local_vars = set()
        self.brace_depth = 0

        # Register external functions
        for name, (nparams, _types) in EXTERNAL_FUNCTIONS.items():
            self.symbols[name] = {"type": XFUNC, "is_local": False, "is_array": False, "param_count": nparams}

    def error(self, msg, text=None):
        loc = f"{self.filename}:{self.linenum}"
        if text:
            self.errors.append(f"Error in line {self.linenum}: {msg} '{text}'")
        else:
            self.errors.append(f"Error in line {self.linenum}: {msg}")

    def warn(self, msg, text=None):
        if text:
            self.warnings.append(f"Warning in line {self.linenum}: {msg} '{text}'")
        else:
            self.warnings.append(f"Warning in line {self.linenum}: {msg}")

    # -- Token access --
    def lookahead(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token(TOK_EOF, None, "")

    def next(self):
        tok = self.lookahead()
        if self.pos < len(self.tokens):
            self.pos += 1
        return tok

    def match(self, expected):
        tok = self.next()
        if isinstance(expected, str):
            if tok.type != ord(expected):
                self.error(f"expected '{expected}'", tok.text)
        elif tok.type != expected:
            expected_name = self._tok_name(expected)
            self.error(f"expected {expected_name}", tok.text)
        return tok

    def _tok_name(self, t):
        rev = {v: k for k, v in globals().items() if isinstance(v, int) and v == t}
        if t < 128:
            return f"'{chr(t)}'"
        return rev.get(t, str(t))

    def at_end(self):
        return self.pos >= len(self.tokens)

    def peek_type(self):
        return self.lookahead().type

    # -- Symbol table helpers --
    def sym_lookup(self, name):
        return self.symbols.get(name)

    def sym_type(self, name):
        s = self.symbols.get(name)
        if s:
            return s["type"]
        return None

    def sym_add(self, name, stype, is_local=False, is_array=False, param_count=None):
        self.symbols[name] = {
            "type": stype,
            "is_local": is_local,
            "is_array": is_array,
            "param_count": param_count,
        }

    # ========================================================================
    # Top-level
    # ========================================================================
    def check(self):
        with open(self.filename, 'r', encoding='utf-8', errors='replace') as f:
            self.lines = f.readlines()

        self.linenum = 0
        has_end = False

        while self.linenum < len(self.lines):
            line = self.lines[self.linenum].rstrip('\n').rstrip('\r')
            self.linenum += 1
            self.tokens = list(tokenize_line(line))
            self.pos = 0

            if not self.tokens:
                continue

            self.compile_line()
            # Check if we saw 'end'
            for tok in self.tokens:
                if tok.type == END:
                    has_end = True

        if not has_end:
            self.warn("program has no 'end' statement")

        # Check for unresolved forward references
        for name, info in self.symbols.items():
            if info["type"] == LABEL and info.get("unresolved"):
                self.error(f"label/function not defined", name)

        return len(self.errors) == 0

    def compile_line(self):
        """Parse one line (may consume multiple lines for blocks)."""
        # Check for label definition: identifier followed by ':'
        if self.peek_type() in (ID, LABEL):
            tok = self.lookahead()
            # Look ahead for ':' (label definition)
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == ord(':'):
                name = tok.value if tok.type == ID else tok.text
                self.sym_add(name, LABEL)
                self.next()  # consume ID
                self.next()  # consume ':'

        self.compile_stmts()

    def compile_stmts(self):
        while not self.at_end():
            t = self.peek_type()
            if t in (ELSE, NEXT, RBRACE, TOK_EOF):
                break
            if t == SEMICOLON:
                self.next()
                continue
            self.compile_stmt()
            if self.peek_type() == SEMICOLON:
                self.next()

    def compile_stmt(self):
        tok = self.next()
        t = tok.type

        if t == FOR:
            self.compile_for()
        elif t == IF:
            self.compile_if()
        elif t == NC_INT32:
            self.compile_int32_decl()
        elif t == STR8:
            self.compile_str8_var()
        elif t == FUNC:
            self.compile_func()
        elif t == RET:
            self.compile_return()
        elif t == ID:
            self.compile_var(tok)
        elif t == LABEL:
            self.compile_var(tok)
        elif t == STRID:
            self.compile_strid_assign(tok)
        elif t == ARR:
            self.compile_arr_access(tok)
        elif t == PRINTF:
            self.compile_printf()
        elif t == NC_CONST:
            self.compile_const()
        elif t == WHILE:
            self.compile_while()
        elif t == END:
            pass  # end statement
        elif t == XFUNC:
            self.compile_xfunc_stmt(tok)
        elif t == BREAK:
            pass
        elif t == RETI:
            pass
        elif t == COPY:
            self.compile_copy()
        elif t == U8:
            self.compile_u_stmt(tok, "u8")
        elif t == U16:
            self.compile_u_stmt(tok, "u16")
        elif t == U32:
            self.compile_u_stmt(tok, "u32")
        elif t == FREE:
            self.match('(')
            self.match(')')
        elif t == DISPATCH:
            self.compile_dispatch()
        elif t == ord(':'):
            pass  # empty
        else:
            self.error("syntax error", tok.text)

    # -- Resolve identifier type from symbol table --
    def resolve_id(self, tok):
        """Re-classify an ID token based on symbol table."""
        name = tok.value if tok.type == ID else tok.text
        info = self.sym_lookup(name)
        if info:
            tok.type = info["type"]
            if info["is_array"]:
                tok.type = ARR
        return tok

    # ========================================================================
    # Statements
    # ========================================================================
    def compile_for(self):
        tok = self.next()
        if tok.type != ID:
            self.error("variable expected after 'for'", tok.text)
            return
        name = tok.value
        if not self.sym_lookup(name):
            self.sym_add(name, ID, is_local=self.in_func)
        self.match(EQ)
        self.compile_expression()
        self.match(TO)
        self.compile_expression()
        if self.peek_type() == STEP:
            self.next()
            self.compile_expression()
        self.match(LBRACE)
        self.compile_block()
        self.match(RBRACE)

    def compile_while(self):
        self.compile_expression()
        self.match(LBRACE)
        self.compile_block()
        self.match(RBRACE)

    def compile_if(self):
        self.compile_expression()
        self.match(LBRACE)
        self.compile_block()
        self.match(RBRACE)
        if self.peek_type() == ELSE:
            self.next()
            # Check for else { or else if
            if self.peek_type() == IF:
                self.next()
                self.compile_if()  # else if
            elif self.peek_type() == LBRACE:
                self.match(LBRACE)
                self.compile_block()
                self.match(RBRACE)
            else:
                # else on next line with {
                self.read_next_line_if_needed()
                if self.peek_type() == LBRACE:
                    self.match(LBRACE)
                    self.compile_block()
                    self.match(RBRACE)
                else:
                    self.error("expected '{' after 'else'")

    def compile_func(self):
        tok = self.next()
        return_type = 0

        # Optional return type
        if tok.type in (NC_INT32, STR8):
            return_type = tok.type
            tok = self.next()

        if tok.type not in (ID, LABEL):
            self.error("function name expected", tok.text)
            return

        func_name = tok.value if tok.type == ID else tok.text
        self.sym_add(func_name, LABEL)

        old_in_func = self.in_func
        old_locals = self.local_vars.copy()
        old_func_name = self.func_name
        old_func_ret = self.func_return_type

        self.in_func = True
        self.func_name = func_name
        self.func_return_type = return_type
        self.local_vars = set()

        self.match('(')
        param_count = 0

        while self.peek_type() != ord(')') and not self.at_end():
            ptok = self.next()
            if ptok.type not in (NC_INT32, STR8):
                self.error("type expected in parameter", ptok.text)
                break

            param_type = ptok.type
            # Check for int32[]
            if param_type == NC_INT32 and self.peek_type() == LBRACKET:
                self.next()  # [
                self.match(RBRACKET)  # ]
                param_type = ARR

            ptok = self.next()
            if ptok.type not in (ID, STRID):
                self.error("parameter name expected", ptok.text)
                break
            pname = ptok.value if ptok.type == ID else ptok.text
            is_arr = (param_type == ARR)
            self.sym_add(pname, ARR if is_arr else ID, is_local=True, is_array=is_arr)
            self.local_vars.add(pname)
            param_count += 1

            if self.peek_type() == ord(','):
                self.next()

        self.match(')')
        self.functions[func_name] = param_count
        self.symbols[func_name]["param_count"] = param_count

        self.match(LBRACE)
        self.compile_block()
        self.match(RBRACE)

        # Clean up local vars
        for lv in self.local_vars:
            if lv in self.symbols:
                del self.symbols[lv]

        self.in_func = old_in_func
        self.local_vars = old_locals
        self.func_name = old_func_name
        self.func_return_type = old_func_ret

    def compile_return(self):
        if not self.in_func:
            self.error("return outside function")
            return
        t = self.peek_type()
        if t not in (TOK_EOF, RBRACE, ord(':'), SEMICOLON):
            if self.func_return_type == 0:
                self.error("void function cannot return value")
            self.compile_expression()
        else:
            if self.func_return_type != 0:
                self.error("function must return a value")

    def compile_var(self, tok):
        name = tok.value if tok.type == ID else tok.text
        info = self.sym_lookup(name)

        # Function call: name(...)
        if self.peek_type() == ord('('):
            if info and info["type"] == LABEL:
                self.compile_func_call(name)
            elif info and info["type"] == XFUNC:
                self.compile_xfunc_call(name)
            elif not info:
                # Forward declaration — assume it's a function
                self.sym_add(name, LABEL, param_count=None)
                self.symbols[name]["unresolved"] = True
                self.compile_func_call(name)
            else:
                self.error("not a function", name)
            return

        # Array access: name[...]
        if info and info.get("is_array"):
            if self.peek_type() == LBRACKET:
                self.compile_arr_access_by_name(name)
                return

        # ++ / --
        if self.peek_type() == INC:
            self.next()
            if not info:
                self.sym_add(name, ID, is_local=self.in_func)
            return
        if self.peek_type() == DEC:
            self.next()
            if not info:
                self.sym_add(name, ID, is_local=self.in_func)
            return

        # Assignment: name = expr
        if not info:
            self.sym_add(name, ID, is_local=self.in_func)
            if self.in_func:
                self.local_vars.add(name)

        self.match(EQ)
        self.compile_expression()

    def compile_strid_assign(self, tok):
        name = tok.value if hasattr(tok, 'value') and tok.value else tok.text
        if not self.sym_lookup(name):
            self.sym_add(name, STRID)
        self.match(EQ)
        self.compile_expression()

    def compile_int32_decl(self):
        tok = self.next()
        if tok.type not in (ID, STRID):
            self.error("identifier expected", tok.text)
            return
        name = tok.value if tok.type == ID else tok.text

        if self.peek_type() == LBRACKET:
            # Array: int32 arr[size]
            if self.in_func:
                self.error("function-local arrays are not supported", name)
                return
            self.sym_add(name, ARR, is_local=False, is_array=True)
            self.match(LBRACKET)
            self.compile_expression()
            self.match(RBRACKET)
        else:
            # Variable: int32 x = expr
            self.sym_add(name, ID, is_local=self.in_func)
            if self.in_func:
                self.local_vars.add(name)
            if self.peek_type() == EQ:
                self.match(EQ)
                self.compile_expression()

    def compile_str8_var(self):
        tok = self.next()
        if tok.type != STRID:
            self.error("string identifier (ending with $) expected", tok.text)
            return
        name = tok.value
        self.sym_add(name, STRID)
        self.match(EQ)
        self.compile_expression()

    def compile_arr_access(self, tok):
        name = tok.text if hasattr(tok, 'text') else str(tok)
        self.match(LBRACKET)
        self.compile_expression()
        self.match(RBRACKET)
        if self.peek_type() in (INC, DEC):
            self.error("a[i]++/-- not supported, use a[i] = a[i] + 1")
            self.next()
            return
        self.match(EQ)
        self.compile_expression()

    def compile_arr_access_by_name(self, name):
        self.match(LBRACKET)
        self.compile_expression()
        self.match(RBRACKET)
        if self.peek_type() in (INC, DEC):
            self.error("a[i]++/-- not supported, use a[i] = a[i] + 1")
            self.next()
            return
        self.match(EQ)
        self.compile_expression()

    def compile_printf(self):
        self.match('(')
        tok = self.next()
        if tok.type != STR:
            self.error("format string expected", tok.text)
            return

        # Count format specifiers
        fmt = tok.value
        num_args = 0
        i = 0
        while i < len(fmt):
            if fmt[i] == '\\' and i + 1 < len(fmt):
                i += 2
                continue
            if fmt[i] == '%' and i + 1 < len(fmt):
                i += 1
                if fmt[i] != '%':
                    num_args += 1
            i += 1

        for _ in range(num_args):
            if self.peek_type() != ord(','):
                self.error("missing argument for printf")
                break
            self.match(',')
            self.compile_expression()

        self.match(')')

    def compile_const(self):
        tok = self.next()
        if tok.type != ID:
            self.error("identifier expected", tok.text)
            return
        name = tok.value
        self.match(EQ)
        negative = False
        if self.peek_type() == ord('-'):
            self.next()
            negative = True
        tok = self.match(NUM)
        val = tok.value if tok.value is not None else 0
        if negative:
            val = -val
        self.constants[name] = val
        self.sym_add(name, e_CNST)

    def compile_copy(self):
        self.match('(')
        self.compile_expression()
        self.match(',')
        self.compile_expression()
        self.match(',')
        self.compile_expression()
        self.match(',')
        self.compile_expression()
        self.match(',')
        self.compile_expression()
        self.match(')')

    def compile_u_stmt(self, tok, name):
        """u8/u16/u32 as statement: u8(arr, idx, val)"""
        self.match('(')
        self.compile_expression()  # arr ref
        self.match(',')
        self.compile_expression()  # idx
        self.match(',')
        self.compile_expression()  # val
        self.match(')')

    def compile_dispatch(self):
        self.match('(')
        self.compile_expression()
        self.match(')')
        self.match(LBRACE)

        # Read ahead to determine variant
        # Skip to first meaningful token (may need to read next lines)
        while self.at_end():
            if not self.read_next_line():
                return

        t = self.peek_type()

        if t == NUM:
            # Inline dispatch: 0: code, 1: code, ...
            count = 0
            while self.peek_type() != RBRACE:
                if self.at_end():
                    if not self.read_next_line():
                        break
                    continue

                if self.peek_type() == RBRACE:
                    break

                tok = self.next()
                if tok.type != NUM:
                    self.error("case number expected", tok.text)
                    return
                if tok.value != count:
                    self.error("sequential case number expected", tok.text)
                    return
                self.match(':')

                if self.peek_type() == LBRACE:
                    self.match(LBRACE)
                    self.compile_block()
                    self.match(RBRACE)
                elif not self.at_end() and self.peek_type() != RBRACE:
                    self.compile_stmts()

                count += 1

                # May need next line
                while self.at_end():
                    if not self.read_next_line():
                        break
            self.match(RBRACE)
        else:
            # Function dispatch: func_a, func_b, ...
            first = True
            while self.peek_type() != RBRACE:
                if self.at_end():
                    if not self.read_next_line():
                        break
                    continue
                if self.peek_type() == RBRACE:
                    break
                if not first:
                    if self.peek_type() == ord(','):
                        self.next()  # skip comma
                        # May need next line after comma
                        while self.at_end():
                            if not self.read_next_line():
                                break
                    else:
                        self.error("',' expected between dispatch entries")
                first = False
                tok = self.next()
                if tok.type not in (ID, LABEL):
                    self.error("function name expected", tok.text)
                    return
                name = tok.value if tok.type == ID else tok.text
                if not self.sym_lookup(name):
                    self.sym_add(name, LABEL, param_count=0)
                    self.symbols[name]["unresolved"] = True
            self.match(RBRACE)

    def compile_func_call(self, name):
        """Parse function call: name(args)"""
        info = self.sym_lookup(name)
        self.match('(')
        arg_count = 0
        while self.peek_type() != ord(')') and not self.at_end():
            self.compile_expression()
            arg_count += 1
            if self.peek_type() == ord(','):
                self.next()
        self.match(')')

        if info and info.get("param_count") is not None:
            if arg_count != info["param_count"]:
                self.error(f"wrong number of arguments (expected {info['param_count']}, got {arg_count})", name)

        # Mark function as resolved if it was a forward declaration
        if info and info.get("unresolved"):
            info["unresolved"] = False
            info["param_count"] = arg_count

    def compile_xfunc_stmt(self, tok):
        name = tok.text
        self.compile_xfunc_call(name)

    def compile_xfunc_call(self, name):
        info = self.sym_lookup(name)
        self.match('(')
        arg_count = 0
        while self.peek_type() != ord(')') and not self.at_end():
            self.compile_expression()
            arg_count += 1
            if self.peek_type() == ord(','):
                self.next()
        self.match(')')

    # ========================================================================
    # Block parsing (multi-line)
    # ========================================================================
    def compile_block(self):
        """Parse statements inside { }, reading new lines as needed."""
        while True:
            # Parse current line
            self.compile_stmts()

            t = self.peek_type()
            if t == RBRACE:
                return
            if t == ELSE:
                return
            if t == NEXT:
                return

            # Need more lines
            if not self.read_next_line():
                return

    def read_next_line(self):
        """Read the next source line and re-tokenize."""
        if self.linenum >= len(self.lines):
            return False
        line = self.lines[self.linenum].rstrip('\n').rstrip('\r')
        self.linenum += 1
        self.tokens = list(tokenize_line(line))
        self.pos = 0
        return True

    def read_next_line_if_needed(self):
        if self.at_end():
            self.read_next_line()

    # ========================================================================
    # Expression parser
    # ========================================================================
    def compile_expression(self):
        self.compile_and_expr()
        while self.peek_type() == OR:
            self.next()
            self.compile_and_expr()

    def compile_and_expr(self):
        self.compile_not_expr()
        while self.peek_type() == AND:
            self.next()
            self.compile_not_expr()

    def compile_not_expr(self):
        if self.peek_type() == NOT:
            self.next()
        self.compile_comp_expr()

    def compile_comp_expr(self):
        self.compile_bin_or_expr()
        while self.peek_type() in (EQ, NQ, LE, LQ, GR, GQ):
            self.next()
            self.compile_bin_or_expr()

    def compile_bin_or_expr(self):
        self.compile_bin_xor_expr()
        while self.peek_type() == ord('|'):
            self.next()
            self.compile_bin_xor_expr()

    def compile_bin_xor_expr(self):
        self.compile_bin_and_expr()
        while self.peek_type() == ord('^'):
            self.next()
            self.compile_bin_and_expr()

    def compile_bin_and_expr(self):
        self.compile_shift_expr()
        while self.peek_type() == ord('&'):
            self.next()
            self.compile_shift_expr()

    def compile_shift_expr(self):
        self.compile_add_expr()
        while self.peek_type() in (SHL, SHR):
            self.next()
            self.compile_add_expr()

    def compile_add_expr(self):
        self.compile_term()
        while self.peek_type() in (ord('+'), ord('-')):
            self.next()
            self.compile_term()

    def compile_term(self):
        self.compile_neg_factor()
        while self.peek_type() in (ord('*'), ord('/'), MOD, ord('%')):
            self.next()
            self.compile_neg_factor()

    def compile_neg_factor(self):
        if self.peek_type() == ord('-'):
            self.next()
        self.compile_factor()

    def compile_factor(self):
        t = self.peek_type()

        if t == ord('('):
            self.next()
            self.compile_expression()
            self.match(')')
        elif t == e_CNST:
            self.next()
        elif t == NUM:
            self.next()
        elif t == ID:
            tok = self.next()
            name = tok.value
            info = self.sym_lookup(name)
            if info and info.get("is_array"):
                # Array element or reference
                if self.peek_type() == LBRACKET:
                    self.next()
                    self.compile_expression()
                    self.match(RBRACKET)
                # else: array reference
            elif self.peek_type() == ord('('):
                # Function call in expression — treat as forward ref
                if not info:
                    self.sym_add(name, LABEL, param_count=None)
                    self.symbols[name]["unresolved"] = True
                self.compile_func_call(name)
            else:
                if not info:
                    self.sym_add(name, ID, is_local=self.in_func)
                    if self.in_func:
                        self.local_vars.add(name)
        elif t == ARR:
            tok = self.next()
            name = tok.text
            if self.peek_type() == LBRACKET:
                self.next()
                self.compile_expression()
                self.match(RBRACKET)
            # else: array reference
        elif t == LABEL:
            tok = self.next()
            name = tok.text if tok.type == LABEL else tok.value
            info = self.sym_lookup(name)
            if self.peek_type() == ord('('):
                if not info:
                    self.sym_add(name, LABEL, param_count=None)
                    self.symbols[name]["unresolved"] = True
                self.compile_func_call(name)
            # else: label reference
        elif t == XFUNC:
            tok = self.next()
            self.compile_xfunc_call(tok.text)
        elif t == STR:
            self.next()
        elif t == STRID:
            self.next()
        elif t == NIL:
            self.next()
        elif t == RND:
            self.next()
            self.match('(')
            self.compile_expression()
            self.match(')')
        elif t == U8:
            self.next()
            self.match('(')
            self.compile_expression()
            self.match(',')
            self.compile_expression()
            self.match(')')
        elif t == U16:
            self.next()
            self.match('(')
            self.compile_expression()
            self.match(',')
            self.compile_expression()
            self.match(')')
        elif t == U32:
            self.next()
            self.match('(')
            self.compile_expression()
            self.match(',')
            self.compile_expression()
            self.match(')')
        elif t == LEFTS:
            self.next()
            self.match('(')
            self.compile_expression()
            self.match(',')
            self.compile_expression()
            self.match(')')
        elif t == RIGHTS:
            self.next()
            self.match('(')
            self.compile_expression()
            self.match(',')
            self.compile_expression()
            self.match(')')
        elif t == MIDS:
            self.next()
            self.match('(')
            self.compile_expression()
            self.match(',')
            self.compile_expression()
            self.match(',')
            self.compile_expression()
            self.match(')')
        elif t == LEN:
            self.next()
            self.match('(')
            self.compile_expression()
            self.match(')')
        elif t == VAL:
            self.next()
            self.match('(')
            self.compile_expression()
            self.match(')')
        elif t == STRS:
            self.next()
            self.match('(')
            self.compile_expression()
            self.match(')')
        elif t == HEXS:
            self.next()
            self.match('(')
            self.compile_expression()
            self.match(')')
        elif t == INSTR:
            self.next()
            self.match('(')
            self.compile_expression()
            self.match(',')
            self.compile_expression()
            self.match(',')
            self.compile_expression()
            self.match(')')
        elif t == STRINGS:
            self.next()
            self.match('(')
            self.compile_expression()
            self.match(',')
            self.compile_expression()
            self.match(')')
        elif t == PARAM:
            self.next()
            self.match('(')
            self.match(')')
        elif t == PARAMS:
            self.next()
            self.match('(')
            self.match(')')
        elif t == FREE:
            self.next()
            self.match('(')
            self.match(')')
        elif t == TOK_EOF:
            pass  # end of input
        else:
            tok = self.next()
            self.error("syntax error in expression", tok.text)

    # ========================================================================
    # External function call on statement level
    # ========================================================================


# ============================================================================
# Main
# ============================================================================
def main():
    verbose = "-v" in sys.argv
    files = [a for a in sys.argv[1:] if not a.startswith("-")]

    if not files:
        print(f"NanoC Syntax Checker")
        print(f"Usage: python {os.path.basename(sys.argv[0])} [-v] <script.nc> [script2.nc ...]")
        print(f"  -v  Verbose mode")
        sys.exit(1)

    total_errors = 0
    total_warnings = 0

    for filename in files:
        if not os.path.exists(filename):
            print(f"Error: file not found: {filename}")
            total_errors += 1
            continue

        checker = NcChecker(filename, verbose=verbose)
        ok = checker.check()

        for w in checker.warnings:
            print(w)
        for e in checker.errors:
            print(e)

        nerr = len(checker.errors)
        nwarn = len(checker.warnings)
        total_errors += nerr
        total_warnings += nwarn

        if ok:
            print(f"{filename}: OK ({nwarn} warning(s))")
        else:
            print(f"{filename}: {nerr} error(s), {nwarn} warning(s)")

    sys.exit(0 if total_errors == 0 else 1)


if __name__ == "__main__":
    main()
