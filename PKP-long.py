import itertools
import datetime
import random
import msvcrt
from datetime import timedelta

def solve(table,N,L,W,o):
    u = 0
    d = 0
    for pair in table:
        up,down = pair
        if len(up) < len(down):
            u=u+1
        if len(down) < len(up):
            d=d+1
    if (u == u+d or d == u+d):
        return
  
    numbers = []
    for i in range(N):
        numbers.append(str(i+1))
    updict = {}
    downdict = {}
    n = 0
    a=0
    for domino in table:
        n = n+1
        updict[str(n)] = domino[0]
        downdict[str(n)] = domino[1]
    queue = ['#']
    next_queue = []
    paths = {}
    
    while queue:
        new = queue.pop(0)
        save,updown = new.split('#')
        if updown == 'down':
                  olddown=save
                  oldup = ''
                  
        elif updown == 'up':
                  olddown = ''
                  oldup=save
        else:
                oldup=''
                olddown=''

        for number in numbers:
            up = oldup + (updict[number])
            down = olddown + (downdict[number])
            if up.startswith(down) or down.startswith(up):
                
                if up == down:
                    result =  number
                    if o < len(paths):
                        while True:
                            new,r = paths[new].split('%')
                            result=r + result
                            if new=='#':
                                break
                        print()
                        print(table)
                        print(result)
                        print('len result', len(result))
                        return(result)
                
                if len(up)<len(down):
                        n = down[len(up):]+'#'+'down'
                        if n not in paths:                        
                                paths[n]= new + '%' + number
                                next_queue.append(n)

                if len(down)<len(up):
                        n = up[len(down):]+'#'+'up'
                        if n not in paths:
                                paths[n]=new+  '%' + number
                                next_queue.append(n)

            if queue == []:
                    queue = next_queue
                    next_queue = []
                    a=a+1

            if W < len(next_queue):
                print('prekrocena sirka')
                return(None)

            if a == L:
                print('prekrocena delka')
                return(None)

def k_long_words(k):
    words = []
    word = ""
    x = itertools.product(['','a','b'],repeat = k)
    for i in list(x):
        word = ''.join(i)
        if word not in words and len(word)>0: #0 pokud chci vĂ„Ä…Ă‹â€ˇechna slova 
                words.append(word)
    return(words)

def make_dominos(words):
    dominos = {}
    n=0
    for domino in itertools.product(words,repeat = 2):
        if domino[0]!=domino[1]:
            dominos[n]=domino
            n=n+1
    return(dominos)

def solve_random(K,N,W,o):
    print('long')
    print(K,N,W,o)
    a=0
    dominos = make_dominos(k_long_words(K))
    xx= datetime.datetime.now()
    xx= xx+ datetime.timedelta(minutes=0)
    yy = xx+ timedelta(minutes=720)   #pocet minut po ktery program bude hledat

    while True:
        table = []
        number = random.sample(list(dominos),N)
        for i in number:
            table.append(dominos[int(i)])
        solve(table,len(table),W,o)
        a=a+1 #pocitadlo , kolik pkp program projel
        xx= datetime.datetime.now()
        xx= xx+ datetime.timedelta(minutes=0)
        if  yy < xx:
            print(a)
            break
        if msvcrt.kbhit():
            print(a)
            break
    x = input()

def solve_all(K,N,W,o):
    dominos = make_dominos(k_long_words(K))
    D=len(dominos)
    print(D,int((3*D*D)))
    pool=[]
    table = []
    r=N
    tisk=0
    start = 0
    for d in range(D):
          pool.append(d)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    numbers = (tuple(pool[i] for i in range(N)))
    for i in numbers:
                  table.append(dominos[i])
    solve(table,len(table),W,o)
    table = []  
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        numbers = (tuple(pool[i] for i in indices))
        start = start+1
        if start > int((3*D*D)):
            for i in numbers:
                table.append(dominos[i])
            solve(table,len(table),W,o)
            tisk=tisk+1
            if tisk==1000:
                print (table,numbers)
                tisk = 0
            table = []

def solve_all_with_one_given(onegiven,K,N,W,o,delay):
    print('solve_all_with_one_given')
    dominos = make_dominos(k_long_words(K))
    D=len(dominos)
    print(onegiven,K,N,W,o,delay,D)
    pool=[]
    table = [onegiven]
    r=N
    tisk=0
    start = 0
    for d in range(D):
          pool.append(d)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    numbers = (tuple(pool[i] for i in range(N)))
    for i in numbers:
                  table.append(dominos[i])
    solve(table,len(table),W,o)
    table = [onegiven]
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
            
        numbers = (tuple(pool[i] for i in indices))
        start = start+1
        if start > delay:
            for i in numbers:
                    table.append(dominos[i])
       
            solve(table,len(table),W,o)
            tisk=tisk+1
            if tisk==10000:
                print (table,numbers)
                tisk = 0
            table = [onegiven]          

def solve_file(file,L,W,o):
    a = open(file,"r")
    tables=[]
    table=[]
    for line in a:
        if line.endswith('\n'):
            line=line[:-1]
        domino = tuple(line.split(' '))
        table.append(domino)
        if line =='':
            tables.append(table[:-1])
            table=[]
    tables.append(list(table))
    for t in tables:
        xx= datetime.datetime.now()
        N = len(t)
        r=solve(t,len(t),L,W,o)
        test(t,r)
        yy= datetime.datetime.now()
        print(yy-xx)
        print()

def test(table,result):
    verifyU = ""
    verifyL = ""
    if result == None:
        print(table)
        return
    for i in result:
        pair = table[int(i)-1]
        verifyU += pair[0]
        verifyL += pair[1]
    if verifyU =='' or verifyL =='':
        print('incorrect - words are empty')
    elif verifyU != verifyL:
        print('incorrect - upper and lower words are not equal')
        #print(verifyU)
        #print(verifyL)
    elif verifyU == verifyL:
        #print(verifyU) 
        #print(verifyL)
        print('correct')

#solve_file('file.txt',200,1200,1)
#solve_random(3,70,2,300,50)
#x=input()
#t= [('ab','abb'),('aa','ab'),('bba','aa'),('babaa','aa'),('abab','ba'),('ba','aaaab'),('baab','aaa')]
t= [('0','010101'),('10','0'),('000000','01')] #192
#t= [('a','bba'),('b','aa'),('b','abbba'),('baaa','ba'),('abb','baa'),('ababa','aaa'),('abbab','abab'),('bbaab','aaaab')]
t=[('0','010101'),('10','0'),('0000000000','01')] #560
#t =[('aa', 'ab'), ('aa', 'ba'), ('aa', 'aaa    a'), ('ababa', 'bbbb'), ('bbbbb', 'bb')]
t= [('0','010101'),('10','0'),('000000000000000000','01')] #1872
#t = [('baaaa', 'aa'), ('ba', 'aaaa'), ('aaa', 'aaaba'), ('abaaa', 'aabaa')]
#t= [('bb', 'bbbab'), ('abbb', 'bba'), ('bbbb', 'ba'), ('babb', 'bb')]
#t=[('bbabb', 'abbab'), ('bba', 'b'), ('b', 'babb'), ('bbaab', 'abab'), ('a', 'babb')]
t=[('a', 'bbab'), ('babbb', 'bab'), ('b', 'a'), ('abb', 'b'), ('bbb', 'bbba')]
t=[('aaaaa', 'aaaa'), ('b', 'abbbbb'), ('b', 'aaaaaa')]
xx= datetime.datetime.now()
#solve_file('soubor.txt',200,1500000000,1)

#r=solve(t,len(t),200,10000,1)

#r=solve(t,len(t),1000000000000,1)
solve_all_with_one_given(('abba', 'a'),7,2,4000,500,120000)

#solve_random(5,5,500000,20)
#solve_all(5,30,5,300,20)
yy= datetime.datetime.now()
#test(t,r)



print(yy-xx)
aaa= input()
          
