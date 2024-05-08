import itertools
import datetime
import random
import msvcrt
from datetime import timedelta

def k_long_words(k):
    words = []
    word = ""
    x = itertools.product(['','a','b'],repeat = k)
    for i in list(x):
        word = ''.join(i)
        if word not in words and len(word)>1: 
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


def solve(table,L,N,W,o):
    """
    L (int): Maximum allowed length for the solution string.
    N (int): Number of dominos to be used in finding a solution.
    W (int): Maximum width of the search to limit the breadth of the search tree.
    o (int): Minimum acceptable length of the result to consider it a valid solution.
    """

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
    rrr=0

    for domino in table:
        n = n+1
        updict[str(n)] = domino[0]
        downdict[str(n)] = domino[1]

    queue = ['##']
    wid = 0
    a = 0
    
    while queue:
        new = queue.pop(0)
        result,save,updown = new.split('#')

        if len(result)>L:
            break        

        if a == len(result):
            a=a+1
            rrr=rrr+wid
            wid=0
        
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
                    if up== down:
                        if len(result+number)>=o:
                            #print(table)
                            #print(result+number)
                            #print(len(result+number),wid)
                            test(table,result+number,wid)
                            #print('')
                            return(result+number,wid)
                        else:
                            return

                    if wid < W:
                        wid = wid + 1
                        if len(up)<len(down):
                            save = down[len(up):]+'#'+'down'
                            queue.append(result+number+'#'+save)
                        elif len(down)<len(up):
                            save = up[len(down):]+'#'+'up'
                            queue.append(result+number+'#'+save)
    return

def solve_without_test(table,L,N,W,o):
    numbers = []
    for i in range(N):
        numbers.append(str(i+1))
    updict = {}
    downdict = {}
    n = 0
    for domino in table:
        n = n+1
        updict[str(n)] = domino[0]
        downdict[str(n)] = domino[1]
    queue = ['##']
    up=''
    down=''
    wid = 0
    a = 0
    
    while queue:
        new = queue.pop(0)
        result,save,updown = new.split('#')

        if len(result)>L:
            print('prekrocena delka')
            return(None)
        
        if a == len(result):
            a=a+1
            wid=0
        
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
                    if up== down:
                        if len(result+number)>=o:
                            return(result+number,wid)
                        else:
                            return

                    if wid < W:
                        wid = wid +1
                        if len(up)<len(down):
                            save = down[len(up):]+'#'+'down'
                            queue.append(result+number+'#'+save)
                        elif len(down)<len(up):
                            save = up[len(down):]+'#'+'up'
                            queue.append(result+number+'#'+save)
                    if wid > W:
                        print('prekrocena sirka')
                        return(None)
    
def solve_random(K,L,N,W,o):
    """
    K (int): Maximum length of the words in any domino.
    L (int): Maximum allowed length for the solution string.
    N (int): Number of dominos to be used in finding a solution.
    W (int): Maximum width of the search to limit the breadth of the search tree.
    o (int): Minimum acceptable length of the result to consider it a valid solution.
    """
    print('nochain')
    print(K,L,N,W,o)
    dominos = make_dominos(k_long_words(K))
    a=0
    xx= datetime.datetime.now()
    xx= xx+ datetime.timedelta(minutes=0)
    yy = xx+ timedelta(minutes=1)   #pocet minut po ktery program bude hledat
    print(yy)
    while True:
        table = []
        number = random.sample(list(dominos),N)
        for i in number:
            table.append(dominos[int(i)])
        solve(table,L,len(table),W,o)
        a=a+1 #pocitadlo , kolik pkp program projel
        xx= datetime.datetime.now()
        xx= xx+ datetime.timedelta(minutes=0)
        if  yy < xx:
            print(a)
            break
        if msvcrt.kbhit():
            print(a)
    x = input()

def solve_all_with_one_given(onegiven,K,L,N,W,o,delay):
    print('solve_all_with_one_given')
    dominos = make_dominos(k_long_words(K))
    D=len(dominos)
    print(K,L,N,W,o)
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
    solve(table,L,N,W,o)
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
       
            solve(table,L,N,W,o)
            tisk=tisk+1
            if tisk==10000:
                print (table,numbers)
                tisk = 0
            table = [onegiven]          
  
def solve_all(K,L,N,W,o):
    """
    K (int): Maximum length of the words in any domino.
    L (int): Maximum allowed length for the solution string.
    N (int): Number of dominos to be used in finding a solution.
    W (int): Maximum width of the search to limit the breadth of the search tree.
    o (int): Minimum acceptable length of the result to consider it a valid solution.
    """
    dominos = make_dominos(k_long_words(K))
    D=len(dominos)
    pool=[]
    table = []
    r=N
    tisk=0
    for d in range(D):
          pool.append(d)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    numbers = (tuple(pool[i] for i in range(N)))
    for i in numbers:
                  table.append(dominos[i])
    solve(table,L,len(table),W,o)
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
        for i in numbers:
            table.append(dominos[i])
        solve(table,L,len(table),W,o)
        tisk=tisk+1
        if tisk==D:
            print (table,numbers)
            tisk = 0
        table = []          

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
        r=solve(t,L,len(t),W,o)
        yy= datetime.datetime.now()
        print(yy-xx)
        print()


def test(table,result,wid):
    if result==None:
        return
    #notin = []
    #for i in range(len(table)):
       #     if str(i+1) not in result:    #smaze nevyuzite dvojice
      #          notin.insert(0,i)
    #for i in notin:
      #      del table[i]

    #print(result)
    
    #if result == 'no' or result== None:
     #   print(table)
    #    return

    #result,wid = solve_without_test(table,500,len(table),10000,1) #kontrola s vyssi sirkou, jeste je potreba upravit

    verifyU = ""
    verifyL = ""
    for i in result:
        pair = table[int(i)-1]
        verifyU += pair[0]
        verifyL += pair[1]

    if verifyU != verifyL:
        print('incorrect - upper and lower words are not equal')
        print(result)
        print(table)
        return
    elif verifyU =='':
        print('incorrect - words are empty')
        return
    elif verifyU == verifyL:
            #print(verifyU) #tato verze bez tohoto nevytiskne slova
            #print(verifyL)
            print(table)
            print(result)
            print('len_result', len(result))
            print('correct')
            return
            
#solve_file('file.txt',200,1200,1)
#solve_random(3,70,2,300,50)
#x=input()

#list of tables that are solvable      
#t= [('ab','abb'),('aa','ab'),('bba','aa'),('babaa','aa'),('abab','ba'),('ba','aaaab'),('baab','aaa')]
#t= [('0','010101'),('10','0'),('000000','01')] #with leght of 192
#t= [('a','bba'),('b','aa'),('b','abbba'),('baaa','ba'),('abb','baa'),('ababa','aaa'),('abbab','abab'),('bbaab','aaaab')]
#t =  [('babb', 'babab'), ('babab', 'ab'), ('ba', 'bbaba'), ('aba', 'bbbba'), ('baba', 'bab')]
#t= [('0','010101'),('10','0'),('0000000000','01')] #with leght of 560
#t= [('bbbb', 'aabba'), ('bb', 'aaa'), ('bbbbb', 'bbbaa'), ('bbaaa', 'bb'), ('a', 'bbaaa')]
#t=[('a', 'bba'), ('b', 'aa'), ('b', 'abbba'), ('baaa', 'ba'), ('abb', 'baa'), ('ababa', 'aaa'), ('abbab', 'abab'), ('bbaab', 'aaaab')]
#t = [('aaaaa', 'bbb'), ('aa', 'aaaaa'), ('bbbb', 'bb'), ('bbaa', 'bab'), ('babb', 'babab')]
#t = [('bbab', 'bbbab'), ('bb', 'bbbba'), ('bbabb', 'ba'), ('babb', 'bb')] 
#t=[('baaaa', 'aa'), ('ba', 'aaaa'), ('aaa', 'aaaba'), ('abaaa', 'aabaa')] 
#t =[('bb', 'aaa'), ('bbaaa', 'bb'), ('bbab', 'bbabb'), ('baba', 'bbbb'),('b','bbbb')]
#t =[('aabbb', 'abbbb'), ('baaaa', 'aa'), ('bbbab', 'aab'), ('abaab', 'abb'), ('bb', 'bbb'), ('bbb', 'ba'), ('bbab', 'aaaaa')]
#t= [('a', 'abb'), ('b', 'a'), ('abbaaa', 'a')]
t=[('aabaaa', 'bbbbbb'), ('bbbbb', 'bbbb'), ('a', 'aabaaa'), ('ab', 'aaaaa')]
#t =[('bb', 'aaa'), ('bbaaa', 'bb'), ('bbab', 'bbabb'), ('baba', 'bbbb'),('b','bbbb')]
#t=[('a', 'bbab'), ('babbb', 'bab'), ('b', 'a'), ('abb', 'b'), ('bbb', 'bbba')]

xx= datetime.datetime.now()
#r,w=solve(t,300,len(t),300000,1)
#solve_file('puvodnisoubor.txt',300,50000,1)
#solve_all(5,70,5,150,40)
#solve_all(5,30,5,300,20)
#r,w=solve(t,3000,len(t),300,1)

#solve_all_with_one_given(('ababab', 'a'),7,100,2,20000,20,120000)

#solve_random(5,40,5,2000,30)

solve_random(9,300,3,1000,30)
#delka slov, max delka resení, pocet slov, max sikra,min delka resení


yy= datetime.datetime.now()
print(yy-xx)
#test(t,r,w)

aaa= input()
          
