import re
from random import randint
from classes.slot import Slot
import os
from colorama import Fore, Back, Style

# extrai os numeros e as letras da palavra
def extractTipsNumber(word):
    list = []
    list.append(int(re.sub('[^0-9]', '', word)))
    list.append("".join(re.findall("[a-zA-Z]+", word)).upper())
    return list

# me diz o mapeamento utilizado
def tipeMapeamento(lista):
    slots = extractTipsNumber(lista[1])
    conjuntos = extractTipsNumber(lista[2])
    if(slots[0]==conjuntos[0] and slots[1]==conjuntos[1]):
        print(Fore.BLUE+Back.BLACK+Style.DIM+ ">> MAPEAMENTO TOTALMENTE ASSOCIATIVO <<" +Style.RESET_ALL)
        print("\n")
        return 1
    elif (conjuntos[0]==1 and conjuntos[1]==''):
        print(Fore.BLUE+Back.BLACK+Style.DIM+" >> MAPEAMENTO DIRETO << "+Style.RESET_ALL)
        print("\n")
        return 2
    else:
        print(Fore.BLUE+Back.BLACK+Style.DIM+" >> MAPEAMENTO ASSOCIATIVO POR CONJUNTOS << " + Style.RESET_ALL)
        print("\n")
        return 3

# função mestre do codigo
def validaResp(resp):

    lista = resp.split(',')
    lista = [word.lstrip().rstrip() for word in lista]
    if (len(lista)!=4):
        print('ENTRADA INVALIDA')
        return False
    bits = [0 for x in lista]
    tipe = tipeMapeamento(lista)
    bits[0] = sepByte(lista[0])
    bits[3] = countBity(4 * int(lista[3]))
    totalPalPorSlot = 1
    totalSlots = pow(2, sepByte(lista[1]))
    if tipe == 1:
        bits[1] = 0
        bits[2] = 0
    elif tipe ==2:
        bits[1] = sepByte(lista[1],mp=bits[0]+1)
        bits[2] = extractTipsNumber(lista[2])[0]
    elif (tipe ==3):
        bits[1] = sepByte(lista[1], mp=bits[0]) # Quantidade de bits para endereçar toda a cache
        bits[1] = pow(2,bits[1]) # Quantidade de linhas na cache

        bits[2] = sepByte(lista[2],mp=bits[0]) # Quantidade de bits para endereçar cada slot da cache
        bits[2] = pow(2,bits[2])
        if(bits[2]>bits[1]):
            print("Você não pode ter mais conjuntos do que linhas na Cache!")
            return False
        bits[1] = countBity(bits[1]/bits[2]) # Todas as linhas da cache dividida pelas quantidades de conjuntos
        totalSlots = pow(2,bits[1])
    indice = bits[1]
    enByte = bits[3]
    tag = bits[0] - (indice + enByte)
    if(tag<=0):
        print("SUA CACHE É MUITO GRANDE, IMPOSSÍVEL DE SER FEITO ESTE CÁLCULO")
        exit()
    return [tag,indice,enByte,bits[0],tipe , totalPalPorSlot, totalSlots]


# Função que conta quantos bits serão nescessários
def countBity(byte , max=0):
    if (max==0):
        max = 64
    for i in range(1,max):
        if(byte<=pow(2,i)):
            return i


# Função que conta quanta memoria há na palavra

def sepByte(resp,mp=0):
    resp = extractTipsNumber(resp)
    if('GB'in resp[1]):
        bity = resp[0]
        bity = bity*pow(2,30)
        bit = countBity(bity, max=mp)
    elif('MB' in resp[1]):
        bity = resp[0]
        bity = bity * pow(2, 20)
        bit = countBity(bity, max=mp)
    elif('KB' in resp[1]):
        bity = resp[0]
        bity = bity * pow(2, 10)
        bit = countBity(bity, max=mp)
    elif('K' in resp[1]):
        bity = resp[0]
        bity = bity * 1024
        bit = countBity(bity, max=mp)
    else:
        bity = resp[0]
        bit = countBity(bity, max=mp)
    return bit

# Função que printa a quantidade de bits usada para cada função
def printBits(bits):
    print(' Tamanho em Bits: \n')
    print(Fore.YELLOW+' TAG| ',end='')
    print(Fore.BLUE+'IND| ',end='')
    print(Fore.RED + 'END.BYTE| ', end='')
    print(Fore.GREEN + 'MP' + Style.RESET_ALL)
    print("+----------------------+")
    print("|  %d  |  %d  |  %d  |  %d |"%(bits[0], bits[1], bits[2],bits[3]))
    print("+----------------------+\n")

# Gera um numero aleatorio
def randomAddress(limit):
    return (randint(1,pow(2 ,limit )))

# Gera um numero binario aleatorio
def randomBinary(total):
    binary = ''
    for i in range(total):
        binary = binary+str(randint(0,1))
    return binary

# Função que separa os bits e suas necessidades
def sepAddres(address, mp, bits, random=1):
    binAddress = str(bin(address))[2:]
    if(random):
        binAddress = randomBinary(mp - len(binAddress))+binAddress
    else:
        for i in range(mp-len(binAddress)):
            binAddress = '0'+binAddress
    t = binAddress[0:bits[0]]
    i = binAddress[bits[0]:(len(binAddress)) - bits[2]]
    e = binAddress[(len(binAddress)) - bits[2]:len(binAddress)]
    return [t, i, e, binAddress]

# Gera um endereço aleatorio em decimal, separa e retorna os enderecos gerados.
def generateAddress(mp,bits,show=False):

    endereco = randomAddress(mp)
    binAddres = sepAddres(endereco , mp , bits)
    if(show):
        printaEnderecosGerados(endereco,binAddres[0],binAddres[1],binAddres[2],binAddres[3])
    return binAddres

# Printa endereços
def printaEnderecosGerados(endereco,t,i,e,binAddres):
    print("----------------------------------------")
    print("[ENDEREÇO GERADO : %d ] b₁₀" % endereco)
    print("[ENDEREÇO GERADO : %02x] b₁₆".upper() % endereco)
    print("[ENDEREÇO GERADO : %d ] b₂" % int(binAddres, 10))
    print("----------------------------------------\n")
    print("-------------------")
    print(Fore.BLUE+Back.BLACK+Style.DIM+" >> MAPEAMENTO DECIMAL << " + Style.RESET_ALL)
    print(Fore.YELLOW+ ' TAG| ', end='')
    print(Fore.BLUE + 'IND| ', end='')
    print(Fore.RED + 'END.BYTE ' + Style.RESET_ALL)
    print("%d | %d | %d" % (int(t, base=2), int(i, base=2), int(e, base=2)))
    print("-------------------\n ")
    print("-------------------")
    print(Fore.BLUE+Back.BLACK+Style.DIM+ " >> MAPEAMENTO HEXA << " + Style.RESET_ALL)
    print(Fore.YELLOW+ ' TAG| ', end='')
    print(Fore.BLUE + 'IND| ', end='')
    print(Fore.RED + 'END.BYTE ' + Style.RESET_ALL)
    print("%s | %s | %s" % (
    hex(int(t, base=2))[2:].upper(), hex(int(i, base=2))[2:].upper(), hex(int(e, base=2))[2:].upper()))
    print("-------------------\n ")
    print("-------------------")
    print(Fore.BLUE+Back.BLACK+Style.DIM+" >> MAPEAMENTO EM BINARIO << " + Style.RESET_ALL)
    print(Fore.YELLOW+ ' TAG| ', end='')
    print(Fore.BLUE + 'IND| ', end='')
    print(Fore.RED + 'END.BYTE ' + Style.RESET_ALL)
    print("%s | %s | %s" % (t, i, e))
    print("-------------------\n ")

# Altera o indice do endereco enviado, e altera a tag, caso o sorteio gere 1;
def forceColision(address ,cache,tipe):
    # Caso especial para mapeamento associativo por conjunto
    if (tipe == 3):
        keys = cache[randint(0,len(cache)-1)]
        address.alterIndice(keys.indice)
        address.alterTag(keys.tag)
        return address

    keys = list(cache.keys())
    indice = keys[randint(0, len(keys) - 1)]
    address.alterIndice(indice)
    sort = [1, 0, 1, 0, 1, 0,1 ,1, 1]
    if(sort[randint(0,8)]):
        address.alterTag(cache[indice].tag)
    return address

# Função que limpa a tela
def limp():
    os.system('cls' if os.name == 'nt' else 'clear')
def transformEnderecos(enderecos):
    enderecos = enderecos.split(',')
    enderecos = [ i.lstrip().rstrip() for i in enderecos]
    enderecos = [int(i) for i in enderecos]
    return enderecos

def preenceCacheFullAssociative(cache , bits , enderecos):
    hit = 0
    miss = 0
    cache['0'] = []
    x = 0
    for address in enderecos:
        print(Fore.RED+Back.BLACK+ " >> ESTADO DA CACHE << " +Style.RESET_ALL)
        printaCache(cache, bits[4])
        if (x):
            hitRate = ((hit / x) * 100)
            print("| hits = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (
            hit, miss, len(cache['0']), hitRate))
        input("\n\nTECLE QUALQUER TECLA PARA CONTINUAR\n\n")
        limp()
        address = sepAddres(address,bits[3],bits,random=0)
        end = Slot('x', address[0], address[2])
        flag = 0
        if (not cache['0']):
            cache['0'].insert(0, end)
            print(Fore.RED+Back.BLACK+ "MISS CACHE VAZIA" + Style.RESET_ALL)
            print('INSERINDO ENDEREÇO COM A TAG >> %s\n' % end.getTag())
            miss += 1
            x+=1
            continue
        for address in cache['0']:
            if (end.tag == address.tag):
                print(Fore.GREEN+Back.BLACK+ 'HIT : ' + Style.RESET_ALL,end='')
                print("DA TAG >>> %s\n" % end.getTag())
                hit += 1
                flag = 1
                break
        if (flag):
            x+=1
            continue
        print(Fore.RED+Back.BLACK+ "MISS: " + Style.RESET_ALL,end='')
        print("VALOR DE TAG >> %s << NÂO ENCONTRADO NA CACHE, ESTÁ SENDO INSERIDO!\n" % (end.getTag()))
        miss += 1
        if (len(cache['0']) == bits[6]):
            print(Fore.RED+Back.BLACK+ "MISS MEMORIA LOTADA: " +Style.RESET_ALL)
            print("ENDEREÇO COM TAG >> %s << SENDO REMOVIDO!\n" % cache['0'].pop().getTag())
        cache['0'].insert(0, end)
        x+=1
    limp()
    try:
        print("| hits = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (hit, miss, len(cache), ((hit / x) * 100)))
    except ZeroDivisionError:
        print("| hits = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (hit, miss, len(cache), 0))
    print("\n\n"+Fore.RED+Back.BLACK+ " >> ESTADO FINAL DA CACHE << " + Style.RESET_ALL)
    printaCache(cache, bits[4])
    input("FIM DA INTERAÇÃO, COMEÇE NOVAMENTE")
    print("\n\n")
    return cache

# Função que preenche uma memoria de mapeamento direto

def preenceCacheMapDirect(cache , bits , enderecos):
    hit = 0
    miss = 0
    print(bits)
    x = 0
    for address in enderecos:
        print(Fore.RED + Back.BLACK + " >> ESTADO DA CACHE << " + Style.RESET_ALL)
        printaCache( cache, bits[4])
        if (x):
            hitRate = ((hit / x) * 100)
            print("| hits = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (hit, miss, len(cache), hitRate))
        input("\n\nTECLE QUALQUER TECLA PARA CONTINUAR\n\n")
        limp()
        address = sepAddres(address,bits[3],bits,random=0)
        end = Slot(address[1],address[0],address[2])
        if(not cache):
            print(Fore.RED+Back.BLACK+"MISS CACHE VAZIA"+Style.RESET_ALL)
            print("INSERINDO O ENDEREÇO DE TAG> %s INDICE> %s"%(end.getTag(),end.getInd()))
            cache[end.indice] = end
            miss+=1
            x+=1
            continue
        try:
            if(cache[end.indice].tag == end.tag):
                hit+=1
                print(Fore.GREEN+Back.BLACK+ 'HIT : ' + Style.RESET_ALL, end='')
                print(': COM A TAG >> %s'%end.getTag())
                x+=1
                continue
            else:
                print(Fore.RED+Back.BLACK+ "MISS" + Style.RESET_ALL,end=' ')
                print(":CONCORRÊNCIA REMOVENDO O ENDEREÇO DE TAG> %s COM INDICE> %s" % (cache[end.indice].getTag(), end.getInd()))
                miss += 1
                cache[end.indice] = end
        except KeyError:
            print(Fore.RED+Back.BLACK+ "MISS" +Style.RESET_ALL,end=' ')
            print(":BIT DE VALIDADE, INSERINDO O ENDEREÇO DE TAG> %s INDICE> %s" % (end.getTag(), end.getInd()))
            miss += 1
            cache[end.indice] = end
        x+=1
    limp()
    try:
        print("| hits = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (hit, miss, len(cache), ((hit / x) * 100)))
    except ZeroDivisionError:
        print("| hits = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (hit, miss, len(cache), 0))
    print("\n\n"+Fore.RED+Back.BLACK+ " >> ESTADO FINAL DA CACHE << " + Style.RESET_ALL)
    printaCache(cache , bits[4])
    input("FIM DA INTERAÇÃO, COMEÇE NOVAMENTE")
    print("\n\n")
    return cache

# Função que preenche uma memoria Associativa por conjuntos
def preecheCacheMapAssociativeConjunt(cache , bits , enderecos):
    hit = 0
    miss = 0
    x = 0

    totalSlots = bits[6]
    for address in enderecos:
        flag = 0
        print(Fore.RED + Back.BLACK + " >> ESTADO DA CACHE << " + Style.RESET_ALL)
        printaCache(cache, bits[4])
        if (x):
            hitRate = ((hit / x) * 100)
            print("| hit = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (hit, miss, len(cache), hitRate))
        input("\n\nTECLE QUALQUER TECLA PARA CONTINUAR\n\n")
        limp()
        address = sepAddres(address,bits[3],bits,random=0)
        end = Slot(address[1] ,address[0] ,address[2]  )
        if (not cache):
            print(Fore.RED+Back.BLACK+ "MISS CACHE VAZIA" + Style.RESET_ALL,end='')
            print('ENDEÇO COM A TAG >> %s << SENDO INSERIDA' % end.getTag())
            cache[end.indice] = []
            cache[end.indice].insert(0, end)
            miss+=1
            input("\n\nTECLE QUALQUER TECLA PARA CONTINUAR\n\n")
            x+=1
            continue
        try:
            for slot in cache[end.indice]:
                if (slot.tag == end.tag):
                    hit += 1
                    flag = 1
                    break
            if(flag):
                continue

            if (len(cache[end.indice]) == totalSlots):
                print(Fore.RED+Back.BLACK+ "MISS :" + Style.RESET_ALL, end='')
                print('VALOR DE TAG %s NÃO ENCONTRADO NO INDICE %s' % (end.getTag(), end.getInd()))
                print('SLOT CHEIO TAG >> %s << ESTÁ SENDO REMOVIDO' % cache[end.indice].pop().getTag())

                cache[end.indice].insert(0,end)
                miss +=1
                x+=1
                continue
            else:
                print(Fore.RED+Back.BLACK+"MISS :" + Style.RESET_ALL, end='')
                print("VALOR DE TAG >> %s NÂO ENCONTRADO NO INDICE %s"%(end.getTag(),end.getInd()))
                cache[end.indice].insert(0,end)
        except KeyError:
            print(Fore.RED+Back.BLACK+ "MISS :" +Style.RESET_ALL , end='')
            print("BIT DE VALIDADE. INDICE %s SENDO INICIALIZADO COM A TAG %s"%(end.getInd(),end.getTag()))
            cache[end.indice] = []
            cache[end.indice].insert(0,end)
        x += 1
    limp()
    try:
        print("| hits = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (hit, miss, len(cache), ((hit / x) * 100)))
    except ZeroDivisionError:
        print("| hits = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (hit, miss, len(cache), 0))
    print("\n\n"+Fore.RED+Back.BLACK+ " >> ESTADO FINAL DA CACHE << " + Style.RESET_ALL)
    printaCache(cache, bits[4])
    input("FIM DA INTERAÇÃO, COMEÇE NOVAMENTE")
    print("\n\n")
    return cache



# Função que preenche uma memoria Full Associativa

def randomPreenceCacheFullAssociative(cache , bits , times):
    hit = 0
    miss = 0
    cache['0'] = []
    for i in range(times):
        print(Fore.RED+Back.BLACK+ " >> ESTADO DA CACHE << " +Style.RESET_ALL)
        printaCache(cache, bits[4])
        if (i):
            hitRate = ((hit / i) * 100)
            print("| hits = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (
            hit, miss, len(cache['0']), hitRate))
        input("\n\nTECLE QUALQUER TECLA PARA CONTINUAR\n\n")
        limp()
        address = generateAddress(bits[3], bits, show=False)
        end = Slot('x', address[0], address[2])
        flag = 0
        if (not cache['0']):
            cache['0'].insert(0, end)
            print(Fore.RED+Back.BLACK+ "MISS CACHE VAZIA" + Style.RESET_ALL)
            print('INSERINDO ENDEREÇO COM A TAG >> %s\n' % end.getTag())
            miss += 1
            continue
        # Força o hit
        if (randint(0, 1)):

            end.tag = cache['0'][randint(0, len(cache['0']) - 1)].tag
            hit += 1
            print(Fore.GREEN+Back.BLACK+"HIT DA TAG >>> %s\n"%(end.getTag())+Style.RESET_ALL)
            continue
        for address in cache['0']:
            if (end.tag == address.tag):
                print(Fore.GREEN+Back.BLACK+ 'HIT : ' + Style.RESET_ALL,end='')
                print("DA TAG >>> %s\n" % end.getTag())
                hit += 1
                flag = 1
                break
        if (flag):
            continue
        print(Fore.RED+Back.BLACK+ "MISS: " + Style.RESET_ALL,end='')
        print("VALOR DE TAG >> %s << NÂO ENCONTRADO NA CACHE, ESTÁ SENDO INSERIDO!\n" % (end.getTag()))
        miss += 1
        if (len(cache['0']) == bits[6]):
            print(Fore.RED+Back.BLACK+ "MISS MEMORIA LOTADA: " +Style.RESET_ALL)
            print("ENDEREÇO COM TAG >> %s << SENDO REMOVIDO!\n" % cache['0'].pop().getTag())
        cache['0'].insert(0, end)

    limp()
    try:
        print("| hits = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (hit, miss, len(cache['0']), ((hit / i) * 100)))
    except ZeroDivisionError:
        print("| hits = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (hit, miss, len(cache['0']), 0))
    print("\n\n"+Fore.RED+Back.BLACK+ " >> ESTADO FINAL DA CACHE << " + Style.RESET_ALL)
    printaCache(cache, bits[4])
    input("FIM DA INTERAÇÃO, COMEÇE NOVAMENTE")
    print("\n\n")
    return cache

# Função que preenche uma memoria de mapeamento direto

def randomPreenceCacheMapDirect(cache , bits , times):
    hit = 0
    miss = 0
    print(bits)
    for i in range(times):
        print(Fore.RED + Back.BLACK + " >> ESTADO DA CACHE << " + Style.RESET_ALL)
        printaCache( cache, bits[4])
        if (i):
            hitRate = ((hit / i) * 100)
            print("| hits = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (hit, miss, len(cache), hitRate))
        input("\n\nTECLE QUALQUER TECLA PARA CONTINUAR\n\n")
        limp()
        address = generateAddress(bits[3],bits, show=False)
        end = Slot(address[1],address[0],address[2])
        if(not cache):
            print(Fore.RED+Back.BLACK+"MISS CACHE VAZIA"+Style.RESET_ALL)
            print("INSERINDO O ENDEREÇO DE TAG> %s INDICE> %s"%(end.getTag(),end.getInd()))
            cache[end.indice] = end
            miss+=1
            continue
        if(randint(0,1)):
            end = forceColision(end , cache , bits[4])
        try:
            if(cache[end.indice].tag == end.tag):
                hit+=1
                print(Fore.GREEN+Back.BLACK+ 'HIT : ' + Style.RESET_ALL, end='')
                print(': COM A TAG >> %s'%end.getTag())
                continue
            else:
                print(Fore.RED+Back.BLACK+ "MISS" + Style.RESET_ALL,end=' ')
                print(":CONCORRÊNCIA REMOVENDO O ENDEREÇO DE TAG> %s COM INDICE> %s" % (cache[end.indice].getTag(), end.getInd()))
                miss += 1
                cache[end.indice] = end
        except KeyError:
            print(Fore.RED+Back.BLACK+ "MISS" +Style.RESET_ALL,end=' ')
            print(":BIT DE VALIDADE, INSERINDO O ENDEREÇO DE TAG> %s INDICE> %s" % (end.getTag(), end.getInd()))
            miss += 1
            cache[end.indice] = end
    limp()
    # Caso especial, para se não houver nenhum hit!
    try:
        print("| hits = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (hit, miss, len(cache), ((hit / i) * 100)))
    except ZeroDivisionError:
        print("| hits = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (hit, miss, len(cache), 0))

    print("\n\n"+Fore.RED+Back.BLACK+ " >> ESTADO FINAL DA CACHE << " + Style.RESET_ALL)
    printaCache(cache , bits[4])
    input("FIM DA INTERAÇÃO, COMEÇE NOVAMENTE")
    print("\n\n")
    return cache

# Função que preenche uma memoria Associativa por conjuntos
def randomPreecheCacheMapAssociativeConjunt(cache , bits , times):
    hit = 0
    miss = 0
    x = 0
    totalSlots = bits[6]
    for i in range(times):
        print(Fore.RED + Back.BLACK + " >> ESTADO DA CACHE << " + Style.RESET_ALL)
        printaCache(cache, bits[4])
        if (i):
            hitRate = ((hit / i) * 100)
            print("| hit = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (hit, miss, len(cache), hitRate))
        input("\n\nTECLE QUALQUER TECLA PARA CONTINUAR\n\n")
        limp()
        address = generateAddress(bits[3], bits, show=False)
        end = Slot(address[1] ,address[0] ,address[2]  )
        flag = 0
        if (not cache):
            print(Fore.RED+Back.BLACK+ "MISS CACHE VAZIA" + Style.RESET_ALL,end='')
            print('ENDEÇO COM A TAG >> %s << SENDO INSERIDA' % end.getTag())
            cache[end.indice] = []
            cache[end.indice].insert(0, end)
            miss+=1
            input("\n\nTECLE QUALQUER TECLA PARA CONTINUAR\n\n")
            continue
        try:
            if (randint(0, 1)):
                end = forceColision(end, cache[end.indice], bits[4])
                for slot in cache[end.indice]:
                    if (slot.tag == end.tag):
                        hit += 1
                        flag = 1
                        break
            if (flag):
                print(Fore.GREEN+Back.BLACK+'HIT : '+Style.RESET_ALL,end='')
                print("TAG: %s"%end.getTag())
                continue

            if (len(cache[end.indice]) == totalSlots):
                print(Fore.RED+Back.BLACK+ "MISS :" + Style.RESET_ALL, end='')
                print('VALOR DE TAG %s NÃO ENCONTRADO NO INDICE %s' % (end.getTag(), end.getInd()))
                print('SLOT CHEIO TAG >> %s << ESTÁ SENDO REMOVIDO' % cache[end.indice].pop().getTag())

                cache[end.indice].insert(0,end)
                miss +=1
                x+=1
                continue
            else:
                print(Fore.RED+Back.BLACK+"MISS :" + Style.RESET_ALL, end='')
                print("VALOR DE TAG >> %s NÂO ENCONTRADO NO INDICE %s"%(end.getTag(),end.getInd()))
                cache[end.indice].insert(0,end)
        except KeyError:
            print(Fore.RED+Back.BLACK+ "MISS :" +Style.RESET_ALL , end='')
            print("BIT DE VALIDADE. INDICE %s SENDO INICIALIZADO COM A TAG %s"%(end.getInd(),end.getTag()))
            cache[end.indice] = []
            cache[end.indice].insert(0,end)

    limp()
    try:
        print("| hit = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (hit, miss, len(cache), ((hit / i) * 100)))
    except ZeroDivisionError:
        print("| hit = %d, miss=%d ,  total slots preenchidos = %d , hit rate = %d%% |" % (hit, miss, len(cache), 0))
    print("\n\n"+Fore.RED+Back.BLACK+ " >> ESTADO FINAL DA CACHE << " + Style.RESET_ALL)
    printaCache(cache, bits[4])
    input("FIM DA INTERAÇÃO, COMEÇE NOVAMENTE")
    print("\n\n")
    return cache

# Função que decide qual será o mapeamento utilizado e redreciona
def preencheCache(bits , times=0 , modo='R', addresses=[]):

    cache = {}
    # Verifica o tipo de mapeamento;
    if(bits[4]==1):
        if (modo=='R'):
            print("Inserindo %d memórias aleatórias na cache\n" % times)
            cache = randomPreenceCacheFullAssociative(cache , bits, times)
        else:
            cache = preenceCacheFullAssociative(cache , bits, addresses)
    elif(bits[4]==2):
        if(modo=="R"):
            print("Inserindo %d memórias aleatórias na cache\n" % times)
            cache = randomPreenceCacheMapDirect(cache, bits, times)
        else:
            cache = preenceCacheMapDirect(cache , bits, addresses)
    else:
        if(modo=='R'):
            print("Inserindo %d memórias aleatórias na cache\n" % times)
            cache = randomPreecheCacheMapAssociativeConjunt(cache, bits, times)
        else:
            cache = preecheCacheMapAssociativeConjunt(cache , bits,addresses)

    return cache

# Função que printa o estado da cache
def printaCache(cache , tipe):
    print("INDICE | TAG | END.B")
    if(tipe==1):
        if(len(cache['0'])==0):
            print("-------------------")
            print("-------------------")
            print("-------------------")
            return
        for i in cache['0']:
            i.printSlot()
    elif(tipe==2):
        if(len(cache) == 0):
            print("-------------------")
            print("-------------------")
            print("-------------------")
            return
        for indice in cache:
            cache[indice].printSlot()
    else:
        if (len(cache) == 0):
            print("-------------------")
            print("-------------------")
            print("-------------------")
            return
        print("Blocos ocupados na cache\n")
        for indice in cache:
            print('------------------------------------------')
            print("INDICE: %02x".upper() %int(indice,2))
            for adress in cache[indice]:
                print("TAG> %s , END.BYTE> %s"%(adress.getTag(),adress.getEndB()))
            print("\nBLOCOS OCUPADOS POR ESTE INDICE: %d\n" % len(cache[indice]))
            print('------------------------------------------')


# Main function
def main():
    print("Informe sequencialmente:")
    print('<TAM-MP>, <N°SLOTS-CACHE> , <N°SLOTS-CONJUNTO> , <N°WORDS-SLOT>')
    aswer = input("Informe, corretamente os campos: ")


    bits = validaResp(aswer)
    if (not bits):
        print('Você forneceu dados ERRADOS!')
    else:
        printBits(bits)
        modo = input("Você deseja fazer inserir os endereços?<i> ou sortealos <r>: ")
        modo = modo.upper()
        if(modo!='R'):
            enderecos = input("DIGITE OS ENDECOS DE FORMA DECIMAL: ")
            enderecos = transformEnderecos(enderecos)
            cache = preencheCache(bits, modo=modo, addresses=enderecos)
        else:
            times = input("Quantos valores deseja adcionar na memória?")
            try:
                times = extractTipsNumber(times)[0]
            except ValueError:
                print("É NECESSÁRIO QUE VOCÊ DIGITE UMA QUANTIDADE DECIMAL VALIDA!")
            if (not times):
                exit()
            cache = preencheCache(bits, times)

