import math

tamañoDePaginas = 16 #Paginacion de 16
algoritmo = True #FIFO por Default

memory = [None] * 2048 #Area de memoria
areaSwapping = [None] * 4096 #Area de Swapping

procesosDePagina = {} #Para organizar cada procesos de pagina segun un identificador "p" y por frames

paginasManejoSwap = {} #Para manejo del swap por frames

swapsTotales = 0 #contador de swaps realizados 
fallosDePaginaTotales = 0  #contador de fallos de página totales
tiempoMedida = 0  #variable para medir el tiempo y luego calcular el rendimiento 
fifoSwap = [] # cola para FIFO 
lruSwap = [] # cola para LRU

# escogeFrameParaSwap:si es FIFO O LRU, escoge que frame remover de memoria y colocar en swap
def escojeFrameParaSwap():

    if(algoritmo): #FIFO = true 
        #Guarda el siguiente frame de la cola de FIFO
        frameAElegir = fifoSwap.pop()
        #Lo añade a la cola de swaps de FIFO
        fifoSwap.insert(0, frameAElegir)
    else: #LRU
        #Guarda el siguiente frame de la cola de LRU
        frameAElegir = lruSwap.pop()
        #Lo añade a la cola de swaps de LRU
        lruSwap.insert(0, frameAElegir)

    return frameAElegir 

#verSiEstaLibreEnMemoria: busca la siguiente página disponible en memoria y la regresa
def verSiEstaLibreEnMemoria():
    #Itera de 0 hasta 4096 (tamaño de memoria), dando saltos de 16(tamañoDePaginas)
    for i in range(0, 4096, tamañoDePaginas):
        if(areaSwapping[i] == None):
            return i #página en memoria 
    print("ERROR: La memoria Swap esta llena")
    return 0

#swap: pone la página del proceso nuevo en la memoria y pone la página actual en el frame correspondiente en el área de swap 
#@paginaNueva: número de pagina del nuevo frame
#@procesoNuevo: id del proceso del nuevo frame
#@siguienteFrame: spacio en memoria que corresponde a donde el nuevo proceso se pondrá 
def swap(paginaNueva, procesosNuevo, siguienteFrame):
    global tiempoMedida

    procesoAnterior, paginaAnterior = memory[siguienteFrame] #obtine datos del proceso y la página anterior

    verificadorFrameLibreEnSwap = verSiEstaLibreEnMemoria() #Encuentra el siguiente frame disponible 

    if verificadorFrameLibreEnSwap == 0:
        return False
    
    print("La página: ", paginaAnterior," del proceso: ",procesoAnterior," haciendo swapping al marco: ",math.floor(verificadorFrameLibreEnSwap/tamañoDePaginas), "del área de swapping")

    cargarPaginaSwap(verificadorFrameLibreEnSwap, procesoAnterior, paginaAnterior) #Carga la página swapiada en la memoria Swap

    if procesoAnterior not in paginasManejoSwap: #Si el proceso no esta en paginasManejoSwap, entonces la añade
        paginasManejoSwap[procesoAnterior] = {}

    paginasManejoSwap[procesoAnterior][paginaAnterior] = verificadorFrameLibreEnSwap #Guarda en paginasManejoSwap donde el proceso se guardar en swap

    del paginasManejoSwap[procesoAnterior][paginaAnterior] #Quita los frames pasados de paginasManejoSwap

    #Carga la página al frame 
    cargarPaginaFrame(siguienteFrame, procesosNuevo, paginaNueva) 
    paginasManejoSwap[procesosNuevo][paginaNueva] = siguienteFrame

    tiempoMedida += 20  #incrementa el tiempo 2 segundos 

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
    global tiempoMedida, swapsTotales
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

    