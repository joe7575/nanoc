import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

is_active = False
index = 0
Opcodes = []
for line in open("../src/nb_int.h").readlines():
    if "Opcode definitions" in line:
        is_active = True
        continue
    elif "};" in line:
        is_active = False
        continue
    if is_active:
        words = line.split()
        if words[0] == "k_END,":
            opcode = words[0][2:-1]
            bytes = 1
        elif words[0].endswith("_Nx,"):
            # Variable length opcodes (PUSH_STR, PRINTF, etc.)
            opcode = words[0][2:-4]
            bytes = 0  # 0 = variable length
        elif words[0][0] == "k":
            opcode = words[0][2:-4]
            bytes = words[0][-2]
        else:
            continue
        Opcodes.append((opcode, int(bytes)))

print("Number of Opcodes: %d" % len(Opcodes))

first_line = True        
code = ""
for line in open("output.txt").readlines():
    code = code + line + " "
    
words = code.split()
idx = 0
while idx < len(words):
    byte = int(words[idx], 16)
    if byte < len(Opcodes):
        opcode, bytes = Opcodes[byte]
        print("%04X: %-14s %02X " % (index, opcode, byte), end="")
        if bytes == 0:
            # Variable length opcode
            if opcode == "PUSH_STR":
                # Format: [opcode][strlen][string...]
                strlen = int(words[idx+1], 16)
                bytes = strlen + 2
                print('%02X "' % strlen, end="")
                for i in range(2, bytes):
                    ch = int(words[idx+i], 16)
                    if ch >= 32 and ch < 127:
                        print("%c" % ch, end="")
                    else:
                        print(".", end="")
                print('"')
            elif opcode == "PRINTF":
                # Format: [opcode][nargs][strlen][string...]
                nargs = int(words[idx+1], 16)
                strlen = int(words[idx+2], 16)
                bytes = strlen + 3
                print('%02X %02X "' % (nargs, strlen), end="")
                for i in range(3, bytes):
                    ch = int(words[idx+i], 16)
                    if ch >= 32 and ch < 127:
                        print("%c" % ch, end="")
                    else:
                        print(".", end="")
                print('"')
            else:
                # Unknown variable length - try to skip
                print("(unknown variable length)")
                bytes = 1
        else:
            for i in range(1, bytes):
                print("%02X " % int(words[idx+i], 16), end="")
            print()
        index += bytes
        idx += bytes
    elif byte == 0xFF:
        break        
