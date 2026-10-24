// Regression tests for compiler/VM fixes:
// - empty for-loops must not run the body (global and local loop variable)
// - user functions with return values in expressions (incl. recursion, str8)
// - many calls to an already defined function (forward-declaration limit)
int32 a = 0
int32 b = 0
int32 c = 0
int32 i = 0
int32 y = 0
int32 v = 5
doit(v)
for i = 1 to 0 {
    a = a + 1
}
for i = 1 to 3 {
    b = b + i
}
for i = 3 to 1 step -1 {
    c = c + i
}
func doit(int32 x) {
    printf("fwd %d\n", x)
}
func int32 add(int32 x, int32 y) {
    return x + y
}
func int32 fib(int32 n) {
    if (n <= 1) {
        return n
    }
    return fib(n - 1) + fib(n - 2)
}
func str8 greeting() {
    return "hi"
}
func int32 g() {
    int32 s = 0
    for i = 1 to 0 {
        s = s + 1
    }
    return s
}
int32 r = add(2, 3)
printf("%d %d %d %d %d %s %d\n", a, b, c, r + add(1, 1), fib(6), greeting(), g())
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
y = add(y, 1)
printf("%d\n", y)
end
