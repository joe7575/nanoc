// Event Handler Example
// Demonstrates fire_on_can() triggering on_can() handler
// Now with LOCAL variables in the handler!

int32 counter = 0;
int32 payload[2]; // 2 * int32 = 8 Bytes

// Main loop - simulates external events
printf("Starting event handler demo\n")

// Simulate CAN message events
fire_on_can(100, 1, 2, payload)
fire_on_can(200, 3, 4, payload)
fire_on_can(300, 5, 6, payload)

printf("Main program done, counter = %d\n", counter)
printf("Payload after events: %d, %d\n", payload[0], payload[1])
end

// Event handler for CAN messages
// id, d1, d2 and temp are LOCAL variables (on stack)
func on_can(int32 id, int32 d1, int32 d2, int32[] pld) {
    int32 temp = id * 2     // LOCAL variable!
    printf("on_can: id=%d, data=%d+%d, temp=%d\n", id, d1, d2, temp)
    counter++               // counter is GLOBAL
    u8(payload, 0, u8(payload, 0) + 1)
}

