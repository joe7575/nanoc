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

    // Labels and jumps
    gosub label
    goto label
    label:
        ...
    return

    // Operators
    &&, ||, !=, ==, <, >, <=, >=
    +, -, *, /, mod
    &, |, ^  (bitwise)

    // Built-in functions
    rnd, len, val, chr$, mid$, left$, right$, str$, hex$
```

Data processing features (optional):

```
    get1, get2, get4, set1, set2, set4, copy, ref, reti
```

Supported data types are:

- int32: Signed Integer, 32 bit (-2,147,483,648 to 2,147,483,647)
- int32[]: Array (one dimension, up to 128 elements)
- str8: String variable (ends with $, up to 120 characters)
- const: Constant (numeric only)

The compiler generates bytecode executed by the virtual machine.
NanoC is designed to be small and fast for embedded applications.

## Event Handlers

NanoC supports event-driven programming via external functions:

```c
// Define event handler
on_can:
    int32 id = param()
    int32 d1 = param()
    int32 d2 = param()
    printf("CAN msg: id=%d\\n", id)
return

// Triggered from C code via fire_on_can(id, d1, d2)
```

### License

Copyright (C) 2024-2026 Joachim Stolberg

The software is licensed under the MIT license.

### History

**2026-02-07 V2.0.0**
- Rename to NanoC with C-style syntax
- Add int32, uint32, str8 type keywords
- Add printf() with format specifiers
- Add C-style blocks { }
- Add C-style operators &&, ||, !=
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
