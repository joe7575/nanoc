// Calculate PI digits using the Spigot algorithm
// NanoC example

int32 n = 16
int32 m = 10 * (n + 1) / 3
int32 d[60]

// Initialize array
for t = 0 to m - 1 {
    d[t] = 2
}

int32 p = 0
int32 c = 0
int32 a = 0
int32 b = 0
int32 f = 0
int32 e = 0

printf("PI = 3.")

for t = 0 to n {
    c = 0
    for a = m - 1 to 1 step -1 {
        b = 2 * a + 1
        f = d[a] * 10 + c
        e = f / b
        d[a] = f - e * b
        c = a * e
    }
    f = d[0] * 10 + c
    e = f / 10
    d[0] = f - e * 10
    
    // Output digit
    if (e < 10) {
        printf("%d", p)
        p = e
    }
}

printf("%d\n", p)
printf("Done!\n")
end
