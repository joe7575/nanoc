// User-defined function example
// Direct function calls like in C

int32 result = 0

// Call function directly (not gosub!)
add_numbers(10, 20)
printf("Result after add: %d\n", result)

multiply(5, 7)
printf("Result after multiply: %d\n", result)

// Call with expressions
add_numbers(result, 100)
printf("Result after add 100: %d\n", result)

// Nested calls
printf("\nNested calls:\n")
outer(3)

printf("\nDone!\n")
end

// User-defined function with local parameters
func add_numbers(int32 a, int32 b) {
    int32 sum = a + b
    result = sum
}

func multiply(int32 x, int32 y) {
    result = x * y
}

// Functions must be defined before they are used, especially if 
// called from other functions (no forward declaration possible).
func inner(int32 v) {
    int32 doubled = v * 2
    printf("  inner: v=%d, doubled=%d\n", v, doubled)
}

func outer(int32 n) {
    int32 i = 0
    while (i < n) {
        inner(i)
        i++
    }
}
