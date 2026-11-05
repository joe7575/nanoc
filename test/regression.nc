// Regression tests for compiler/VM fixes:
// - empty for-loops must not run the body (global and local loop variable)
// - user functions with return values in expressions (incl. recursion, str8)
// - many calls to an already defined function (forward-declaration limit)
// - a forward-called function must not share its variable index with a later variable
// - str8 function result assigned to a variable
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
time()
printf("bare xfunc\n")
func int32 keep(int32 x) {
    time()
    return x
}
printf("keep %d\n", keep(7))
int32 mp[1]
int32 mi = 2
printf("mod %d %d\n", mi mod 3, mi % 3)
int32 mp2[1]
func str8 mstr(int32 x) {
    return "x"
}
payload(1, 2, mp2)
payload(1, 2, mstr(1))
printf("payloads ok\n")
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
fwd2()
int32 keepme = 5
func fwd2() {
}
int32 other = 7
str8 gs = greeting()
printf("vars %d %d %s\n", keepme, other, gs)
end
