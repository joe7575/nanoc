// Dispatch Example for NanoC

// === Function Dispatch ===
// Calls function based on index (0-based, like GOSUB)

func handler_a() {
    printf("Handler A called\n")
}

func handler_b() {
    printf("Handler B called\n")
}

func handler_c() {
    printf("Handler C called\n")
}

printf("=== Function Dispatch ===\n")
for i = 0 to 2 {
    printf("Dispatching index %d: ", i)
    dispatch(i) {
        handler_a
        handler_b
        handler_c
    }
}

// === Inline Dispatch ===
// Code runs in current scope (access to local variables)

printf("\n=== Inline Dispatch ===\n")

func on_event(int32 id, int32 d1, int32 d2) {
    printf("on_event(id=%d, d1=%d, d2=%d): ", id, d1, d2)
    dispatch(id) {
        0: printf("idle\n")
        1: printf("run d1=%d d2=%d\n", d1, d2)
        2: {
            int32 sum = d1 + d2
            printf("error sum=%d\n", sum)
        }
    }
}

on_event(0, 10, 20)
on_event(1, 30, 40)
on_event(2, 50, 60)

// Out-of-range: silently skipped
printf("Out of range: ")
dispatch(99) {
    0: printf("FAIL\n")
}
printf("(skipped)\n")

printf("Done!\n")
end
