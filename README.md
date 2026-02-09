NanoC
=====

A small C-style compiler with virtual machine for embedded systems.
This software is written from scratch in C.

## Language Features

```c
    // Comments (C-style)
    // Variable declarations
    int32 x = 42
    int32 arr[10]
    str8 name$ = "hello"
    const MAX = 100

    // Control flow (C-style blocks)
    if (condition) {
        statements...
    } else {
        statements...
    }

    while (condition) {
        statements...
    }

    for i = 1 to 10 {
        statements...
    }

    // Output
    printf("value = %d, hex = %h, str = %s\n", num, num, str)

    // Operators
    and, or, not, ==, !=, <, >, <=, >=
    +, -, *, /, mod
    &, |, ^  (bitwise)
    ++, --   (increment/decrement)

    // Built-in functions
    rnd, len, mid$, left$, right$, str$, hex$, instr, string$
```

Byte/Word access functions (optional):

```c
    u8(arr, idx)         // Read byte at byte offset idx
    u8(arr, idx, val)    // Write byte at byte offset idx
    u16(arr, idx)        // Read 16-bit word at byte offset idx
    u16(arr, idx, val)   // Write 16-bit word at byte offset idx
    u32(arr, idx)        // Read 32-bit dword at byte offset idx
    u32(arr, idx, val)   // Write 32-bit dword at byte offset idx
    copy(src, soff, dst, doff, len)  // Copy len bytes
```

Supported data types are:

- int32: Signed Integer, 32 bit (-2,147,483,648 to 2,147,483,647)
- int32[]: Array (one dimension, up to 128 elements)
- int32[] (parameter): Array reference passed to functions
- str8: String variable (ends with $, up to 120 characters)
- const: Constant (numeric only)

The compiler generates bytecode executed by the virtual machine.
NanoC is designed to be small and fast for embedded applications.

## User-Defined Functions

NanoC supports user-defined functions with parameters and return values:

```c
// Function with return value
func int32 add(int32 a, int32 b) {
    return a + b
}

// Array reference parameters (passed by reference)
func int32 sumArr(int32[] arr, int32 size) {
    int32 sum = 0
    for i = 0 to size - 1 {
        sum = sum + arr[i]
    }
    return sum
}

// Usage
int32 data[5]
data[0] = 1
data[1] = 2
int32 total = sumArr(data, 5)
```

## Event Handlers

NanoC supports event-driven programming via external functions:

```c
// Event handler function (called from C code via fire_on_can)
func on_can(int32 id, int32 d1, int32 d2) {
    printf("CAN msg: id=%d, d1=%d, d2=%d\n", id, d1, d2)
}

// Test the handler
fire_on_can(100, 1, 2)
```

### License

Copyright (C) 2024-2026 Joachim Stolberg

The software is licensed under the MIT license.

### History

**2026-02-09 V2.1.0**
- Add array reference parameters for functions (int32[] syntax)

**2026-02-07 V2.0.0**
- Rename to NanoC with C-style syntax
- Add int32, str8 type keywords
- Add printf() with format specifiers
- Add C-style blocks { }
- Add C-style operators ==, !=
- Add C-style comments //
- Add array syntax arr[i]
- Add event handler mechanism
- Remove BASIC backward compatibility

**2025-09-26 V1.0.4**
- Add '|', '&', and '^' operators

**2025-03-11 V1.0.3**
- Add ELSEIF statement

**2025-01-24 V1.0.2**
- Add RETI command

**2025-01-11 V1.0.1**
- Rework data access API and functions

**2025-01-01 V1.0.0**
- First release
