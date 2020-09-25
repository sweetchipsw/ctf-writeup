from pwn import *
import numpy as np
import string
import json

f = open("prob.mv", "rb")
code = f.read()
f.close()

mdict = {}
user_input_str = ""
user_input_str += "\x00"*(25-len(user_input_str))
user_input = [ord(c) for c in user_input_str]
user_input_tmp = {}
user_input_tmp["x"] = 5
user_input_tmp["y"] = 5
user_input_tmp["matrix"] = np.reshape(user_input, (5, 5))
mdict[0x3e8] = user_input_tmp

idx = 0
while True:
    if (len(code) == idx):
        # If code ended
        break

    opcode = code[idx]
    idx += 1
    if opcode == 0x0:
        tmp = {}
        id = u64(code[idx:idx+8], sign="signed")
        x = u64(code[idx+8:idx+16], sign="signed")
        y = u64(code[idx+16:idx+24], sign="signed")
        tmp["x"] = x
        tmp["y"] = y
        idx += 24
        tmpcode = code[idx:idx+(8*x*y)]
        tmp["code"] = []
        matrix = [[0 for w in range(x)] for h in range(y)]
        for z in range(0, len(tmpcode), 8):
            v = u64(tmpcode[z:z+8], sign="signed")
            tmp["code"].append(v)
        idx += 8*x*y
        result = (np.reshape(tmp["code"], (x, y)))
        tmp["matrix"] = result
        if id == 0x3e8:
            # 0x3e8 has already declared. (user_input_str)
            print(("mdict[%x]=" %id), mdict[id]["matrix"])
            continue
        mdict[id] = tmp
        print(("mdict[%x]=" %id), mdict[id]["matrix"])
    elif opcode >= 1 and opcode <= 3:
        if opcode == 1:
            result = u64(code[idx:idx+8], sign="signed")
            m1 = u64(code[idx+8:idx+16], sign="signed")
            m2 = u64(code[idx+16:idx+24], sign="signed")
            m1m = mdict[m1]["matrix"]
            m2m = mdict[m2]["matrix"]
            new_matrix = m1m.dot(m2m)
            tmp = {}
            tmp["x"] = new_matrix.shape[0]
            tmp["y"] =new_matrix.shape[1]
            tmp["matrix"] = new_matrix
            mdict[result] = tmp
            print("mdict[%x] = mdict[%x].dot((mdict[%x]))" % (result, m1, m2))
        idx += 24
    elif opcode == 4:
        dst_id = u64(code[idx:idx+8], sign="signed")
        dst_x = u64(code[idx+8:idx+16], sign="signed")
        dst_y = u64(code[idx+16:idx+24], sign="signed")
        src_id = u64(code[idx+24:idx+32], sign="signed")
        src_x = u64(code[idx+32:idx+40], sign="signed")
        src_y = u64(code[idx+40:idx+48], sign="signed")
        mdict[dst_id]["matrix"][dst_x][dst_y] = mdict[src_id]["matrix"][src_x][src_y]
        tmpstr = 0
        if src_id == 0x3ec:
            tmpstr = (mdict[src_id]["matrix"][src_x][src_y])
        print('mdict[%x][%d][%d] = mdict[%x][%d][%d]'%(dst_id, dst_x, dst_y, src_id, src_x, src_y), tmpstr)
        idx += 48
    elif opcode == 5:
        id = u64(code[idx:idx+8], sign="signed")
        v = mdict[id]["matrix"][0]
        print("compare : mdict[%x][0][0] == 0" % id)
        print(v, v[0] == 0, mdict[id]["matrix"])
				print(mdict[0x3eb]) # refer Tips section
        exit(-1) # this allows to stop at first comparing operation
        idx += 16
    else:
        print("unknown opcode", opcode)
        print(hexdump(code[idx:idx+32]))
        print(opcode)
        break