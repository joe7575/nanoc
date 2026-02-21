// Test i++ and i-- operators

int32 i = 0

printf("Initial i = %d\n", i)

i++
printf("After i++: i = %d\n", i)

i++
i++
printf("After 2x i++: i = %d\n", i)

i--
printf("After i--: i = %d\n", i)

// Use in loop
int32 sum = 0
int32 j = 0

while (j < 5) {
    sum = sum + j
    j++
}
printf("Sum of 0..4 = %d\n", sum)

// Count down
int32 count = 5
while (count > 0) {
    printf("Countdown: %d\n", count)
    count--
}

printf("Done!\n")
