// str2arr / arr2str: copy strings into byte arrays and back

int32 buf[8]      // 32 bytes

func show(int32[] arr, int32 offs) {
    printf("'%s'\n", arr2str(arr, offs))
}

str8 id = "CANbridge"
str2arr(buf, 0, id)                   // writes 9 chars + '\0'
printf("len = %d, byte 0 = %d\n", len(id), u8(buf, 0))

str2arr(buf, 9, " Basic")             // append: overwrite the '\0'
printf("%s\n", arr2str(buf, 0))
show(buf, 10)                         // array reference parameter

// TLV-like frame: header bytes followed by a string
u8(buf, 0, 0)
u16(buf, 1, 4)
str2arr(buf, 3, "abc")
printf("payload = %s\n", arr2str(buf, 3))
end
