// NanoC Test Report
// Tests various language features

// Helper function: print separator line
func print_line() {
    printf("+----------------------------------------------------------+\n")
}

// Helper function: print equals line  
func print_equals() {
    printf("|==========================================================|\n")
}

// Main program
print_line()
printf("|                         Test Report                      |\n")
print_line()

// Test constants and large numbers
const MAX = 2147483647
int32 _max = MAX
printf("| The largest number is 2147483647                         |\n")
printf("| The almost largest is 2147483646                         |\n")

// Test array
int32 AR[6]
for i = 1 to 5 {
    AR[i] = i + 1
}

// Test string$ function
str8 B$ = string$(10, "A")
printf("| Length of string 'B$' should be 10: %d                   |\n", len(B$))

// Test while loop with countdown
int32 i = 21
printf("| ")
while (i > 0) {
    printf("%d ", i)
    i = i - 1
}
printf("   |\n")

// Test nested loops
for j = 1 to 5 {
    print_equals()
    printf("| ")
    for k = 1 to j {
        printf("%d:%d ", j, k)
    }
    // Padding: content "j:k " is 4 chars each, need 56 total after "| "
    if (j == 1) { printf("                                                     ") }
    if (j == 2) { printf("                                                 ") }
    if (j == 3) { printf("                                             ") }
    if (j == 4) { printf("                                         ") }
    if (j == 5) { printf("                                     ") }
    printf("|\n")
}

// Test memory functions
printf("| Memory: ")
free
printf("      |\n")

// Allocate some arrays
int32 BR[127]
int32 BR1[127]
int32 BR2[127]
int32 BR3[127]

printf("| After:  ")
free
printf("      |\n")

// Test comparisons
int32 C1 = 100
int32 C2 = 101
printf("| Comparisons: ")
if (C1 < C2) { printf("1 ") }
if (C1 != C2) { printf("2 ") }
if (C1 + 1 <= C2) { printf("3 ") }
if (C1 + 1 >= C2) { printf("4 ") }
if (C1 != C2) { printf("5 ") }
if (C1 > 99 and C2 > 100 and C1 < 101 and C2 < 102) { printf("6 ") }
if (not (C1 < 99 or C2 < 100 or C1 > 101 or C2 > 102)) { printf("7 ") }
printf("8 9 10                        |\n")

// Test time
printf("| Time since start = %d sec                                 |\n", time())

// Test string functions
str8 s$ = "111***222***333"
str8 left3$ = left$(s$, 3)
str8 mid3$ = mid$(s$, 6, 3)
str8 right3$ = right$(s$, 3)
printf("| left$=%s mid$=%s right$=%s                            |\n", left3$, mid3$, right3$)

str8 concat$ = left3$ + mid3$ + right3$
printf("| concat=%s str$=%s hex$=%s                       |\n", concat$, str$(444), hex$(1365))

// Test instr (0-based in NanoC, returns -1 if not found)
int32 i1 = instr(0, s$, "1")
int32 i2 = instr(1, s$, "1")
int32 i3 = instr(0, s$, "2")
int32 i4 = instr(8, s$, "2")
int32 i5 = instr(0, s$, "3")
int32 i6 = instr(14, s$, "3")
printf("| instr: %d %d %d %d %d %d                                     |\n", i1, i2, i3, i4, i5, i6)

// Test not found
int32 notfound = instr(0, s$, "X")
printf("| instr not found = %d (expect -1)                         |\n", notfound)

// Test numeric conversions
int32 v = 1234567890
int32 l = len("1234567890")
printf("| v=%d len=%d                                      |\n", v, l)

// Test hex$
printf("| hex$(255)=%s hex$(65535)=%s                            |\n", hex$(255), hex$(65535))

print_line()
end
