// Test: Array reference parameters for functions

// Function that modifies array elements
func myFunc(int32[] arr, int32 size) {
    int32 i = 0;
    while(i < size) {
        arr[i] = arr[i] * 2;
        i = i + 1;
    }
}

// Function that sums array elements
func int32 sumArr(int32[] arr, int32 size) {
    int32 sum = 0;
    int32 i = 0;
    while(i < size) {
        sum = sum + arr[i];
        i = i + 1;
    }
    return sum;
}

// Main program
int32 data[5];
data[0] = 1;
data[1] = 2;
data[2] = 3;
data[3] = 4;
data[4] = 5;

printf("Before: %d %d %d %d %d\n", data[0], data[1], data[2], data[3], data[4]);
printf("Sum before: %d\n", sumArr(data, 5));

myFunc(data, 5);

printf("After:  %d %d %d %d %d\n", data[0], data[1], data[2], data[3], data[4]);
printf("Sum after: %d\n", sumArr(data, 5));
