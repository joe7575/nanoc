// Math operations example for NanoC

printf("1 + 2 = %d (expected 3)\n", 1 + 2)
printf("1 - 2 = %d (expected -1)\n", 1 - 2)
printf("2 - 1 = %d (expected 1)\n", 2 - 1)
printf("2 * 3 = %d (expected 6)\n", 2 * 3)
printf("7 / 2 = %d (expected 3)\n", 7 / 2)
printf("7 mod 2 = %d (expected 1)\n", 7 mod 2)

// Bitwise operations
printf("1 | 2 = %d (expected 3)\n", 1 | 2)
printf("3 & 2 = %d (expected 2)\n", 3 & 2)
printf("3 ^ 2 = %d (expected 1)\n", 3 ^ 2)

// Shift operations
printf("1 << 4 = %d (expected 16)\n", 1 << 4)
printf("256 >> 3 = %d (expected 32)\n", 256 >> 3)
printf("0xFF << 8 = %d (expected 65280)\n", 255 << 8)

// Comparison operators
int32 a = 5
int32 b = 3

if (a > b) {
    printf("%d > %d is true\n", a, b)
}

if (a != b) {
    printf("%d != %d is true\n", a, b)
}

if (a >= 5 && b <= 3) {
    printf("a >= 5 AND b <= 3 is true\n")
}

end
