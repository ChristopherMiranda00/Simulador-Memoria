import math

tamañoDePaginas = 16 #Paginacion de 16
algoritmo = True #FIFO por Default

memory = [None] * 2048 #Area de memoria
areaSwapping = [None] * 4096 #Area de Swapping

procesosDePagina = {} #Para organizar cada procesos de pagina segun un identificador "p" y por frames

paginasManejoSwap = {} #Para manejo del swap por frames

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

    cargarPaginaSwap(verificadorFrameLibreEnSwap, procesoAnterior, paginaAnterior)

    if procesoAnterior not in paginasManejoSwap:
        paginasManejoSwap[procesoAnterior] = {}

    paginasManejoSwap[procesoAnterior][paginaAnterior] = verificadorFrameLibreEnSwap

    del paginasManejoSwap[procesoAnterior][paginaAnterior]

    cargarPaginaFrame(siguienteFrame, procesosNuevo, paginaNueva)
    paginasManejoSwap[procesosNuevo][paginaNueva] = siguienteFrame
    tiempoMedida += 20

    return True

def cargarPaginaSwap(frameLibre, procesoAnterior, paginaAnterior):
    val = None if procesoAnterior == None and paginaAnterior == None else [procesoAnterior,paginaAnterior]

    for i in range(0, 16):
        areaSwapping[frameLibre + i] = val

def cargarPaginaFrame(pagina, procesosNuevo, paginaNueva):
    val = None if procesosNuevo == None and paginaNueva == None else [procesosNuevo, paginaNueva]
    for i in range(0, 16):
        memory[pagina + i] = val

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
    frames = []

    while paginaActual < numeroPaginas:
        if paginaActual < numeroPaginas and manejoDeFramesVacios >= 2048:
            siguienteFrame = escojeFrameParaSwap()
            cambio = swap(paginaActual, p, siguienteFrame)

            if not cambio:
                return
            
            frames.append(math.floor(siguienteFrame/16))
            swapsTotales += 1
            paginaActual += 1

    while manejoDeFramesVacios < 2048:
        if memory[manejoDeFramesVacios] == None:
            frames.append(math.floor(manejoDeFramesVacios/16))
            procesosDePagina[p][paginaActual] = manejoDeFramesVacios
            if algoritmo:
                fifoSwap.insert(0, siguienteFrame)
            else:
                lruSwap.insert(0, siguienteFrame)
            cargarPaginaFrame(manejoDeFramesVacios, p, paginaActual)
            tiempoMedida += 10
            paginaActual += 1
            break
        manejoDeFramesVacios += 16
    print("Marcos de pagina: ", frames,"al proceso: ",p)

def E():
    print("Se acabaron las instrucciones del programa, adios")
    exit()

def L(p):
    global procesosDePagina, tiempoMedida, paginasManejoSwap, lruSwap, fifoSwap
    objetoDeSwap = {}
    if (procesosDePagina[p] == None):
        print("No existe el proceso: ",p)
        return
    if "tiempoTerminacion" in  procesosDePagina[p]:
        print("el proceso ya se liberó")
        return
    paginas = procesosDePagina[p]

    for key in paginas:
        if key!= "tiempoInicio":
            cargarPaginaFrame(paginas[key],None,None)
    
    if algoritmo:
        fifoSwap = [i for i in fifoSwap if i not in paginas.values()]
    else:
        lruSwap = [i for i in lruSwap if i not in paginas.values()]
    
    framesDePagina = [math.floor(paginas[i]/16) for i in paginas.keys() if i != 'tiempoInicio']
    print("Se liberaron los marcos de página: ", framesDePagina)

    if p in paginasManejoSwap:
        objetoDeSwap = paginasManejoSwap[p]

        for key in objetoDeSwap:
            cargarPaginaSwap(objetoDeSwap[key],None,None)
        
        framesDePaginaSwapiados = [math.floor(i/16) for i in objetoDeSwap.values()]
        print("Los marcos de memoria liberados del area de swapping fueron: ", framesDePaginaSwapiados)
        del paginasManejoSwap[p]
        tiempoMedida += (len(paginas) + len(objetoDeSwap) -1)

        procesosDePagina[p]["tiempoTerminacion"] = tiempoMedida

    