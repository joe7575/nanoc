// Dispatch Example for NanoC
// Calls function based on index (0-based)

func handler_a() {
    printf("Handler A called\n")
}

func handler_b() {
    printf("Handler B called\n")
}

func handler_c() {
    printf("Handler C called\n")
}

// Test: dispatch each handler
for i = 0 to 2 {
    printf("Dispatching index %d: ", i)
    dispatch(i) {
        handler_a
        handler_b
        handler_c
    }
}

// Test: out-of-range index is skipped
printf("Out of range: ")
dispatch(5) {
    handler_a
    handler_b
    handler_c
}
printf("(skipped)\n")

// Test: negative index is skipped
printf("Negative: ")
dispatch(-1) {
    handler_a
    handler_b
    handler_c
}
printf("(skipped)\n")

printf("Done!\n")
end
