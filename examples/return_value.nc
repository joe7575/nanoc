// Function with return value example
// func int32 funcname(...) returns int32

// Functions must be defined before they are called

// Function returning int32
func int32 add(int32 a, int32 b) {
    return a + b
}

func int32 square(int32 n) {
    return n * n
}

func int32 max(int32 a, int32 b) {
    if (a > b) {
        return a
    }
    return b
}

// Recursive function example
func int32 factorial(int32 n) {
    if (n <= 1) {
        return 1
    }
    int32 prev = factorial(n - 1)
    return n * prev
}

// Main program starts here
int32 x = 0
int32 y = 0

x = add(10, 20)
printf("add(10, 20) = %d\n", x)

y = square(7)
printf("square(7) = %d\n", y)

x = max(15, 8)
printf("max(15, 8) = %d\n", x)

x = factorial(5)
printf("factorial(5) = %d\n", x)

end
