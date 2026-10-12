// else if chains

func int32 classify(int32 n) {
    if (n < 0) {
        return -1
    } else if (n == 0) {
        return 0
    } else if (n < 10) {
        return 1
    } else if (n < 100) {
        return 2
    } else {
        return 3
    }
}

int32 i = 0
int32 hits = 0

for i = -1 to 3 {
    printf("%d -> %d\n", i, classify(i))
}
printf("50 -> %d\n", classify(50))
printf("500 -> %d\n", classify(500))

// chain without final else
for i = 0 to 4 {
    if (i == 1) {
        hits = hits + 1
    } else if (i == 3) {
        hits = hits + 10
    }
}
printf("hits = %d\n", hits)

// nested if inside an else-if branch
i = 7
if (i < 5) {
    printf("small\n")
} else if (i < 10) {
    if (i == 7) {
        printf("seven\n")
    } else {
        printf("five to nine\n")
    }
} else {
    printf("large\n")
}
