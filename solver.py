#!/usr/bin/env python3
import itertools
import math
import sys

result = list()

def reverse_num(x):
    if x >= 0:    
        return int(str(x)[::-1].lstrip("0"))
    else:
        return -int(str(-x)[::-1].lstrip("0"))



def mirror_num(x):
    if x >= 0:
        return x * (10 ** len(str(x))) + reverse_num(x)
    else:
        return x * (10 ** (len(str(x)) - 1) ) + reverse_num(x)

def sum_num(x):
    if abs(x) != x:
        return x
    r = 0
    while x:
        r, x = r + x % 10, x // 10
    return r


def map_num(s,x):
    f,d = x.split("=>",2)
    return int(str(s).replace(f,d))

def shift_left_with_carry(x):
    n = x
    if x < 0:
        n = -x
    res = list(str(n))
    n = res.pop(0)
    res.append(n)
    res = int("".join(res))
    if x < 0:
        return -res
    else:
        return res

def shift_left_without_carry(x):
    res = str(x)
    res.append('0')
    return int(res)

def shift_right_with_carry(x):
    n = x
    if x < 0:
        n = -x
    res = list(str(n))
    n = res.pop()
    res.insert(0,n)
    res = int("".join(res))
    if x < 0:
        return -res
    else:
        return res

def shift_right_without_carry(x):
    res = str(x)[:-1]
    if res == "" or res == "-":
        return 0
    else:
        return int(res)

def div_num(s,x):
    if (s % int(x[1:])) == 0:
        return s // int(x[1:])
    else: 
        return s

def isInt(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

def inc_ops(x,ops):
    x = int(x[3:])
    res = list()
    for i in ops:
        if (i[0] == "+" or  i[0] == "-" or  i[0] == "x" or  i[0] == "/") and isInt(i[1:]):
            res.append(i[0] + str(int(i[1:]) + x ))
        elif isInt(i):
            res.append(str(int(i)+x))
        else:
            res.append(i)
    #print(ops)
    #print(res)
    #print("")
    return res

def inv_num(x):
    result = list(str(x))
    for i in range(len(result)):
        if result[i].isdigit():
            result[i] = str((10 - int(result[i])) % 10)

    return int("".join(result))

def portal(s,start,end):
    if len(str(s))-1 <  end:
        return s

    result = str(s)
    f = int(result[len(result)-1 - end])
    result = result[:len(result) - 1 - end] + result[len(result) - end:]
    result = str(int(result) + f * (10 ** start))
    if len(result)-1 < end:
        return int(result)
    else:
        return portal(int(result),start,end)

def router(s,x,ops):
    x = x.lower()
    res = [s,ops]
    if x.lower() == "Inv10".lower():
        res[0] = inv_num(s)
    elif x[:3] == "[+]":
        res[1] = inc_ops(x,ops)
    elif x == "SHIFT<<".lower() or x == ">>":
        res[0] =  shift_left_without_carry(s)
    elif x == "<SHIFT".lower():
        res[0] =  shift_left_with_carry(s)
    elif x == "SHIFT>>".lower() or x == "<<":
        res[0] =  shift_right_without_carry(s)
    elif x == "SHIFT>".lower():
        res[0] = shift_right_with_carry(s)
    elif "=>" in x:
        res[0] = map_num(s,x)
    elif x == "SUM".lower():
        res[0] = sum_num(s)
    elif x == "+-":
        res[0] =  -s
    elif x == "Reverse".lower():
        res[0] = reverse_num(s)
    elif x == "Mirror".lower():
        res[0] = mirror_num(s)
    elif x[0] == '/':
        res[0] = div_num(s,x)
    elif x[0] == '-':
        res[0] = s - int(x[1:])
    elif x[0] == '+':
        res[0] = s + int(x[1:])
    elif x[0] == 'x':
        res[0] = s * int(x[1:])
    else:
        res[0] = s*(10**len(str(x)))+int(x)
    return tuple(res)


def job(goal,src,tail,remaining_steps,ops,use_memory,state,memory_state,last_mem=0,p_start = 0, p_end = 100):
    #print(src,tail,remaining_steps,ops,use_memory,state,memory_state)
    for i in ops:
        n_tail = list(tail)
        n_state = list(state)
        n_src,n_ops = router(src,i,ops)
        n_src = portal(n_src,p_start,p_end)
        if n_src == goal:
            #print(memory_state)
            result.extend(tail)
            result.append(i)
            #Merge memory State
            for i in range(len(memory_state)):
                result.insert(i+memory_state[i],"Remember")

            return True
        elif remaining_steps > 0:
            n_tail.append(i)
            n_state.append(n_src)
            if job(goal,n_src,n_tail,remaining_steps - 1,n_ops,use_memory,n_state,memory_state,last_mem,p_start,p_end) == True:
                return True
    if use_memory:
        for i in range(last_mem,len(state)): #i want the next element but range works like this: [start,end) 
            n_tail = list(tail)
            
            n_memory_state = list(memory_state)
            n_memory_state.append(i)
            
            n_state = list(state)
            n_src,n_ops = router(src,str(state[i]),ops)
            n_src = portal(n_src,p_start,p_end)
            if n_src == goal:
                #print(n_memory_state)
                result.extend(n_tail)
                result.append(str(state[i]))
                
                for i in range(len(n_memory_state)):
                    result.insert(i+n_memory_state[i]-1,"Remember")
                return True
            elif remaining_steps > 0:
                n_tail.append(str(state[i]))
                n_state.append(n_src)
                if job(goal,n_src,n_tail,remaining_steps - 1,n_ops,use_memory,n_state,n_memory_state,i+1,p_start,p_end) == True:
                    return True

    return False



def  main():
    args = sys.argv[1:]
    steps = int(args[0])
    goal = int(args[1])
    source = int(args[2])
    operations = args[3:]
    use_memory = True
    try:
        operations.remove("MEM")
    except Exception:
        use_memory = False

    p_start = 0
    p_end = 100
    try:
        for i in operations:
            if i[0].lower() == 'p':
                p_start = int(i[1])
                p_end = int(i[2])
                operations.remove(i)
                break
    except:
        pass
    print(steps,goal,source,operations)
    if job(goal,source,[],steps-1,operations,use_memory,[source],[],p_start=p_start,p_end=p_end) == True:
        #reduce()
        print(result)
    exit(0)
if __name__ == "__main__":
    main()
