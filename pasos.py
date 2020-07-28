import math

tamañoDePaginas = 16 #Paginacion de 16
algoritmo = True #FIFO por Default

memory = [None] * 2048 #Area de memoria
areaSwapping = [None] * 4096 #Area de Swapping

procesosDePagina = {} #Para organizar cada procesos de pagina segun un identificador "p" y por frames

PaginasMenejoSwapp = {} #Para manejo del swap por frames

swapsTotales = 0
fallosDePaginaTotales = 0
tiempoMedida = 0
fifoSwap = []
lruSwap = []

def escojeFrameParaSwap():
    if(algoritmo): #FIFO
        frameAElegir = fifoSwap.pop()
        fifoSwap.insert(0, frameAElegir)
    else: #LRU
        frameAElegir = lruSwap.pop()
        lruSwap.insert(0, frameAElegir)
    return frameAElegir

def verSiEstaLibreEnMemoria():
    for i in range(0, 4096, tamañoDePaginas):
        if(areaSwapping[i] == None):
            return
    print("Memoria Swap Llena")
    return 0

def swap(paginaNueva, procesosNuevo, siguienteFrame):
    global tiempoMedida, fallosDePaginaTotales

    procesoAnterior, paginaAnterior = memory[siguienteFrame]

    verificadorFrameLibreEnSwap = verSiEstaLibreEnMemoria()

    if verificadorFrameLibreEnSwap == 0:
        return False
    
    print("La Pagina: ", paginaAnterior," del proceso: ",procesoAnterior," haciendo swapping al marco: ",math.floor(verificadorFrameLibreEnSwap/tamañoDePaginas), "del área de swapping")



def P(n, p): #Paso[1] = bytes a asignar, Paso[2] = proceso
    global tiempoMedida, swapsTotales, fallosDePaginaTotales
    print("Para la instruccion P asignammos: ", n, "bytes al procesos: ", p)

    if p < 0:
        print("ERROR: no puede haber procesos menores a 0")
        return
    if p in procesosDePagina:
        print("Ese procesos ya existe")
        return
    if (n <= 0 or n > 2048):
        print("ERROR: los bytes a asignar no son validos")
        return
    
    numeroPaginas = math.ceil(n / tamañoDePaginas)

    procesosDePagina[p] = {} 
    procesosDePagina[p]["tiempoInicio"] = tiempoMedida
    paginaActual = 0
    manejoDeFramesVacios = 0

    while paginaActual < numeroPaginas:
        if paginaActual < numeroPaginas and manejoDeFramesVacios >= 2048:
            siguienteFrame = escojeFrameParaSwap()
            cambio = swap(paginaActual, p, siguienteFrame)