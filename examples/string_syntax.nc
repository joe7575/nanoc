// Strings without the BASIC '$' suffix (the '$' form is still supported)

str8 greeting = "Hello"
str8 old$ = "World"          // old form, still valid

func shout(str8 text, int32 times) {
    printf("%s%s\n", text, string(times, "!"))
}

str8 msg = greeting + ", " + old$
shout(msg, 3)
printf("left = %s, mid = %s\n", left(msg, 5), mid(msg, 7, 3))
printf("right = %s\n", right(msg, 3))
printf("len = %d, str = %s, hex = %s\n", len(msg), str(1234), hex(255))

if (left(msg, 5) == greeting) {
    printf("starts with %s\n", greeting)
}
if (mid$(msg, 7, 5) != "World") {
    printf("unexpected\n")
}
end
