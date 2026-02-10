// Test: u8/u16/u32 with function-local arrays
int32 Buf[10]

func test_byte_access(int32[] buf) {

    // Write bytes
    u8(buf, 0, 255)
    u8(buf, 1, 128)
    u8(buf, 2, 64)
    u8(buf, 3, 32)
    printf("u8: %d, %d, %d, %d\n", u8(buf, 0), u8(buf, 1), u8(buf, 2), u8(buf, 3))

    // Write 16-bit words
    u16(buf, 4, 1000)
    u16(buf, 6, 2000)
    printf("u16: %d, %d\n", u16(buf, 4), u16(buf, 6))

    // Write 32-bit dword
    u32(buf, 8, 123456789)
    printf("u32: %d\n", u32(buf, 8))
}

test_byte_access(Buf)
end
