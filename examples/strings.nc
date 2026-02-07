// String handling example for NanoC
// String variables MUST end with $

// Declare string variables
str8 name$ = "Hello World"
str8 result$ = ""

// Print string
printf("Original: %s\n", name$)

// String length
int32 l = len(name$)
printf("Length: %d\n", l)

// Substring functions
result$ = left$(name$, 5)
printf("left$(name$, 5) = %s\n", result$)

result$ = right$(name$, 5)
printf("right$(name$, 5) = %s\n", result$)

result$ = mid$(name$, 6, 5)
printf("mid$(name$, 6, 5) = %s\n", result$)

// Find substring (0-based, returns -1 if not found)
int32 pos = instr(0, name$, "World")
printf("Position of 'World': %d\n", pos)

// Number to string conversion
int32 num = 12345
result$ = str$(num)
printf("str$(12345) = %s\n", result$)

// Number to hex string
result$ = hex$(255)
printf("hex$(255) = %s\n", result$)

// String concatenation
str8 a$ = "Hello"
str8 b$ = " "
str8 c$ = "NanoC"
result$ = a$ + b$ + c$
printf("Concatenated: %s\n", result$)

// Create repeated character string
str8 star$ = "*"
result$ = string$(10, star$)  // 10 asterisks
printf("string$(10, star$) = %s\n", result$)

printf("\nDone!\n")
end
