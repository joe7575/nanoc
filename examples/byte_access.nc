// Byte Access Example for NanoC
// Demonstrates u8(), u16(), u32() functions

int32 buf[10]  // Buffer for byte access

// Write bytes
u8(buf, 0, 255)       // Write byte at offset 0
u8(buf, 1, 128)       // Write byte at offset 1
u8(buf, 2, 64)        // Write byte at offset 2
u8(buf, 3, 32)        // Write byte at offset 3

printf("Bytes written: %d, %d, %d, %d\n", u8(buf, 0), u8(buf, 1), u8(buf, 2), u8(buf, 3))

// Write 16-bit words
u16(buf, 4, 1000)     // Write word at offset 4
u16(buf, 6, 2000)     // Write word at offset 6

printf("Words written: %d, %d\n", u16(buf, 4), u16(buf, 6))

// Write 32-bit dwords
u32(buf, 8, 123456789)

printf("Dword written: %d\n", u32(buf, 8))

// Increment example: u16(buf, 4, u16(buf, 4) + 1)
printf("Before increment: %d\n", u16(buf, 4))
u16(buf, 4, u16(buf, 4) + 1)
printf("After increment: %d\n", u16(buf, 4))

// Check raw array values
printf("\nRaw array values:\n")
for i = 0 to 4 {
    printf("  buf[%d] = %d (0x%h)\n", i, buf[i], buf[i])
}

printf("\nDone!\n")
end
