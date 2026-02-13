/*

Copyright 2024-2025 Joachim Stolberg

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the “Software”), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <assert.h>
#include <time.h>
#include <stdarg.h>
#ifdef _WIN32
#include <windows.h>
#else
#include <errno.h>
#endif
#include "nc.h"
#include "nc_int.h"
#include "nc_kvstore.h"

// KV-Store instances (max 4 stores supported)
#define MAX_KVS_STORES 4

#define kSETCUR             (NB_XFUNC + 0)
#define kCLRSCR             (NB_XFUNC + 1)
#define kCLRLINE            (NB_XFUNC + 2)
#define kTIME               (NB_XFUNC + 3)
#define kSLEEP              (NB_XFUNC + 4)
#define kINPUT              (NB_XFUNC + 5)
#define kINPUT_STR          (NB_XFUNC + 6)
#define kCMD                (NB_XFUNC + 7)
#define kSGN                (NB_XFUNC + 8)
#define kKVS_CREATE         (NB_XFUNC + 9)
#define kKVS_SET            (NB_XFUNC + 10)
#define kKVS_GET            (NB_XFUNC + 11)
#define kFIRE_ON_CAN        (NB_XFUNC + 12)

// Memory: 8 bytes header + 256 entries * 8 bytes each = 2056 bytes per store
#define KVS_MEM_SIZE 2056
static kvs_store_t *kvs_stores[MAX_KVS_STORES] = {NULL};
static uint8_t kvs_memory[MAX_KVS_STORES][KVS_MEM_SIZE];

// Event handler addresses (resolved after compile)
static uint16_t on_can_addr = 0;

/* msleep(): Sleep for the requested number of milliseconds. */
int msleep(uint32_t msec)
{
#ifdef _WIN32
    Sleep(msec);
    return 0;
#else
    struct timespec ts;
    int res;

    ts.tv_sec = msec / 1000;
    ts.tv_nsec = (msec % 1000) * 1000000;

    do {
        res = nanosleep(&ts, &ts);
    } while (res && errno == EINTR);
    return res;
#endif
}

char *nc_get_code_line(void *fp, char *line, int max_line_len) {
    return fgets(line, max_line_len, fp);
}

void nc_print(const char * format, ...) {
    va_list args;
    va_start(args, format);
    vprintf(format, args);
    va_end(args);
    fflush(stdout);
}

int main(int argc, char* argv[]) {
    uint16_t res = NB_BUSY;
    uint16_t cycles;
    uint16_t errors;
    uint32_t timeout = 0;
    uint32_t startval = time(NULL);
    int compile_only = 0;
    char *filename = NULL;
#if defined(cfg_DATA_ACCESS) && !defined(cfg_STRING_SUPPORT)
    bool interrupted = false;
#endif
    
    // Parse command line arguments
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-c") == 0) {
            compile_only = 1;
        } else if (argv[i][0] != '-') {
            filename = argv[i];
        }
    }
    
    if (filename == NULL) {
        nc_print("Usage: %s [-c] <program>\n", argv[0]);
        nc_print("  -c  Compile only, dump bytecode to stdout\n");
        return 1;
    }
    if (!compile_only) {
        nc_print("NanoC Compiler V%s\n", SVERSION);
    }
    nc_init();
#if defined(cfg_DATA_ACCESS) && !defined(cfg_STRING_SUPPORT)
    assert(nc_define_external_function("send", 3, (uint8_t[]){NB_NUM, NB_NUM, NB_REF}, NB_NONE) == NB_XFUNC + 0);
#elif defined(cfg_STRING_SUPPORT)
    assert(nc_define_external_function("setcur", 2, (uint8_t[]){NB_NUM, NB_NUM}, NB_NONE) == kSETCUR);
    assert(nc_define_external_function("clrscr", 0, NULL, NB_NONE) == kCLRSCR);
    assert(nc_define_external_function("clrline", 1, (uint8_t[]){NB_NUM}, NB_NONE) == kCLRLINE);
    assert(nc_define_external_function("time", 0, NULL, NB_NUM) == kTIME);
    assert(nc_define_external_function("sleep", 1, (uint8_t[]){NB_NUM}, NB_NONE) == kSLEEP);
    assert(nc_define_external_function("input", 1, (uint8_t[]){NB_STR}, NB_NUM) == kINPUT);
    assert(nc_define_external_function("input$", 1, (uint8_t[]){NB_STR}, NB_STR) == kINPUT_STR);
    assert(nc_define_external_function("cmd", 3, (uint8_t[]){NB_NUM, NB_ANY, NB_ANY}, NB_NUM) == kCMD);
    assert(nc_define_external_function("sgn", 1, (uint8_t[]){NB_NUM}, NB_NUM) == kSGN);
    assert(nc_define_external_function("kvs_create", 2, (uint8_t[]){NB_NUM, NB_NUM}, NB_NUM) == kKVS_CREATE);
    assert(nc_define_external_function("kvs_set", 3, (uint8_t[]){NB_NUM, NB_NUM, NB_NUM}, NB_NONE) == kKVS_SET);
    assert(nc_define_external_function("kvs_get", 2, (uint8_t[]){NB_NUM, NB_NUM}, NB_NUM) == kKVS_GET);
    // Event trigger function: fire_on_can(id, data1, data2) -> calls on_can: label
    assert(nc_define_external_function("fire_on_can", 4, (uint8_t[]){NB_NUM, NB_NUM, NB_NUM, NB_REF}, NB_NONE) == kFIRE_ON_CAN);
#endif

    void *instance = nc_create();

#ifdef cfg_LINE_NUMBERS
    //FILE *fp = fopen("../examples/lineno.nc", "r");
    FILE *fp = fopen("../examples/trace_on.nc", "r");
    //FILE *fp = fopen("../examples/calc_pi.nc", "r");
#elif !defined(cfg_STRING_SUPPORT)
    FILE *fp = fopen("../examples/heron.nc", "r");
#else
    FILE *fp = fopen(filename, "r");
#endif
    if(fp == NULL) {
        nc_print("Error: could not open file '%s'\n", filename);
        return -1;
    }

    errors = nc_compile(instance, fp);
    fclose(fp);

    if(errors > 0) {
        return 1;
    }

    // Compile-only mode: dump bytecode and exit
    if (compile_only) {
        nc_dump_code(instance);
        nc_destroy(instance);
        return 0;
    }

#if defined(cfg_DATA_ACCESS) && !defined(cfg_STRING_SUPPORT)
    uint16_t start = nc_get_label_address(instance, "start");
#endif
#if defined(cfg_LINE_NUMBERS)
    uint16_t error = nc_get_label_address(instance, "1000");
#else
    uint16_t error = 0;
#endif
#if defined(cfg_STRING_SUPPORT)
    // Get event handler address (0 if not defined)
    on_can_addr = nc_get_label_address(instance, "on_can");
#endif

    //nc_output_symbol_table(instance);
    nc_print("\nNanoC Interpreter V%s\n", SVERSION);
    //nc_dump_code(instance);

    while(res >= NB_BUSY) {
        cycles = 5000;
        while(cycles > 0 && res >= NB_BUSY && timeout <= time(NULL)) {
            res = nc_run(instance, &cycles);
            if(res == NB_BREAK) {
                uint32_t lineno = nc_pop_num(instance);
                nc_print("Break in line %u\n", lineno);
                uint32_t val = nc_get_number(instance, 0);
                printf("read num %d = %d\n", 0, val);
#ifdef cfg_STRING_SUPPORT                
                char *ptr = nc_get_string(instance, 1);
                if(ptr != NULL) {
                    printf("read str %d = %s\n", 1, ptr);
                }
#endif
                val = nc_get_arr_elem(instance, 3, 0);
                printf("read arr %d(%d) = %d\n", 3, 0, val);
#if defined(cfg_DATA_ACCESS) && !defined(cfg_STRING_SUPPORT)
            } else if(res == NB_RETI) {
                interrupted = false;
            } else if(res == NB_XFUNC) {
                // send
                uint8_t arr[80];
                uint16_t ref = nc_pop_arr_ref(instance);
                nc_read_arr(instance, ref, arr, 80);
                uint32_t id = nc_pop_num(instance);
                uint8_t port = nc_pop_num(instance);
                nc_print("send on port %d: %u %02X %02X %02X %02X %08X\n", port, id, arr[0], arr[1], arr[2], arr[3], ACS32(arr[4]));
                if(start > 0 && !interrupted) {
                    nc_set_pc(instance, start);
                    nc_push_num(instance, 1);
                    nc_push_num(instance, 2);
                    nc_write_arr(instance, ref, (uint8_t*)"\x08\x07\x06\x05\x04\x03\x02\x01", 8);
                    interrupted = true;
                }    
#elif defined(cfg_STRING_SUPPORT)
            } else if(res == NB_XFUNC) {
                // setcur
                uint8_t y = nc_pop_num(instance);
                uint8_t x = nc_pop_num(instance);
                x = MAX(1, MIN(x, 60));
                y = MAX(1, MIN(y, 60));
                nc_print("\033[%u;%uH", y, x);
            } else if(res == NB_XFUNC + 1) {
                // clrscr
                nc_print("\033[2J");
            } else if(res == NB_XFUNC + 2) {
                // clrline
                nc_print("\033[2K");
            } else if(res == NB_XFUNC + 3) {
                // time
                nc_push_num(instance, time(NULL) - startval);
            } else if(res == NB_XFUNC + 4) {
                // sleep
                timeout = time(NULL) + nc_pop_num(instance);
            } else if(res == NB_XFUNC + 5) {
                // input
                char str[80];
                nc_pop_str(instance, str, 80);
                nc_print("%s?  ", str);
                //fgets(str, 80, stdin);
                //str[strlen(str)-1] = '\0';
                //nc_push_num(instance, atoi(str));
                nc_push_num(instance, 12);
            } else if(res == NB_XFUNC + 6) {
                // input$
                char str[80];
                nc_pop_str(instance, str, 80);
                nc_print("%s?  ", str);
                //fgets(str, 80, stdin);
                //str[strlen(str)-1] = '\0';
                //nc_push_str(instance, str);
                nc_push_str(instance, "Joe");
#endif
            } else if(res == NB_XFUNC + 7) {
                // cmd
                uint8_t depth = nc_stack_depth(instance);
                if(depth == 3) {
                    uint32_t val1 = nc_peek_num(instance, 3);
                    if(val1 >= 128) {
#ifdef cfg_STRING_SUPPORT                        
                        char buff[80];
                        char *str3 = nc_pop_str(instance, buff, 80);
                        uint32_t val2 = nc_pop_num(instance);
                        nc_print("cmd on port %u, %d, %s\n", val1, val2, str3);
#else
                        uint32_t val2 = nc_pop_num(instance);
                        nc_print("cmd on port %u, %d\n", val1, val2);
#endif
                    } else {
                        uint32_t val3 = nc_pop_num(instance);
                        uint32_t val2 = nc_pop_num(instance);
                        nc_print("cmd on port %u, %d, %d\n", val1, val2, val3);
                    }
                    nc_pop_num(instance);
                    nc_push_num(instance, -1);
                } else if(depth == 2) {
                    uint32_t val2 = nc_pop_num(instance);
                    uint32_t val1 = nc_pop_num(instance);
                    nc_print("cmd on port %u, %u\n", val1, val2);
                    nc_push_num(instance, 0);
                    nc_set_pc(instance, error);
                    nc_push_num(instance, 3);
                } else {
                    nc_print("Error: wrong number of parameters\n");
                    nc_push_num(instance, -3);
                }
            } else if(res == NB_XFUNC + 8) {
                // sgn
                int32_t val = nc_pop_num(instance);
                nc_push_num(instance, (val > 0) - (val < 0));
            } else if(res == NB_XFUNC + 9) {
                // kvs_create(num_elem, default_val) -> store_id
                int32_t default_val = nc_pop_num(instance);
                int32_t num_elem = nc_pop_num(instance);
                int32_t store_id = -1;
                for (int i = 0; i < MAX_KVS_STORES; i++) {
                    if (kvs_stores[i] == NULL) {
                        if (num_elem > 256) num_elem = 256;
                        if (num_elem < 1) num_elem = 1;
                        kvs_stores[i] = kvs_create(kvs_memory[i], (uint16_t)num_elem, default_val);
                        store_id = i;
                        break;
                    }
                }
                nc_push_num(instance, store_id);
            } else if(res == NB_XFUNC + 10) {
                // kvs_set(store_id, key, value)
                int32_t value = nc_pop_num(instance);
                int32_t key = nc_pop_num(instance);
                int32_t store_id = nc_pop_num(instance);
                if (store_id >= 0 && store_id < MAX_KVS_STORES && kvs_stores[store_id] != NULL) {
                    kvs_set(kvs_stores[store_id], key, value);
                }
            } else if(res == NB_XFUNC + 11) {
                // kvs_get(store_id, key) -> value
                int32_t key = nc_pop_num(instance);
                int32_t store_id = nc_pop_num(instance);
                int32_t value = 0;
                if (store_id >= 0 && store_id < MAX_KVS_STORES && kvs_stores[store_id] != NULL) {
                    value = kvs_get(kvs_stores[store_id], key);
                }
                nc_push_num(instance, value);
            } else if(res == NB_XFUNC + 12) {
                // fire_on_can(id, data1, data2, data_arr) -> jumps to on_can: label
                int32_t data_arr = nc_pop_num(instance);
                int32_t data2 = nc_pop_num(instance);
                int32_t data1 = nc_pop_num(instance);
                int32_t id = nc_pop_num(instance);
                if (on_can_addr > 0) {
                    // Jump to on_can handler (like gosub)
                    nc_set_pc(instance, on_can_addr);
                    // Push params in normal order (handler receives in LIFO order)
                    nc_push_num(instance, id);
                    nc_push_num(instance, data1);
                    nc_push_num(instance, data2);
                    nc_push_num(instance, data_arr);
                } else {
                    nc_print("Warning: on_can handler not defined\n");
                }
            } else if(res >= NB_XFUNC) {
                nc_print("Unknown external function\n");
            }
        }
        msleep(100);
    }
    nc_destroy(instance);
    nc_print("Ready.\n");
    return 0;
}
