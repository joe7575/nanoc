// Switch/Dispatch Example for NanoC
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
    switch(i) {
        case handler_a
        case handler_b
        case handler_c
    }
}

// Test: out-of-range index is skipped
printf("Out of range: ")
switch(5) {
    case handler_a
    case handler_b
    case handler_c
}
printf("(skipped)\n")

// Test: negative index is skipped
printf("Negative: ")
switch(-1) {
    case handler_a
    case handler_b
    case handler_c
}
printf("(skipped)\n")

printf("Done!\n")
end
