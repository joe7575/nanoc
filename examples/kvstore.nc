// KV-Store Example for NanoC
// Demonstrates the key-value store functionality

// Create a store with capacity for 100 entries, default value -1
int32 store = kvs_create(100, -1)

if (store < 0) {
    printf("Error: Could not create KV store\n")
    end
}

printf("KV-Store created with ID: %d\n", store)

// Store some values
printf("Storing values...\n")
kvs_set(store, 10, 1000)
kvs_set(store, 20, 2000)
kvs_set(store, 15, 1500)
kvs_set(store, 5, 500)
kvs_set(store, 25, 2500)

// Read values back
printf("Reading values:\n")
printf("Key 10 = %d\n", kvs_get(store, 10))
printf("Key 20 = %d\n", kvs_get(store, 20))
printf("Key 15 = %d\n", kvs_get(store, 15))
printf("Key 5 = %d\n", kvs_get(store, 5))
printf("Key 25 = %d\n", kvs_get(store, 25))

// Try to read a non-existing key (should return -1)
printf("Key 99 (not exists) = %d\n", kvs_get(store, 99))

// Update an existing key
printf("Updating key 15 to 9999...\n")
kvs_set(store, 15, 9999)
printf("Key 15 = %d\n", kvs_get(store, 15))

// Use negative keys
kvs_set(store, -100, 42)
printf("Key -100 = %d\n", kvs_get(store, -100))

printf("Done!\n")
end
