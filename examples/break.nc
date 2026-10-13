// break leaves the innermost for/while loop

func int32 find(int32[] arr, int32 size, int32 value) {
    for i = 0 to size - 1 {
        if (arr[i] == value) {
            return i
        }
    }
    return -1
}

int32 data[5]
for i = 0 to 4 {
    data[i] = i * 10
}

// break out of a for loop
for i = 0 to 4 {
    if (data[i] > 15) {
        break
    }
    printf("data[%d] = %d\n", i, data[i])
}

// break out of a while loop
int32 n = 0
while (1) {
    n++
    if (n == 3) {
        break
    }
}
printf("n = %d\n", n)

// break inside a nested loop only leaves the inner loop
for i = 1 to 3 {
    for j = 1 to 10 {
        if (j > i) {
            break
        }
        printf("%d", j)
    }
    printf("\n")
}

// return from inside a loop
printf("index of 30: %d\n", find(data, 5, 30))
printf("index of 99: %d\n", find(data, 5, 99))
end
