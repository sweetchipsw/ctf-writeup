from pwn import *
from capstone import *

elf = ELF('./rabbit')

# List symbols at program

target = "func"

func = elf.symbols[target]

print(func)

basesize = func
idx =0
t2 = False
patched_jmp = []
while True:
    if idx > 1000:
        break
    asd = elf.read(func, 20)
    print(disasm(asd,basesize,3))

    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = True
    i = md.disasm(asd, func, 3)
    i1 = next(i)
    i2 = next(i)
    i3 = next(i)
    i.close()
    #input(">")

    if i1.mnemonic == "ret":
        elf.save("./rabbit.patched")
        input("> RET DETECTED and saved")

    if t2:
        t2 = False
        if i1.mnemonic == "je":
            if (i2.operands[0].imm) in patched_jmp:
                print("already patched for next instruction. pass!")
                #print("T2 detect / ", i2.operands[0].imm-i1.size)
                func = i1.operands[0].imm
                print("go to ", hex(func))
                #patched_jmp.append(i2.operands[0].imm-i1.size)
                continue
            else:
                func = func + i1.size
                patched_jmp.append(i2.operands[0].imm)
                continue


    print(i1, i2, i3)
    if i1.size == 6 and i1.mnemonic == "cmp":
        print("good", i1.size, i1.operands[0], i1.operands[1].imm == 0x80000000)
        print("good1", i2.operands[0], hex(i2.operands[0].imm))
    elif i1.mnemonic == "test" and i2.mnemonic == "jmp":
        t2 = True
        #if i2.operands[0].imm in patched_jmp:
        #    func = func + i1.size
        #    print("[!] already patched... skipped this instruction")
        #    continue
        #testsize = i1.size
        #print("NEW 0x%x" % (i2.operands[0].imm))
        #patched_jmp.append((i2.operands[0].imm))
        #print(patched_jmp)
        func = i2.operands[0].imm#-i1.size
        continue
    elif i1.mnemonic == "jmp":
        print("Jumping to the 0x%x", i1.operands[0].imm)
        func = i1.operands[0].imm
        continue
    else:
        print("no", i1.size)
        func = func + i1.size
        print("="*100)
        continue
    size = i1.size
    elf.asm(func+size, 'jmp 0x%x' % (i2.operands[0].imm))
    print("patch ", 'jmp 0x%x' % (i2.operands[0].imm))

    print("after")
    asd = (elf.read(func, 20))
    print(disasm(asd,basesize,3))

    func = (i2.operands[0].imm)
    idx +=1
    print("="*100)
    print("="*100)
    print("="*100)
    elf.save("./rabbit.patched")