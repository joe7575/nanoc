// Heron's method for square root calculation
// NanoC example

int32 v = 400000  // Value to calculate the square root
int32 s = 100     // Initial guess
int32 t = 0
int32 res[6]     // Array to store intermediate results
int32 done = 0

// Root calculation according to Heron
for i = 1 to 6 {
    if (done == 0) {
        t = ((v / s) + s) / 2
        res[i] = t
        if (t == s) {
            done = 1
        }
        s = t
    }
}

printf("The square root of %d is %d\n", v, t)

printf("Intermediate results:\n")
for i = 1 to 6 {
    printf("  Step %d: %d\n", i, res[i])
}

free
end
