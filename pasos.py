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
    #Guarda en paginasManejoSwap donde el proceso se guardar en swap
    paginasManejoSwap[procesoAnterior][paginaAnterior] = verificadorFrameLibreEnSwap

    del paginasManejoSwap[procesoAnterior][paginaAnterior] #Quita los frames pasados de paginasManejoSwap

    #Carga la página al frame 
    cargarPaginaFrame(siguienteFrame, procesosNuevo, paginaNueva) 
    paginasManejoSwap[procesosNuevo][paginaNueva] = siguienteFrame

    tiempoMedida += 20  #incrementa el tiempo 2 segundos 

    return True


#cargarPaginaSwap: carga página a memoria swap
#@pagina: la página a cargar
#@procesoAnterior: proceso anterior
#@paginaAnterior: pagina anterior 
def cargarPaginaSwap(pagina, procesoAnterior, paginaAnterior):
    val = None if procesoAnterior == None and paginaAnterior == None else [procesoAnterior,paginaAnterior]
    for i in range(0, 16): #16 es el tamaño de página
        areaSwapping[pagina + i] = val


#cargarPaginaFrame: carga frame a memoria 
#@frameLibre: el frame a cargar
#@procesoAnterior: proceso anterior
#@paginaAnterior: pagina anterior 
def cargarPaginaFrame(frameLibre, procesosNuevo, paginaNueva):
    val = None if procesosNuevo == None and paginaNueva == None else [procesosNuevo, paginaNueva]
    for i in range(0, 16): #16 es el tamaño de página
        memory[frameLibre + i] = val

#P: carga un proceso a memoria[]
#@n: número de bytes 
#@p: ID del proceso 
def P(n, p): #Paso[1] = bytes a asignar, Paso[2] = proceso
    global tiempoMedida, swapsTotales
    print("Para la instruccion P asignammos: ", n, "bytes al proceso: ", p)

    #Anlizador de casos invaliados 
    if p < 0:
        print("ERROR: no puede haber procesos menores a 0")
        return
    if p in procesosDePagina:
        print("Ese procesos ya existe")
        return
    if (n <= 0 or n > 2048):
        print("ERROR: los bytes a asignar no son validos")
        return
    
    numeroPaginas = math.ceil(n / tamañoDePaginas) #Calcular cuantas páginas son necesarias para cargar el proceso

    procesosDePagina[p] = {} 

    procesosDePagina[p]["tiempoInicio"] = tiempoMedida #Guarda el tiempo de inico del proceso 
    paginaActual = 0
    manejoDeFramesVacios = 0

    frames = [] #frames usados 

    while paginaActual < numeroPaginas:

        #Si no hay frames vacios y el proceso no se a cargado completamente 
        if paginaActual < numeroPaginas and manejoDeFramesVacios >= 2048:
            siguienteFrame = escojeFrameParaSwap()
            cambio = swap(paginaActual, p, siguienteFrame)

            if not cambio:
                return
            #guarda el frame cargado para luego desplegarlo
            frames.append(math.floor(siguienteFrame/16)) #16 es en número de página

            #Suma al contador de Swaps 
            swapsTotales += 1
            paginaActual += 1
    #Encuentra el primer o siguiente frame vacio 
        while manejoDeFramesVacios < 2048: #Mientras sea menor al tamaño de memoria (2048), guardas el frame
        #Si en la manejoDeFramesVaciones no hay nada, se guarda el frame 
            if memory[manejoDeFramesVacios] == None:
                frames.append(math.floor(manejoDeFramesVacios/16)) #guarda el frame cargado para luego desplegarlo
                procesosDePagina[p][paginaActual] = manejoDeFramesVacios
                if algoritmo:
                #FIFO
                #Si sea usa fifo, se agrega el frame a la cola de fifo
                    fifoSwap.insert(0, manejoDeFramesVacios) 
                else:
                #LRU
                #Si sea usa lru, se agrega el frame a la cola de lru
                    lruSwap.insert(0, manejoDeFramesVacios)
            
                cargarPaginaFrame(manejoDeFramesVacios, p, paginaActual) #Carga este frame

                tiempoMedida += 10 #Suma 1 segundo al tiempo de cargar la página en memoria
                paginaActual += 1 
                break

            manejoDeFramesVacios += 16 #Se mueve el aisugeinte frame (16 bytes)
    print("Marcos de pagina: ", frames,"al proceso: ",p)

#Esta instrucciones acaba el programa 
def E():
    print("Se acabaron las instrucciones del programa, vuelva pronto") #Tiempo de despedida
    exit()

#L: Libera un espacio de memoria donde se encontraba un proceso
#@p: El proceso a liberar 
def L(p):
    global procesosDePagina, tiempoMedida, paginasManejoSwap, lruSwap, fifoSwap
    objetoDeSwap = {}
    #Revisa si el proceso existe
    if (procesosDePagina[p] == None):
        print("No existe el proceso: ",p)
        return
    if "tiempoTerminacion" in  procesosDePagina[p]:
        print("el proceso ya se liberó")
        return

    #Guarda el proceso
    paginas = procesosDePagina[p]

    for key in paginas:
        if key!= "tiempoInicio":
            cargarPaginaFrame(paginas[key],None,None)
            
    #Dependiendo del algoritmo utilizado 
    if algoritmo:#FIFO = true
        #Liberar la cola de FIFO de los frames del proceso que se quiere liberar sin alterar los demas. 
        fifoSwap = [i for i in fifoSwap if i not in paginas.values()]
    else:#LRU = false
        #Liberar la cola de LRU de los frames del proceso que se quiere liberar sin alterar los demas.
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

def encuentraFrameLibreEnMemoria():
    for i in range(0,2048,16):
        if(memory[i]==None):
            return i
    print("ERROR: Memoria de Swap llena")
    return 0

def nuevoLru(pagina):
    lruSwap.remove(pagina)
    lruSwap.insert(0,pagina)

#Accede a la memoria virtual del proceso dado
#@direccionVirtual: la direccion virtual
#@proceso: id del proceso
#@m: 0 es leer y 1 es escribir
def A(direccionVirtual, p, m):
    global swapsTotales, fallosDePaginaTotales, tiempoMedida
    print("obtiene la direccion virtual: ",direccionVirtual," del proceso dado: ",p)
    if m == 1:
        print("modifica")
    else:
        print("leer")
    #Analizador de casos inválidos
    if m != 0 and m != 1:
        print("ERROR: Se ingreso un valor de m diferente de 0 o 1")
        return
    if not p in procesosDePagina:
        print("ERROR: No existe el proceso: ",p)
        return
    if direccionVirtual < 0 or direccionVirtual > len(procesosDePagina[p])*16:
        print("ERROR: La direccion virtual es incorrecta o es demasiado grande")
        return
    
    #Direccion Fisica calculo
    pagina = math.floor(direccionVirtual/16)
    fraccion, i = math.modf(direccionVirtual/16)
    desplazamiento = int(round(fraccion, 4) * 16) #Calculo desplazamiento en enteros

    if pagina not in procesosDePagina[p]:
        if pagina not in paginasManejoSwap[p]:  #checa que la página exista 
            print("ERROR: No hay direccion asociada al proceso: ",p)
            return 

        fallosDePaginaTotales += 1 #almacena el fallo de página

        frameParaSwapiar = encuentraFrameLibreEnMemoria()#checa si la memoria esta libre

        #Si la memoria no esta libre, escoge para el swap
        if frameParaSwapiar == 0:
            frameParaSwapiar = escojeFrameParaSwap()
            cambio = swap(pagina,p,frameParaSwapiar)
            if not cambio:
                return
            swapsTotales += 2 #añade al contador de swaps
        else:
            cargarPaginaFrame(frameParaSwapiar,p,pagina)
            procesosDePagina[p][pagina] = frameParaSwapiar
            tiempoMedida += 11 #se suma tiempo de cargar el frame 
            if algoritmo:
                #FIFO
                #Si sea usa fifo, se agrega el frame a la cola de fifo
                fifoSwap.insert(0, frameParaSwapiar) 
            else:
                #LRU
                #Si sea usa lru, se agrega el frame a la cola de lru
                lruSwap.insert(0, frameParaSwapiar)
            swapsTotales += 1
        print("La pagina: ",pagina," del proceso dado: ",p," en la posicion: ",paginasManejoSwap[p][pagina]," se localizó y cargo al marco: ",math.floor(frameParaSwapiar/16))
        #Borra esta pagina de la areaDeSwap
        paginaEnAreaDeSwap = paginasManejoSwap[p][pagina]
        cargarPaginaSwap(paginaEnAreaDeSwap,None,None)
        del paginasManejoSwap[p][pagina]
    
    elif not algoritmo:
        #Si la página esta en memoria y se usa el algoritmo lru, entonces se actualiza la cola 
        nuevoLru(procesosDePagina[p][pagina])
    tiempoMedida += 1 #Se añade tiempo de escritura y lectura
    frame = procesosDePagina[p][pagina] #la direccion del frame donde la página se va a guardar
    direccionReal = frame + desplazamiento
    print("La direccion Virtual es: ",direccionVirtual)
    print("La direccion Real es: ",direccionReal)

def F():
    global procesosDePagina, paginasManejoSwap, lruSwap, fifoSwap, fallosDePaginaTotales, swapsTotales, tiempoMedida

    numeroProcesos = 0 # contadoe de los proceso 
    
    turnAroundPromedio = 0 # se hace la suma del turnAroundActual y se divide entre en número de procesos

    if len(procesosDePagina) == 0:
        print("No hay procesos guardados, por ende no se puede calcular el reporte")
        return
    
    valores = [i for i in procesosDePagina if "tiempoTerminacion" not in procesosDePagina[i]]
    if len(valores) > 0:
        print("Se liberan procesos que estan corriendo al momento")
        print()
        #Tiempo de Turnaround
        for key in sorted(valores):
            if "tiempoTerminacion" not in procesosDePagina[key]:
                print("L(", key, ")")
                L(key)
                print()
    
    print("Reporte: ")
    for key in sorted(procesosDePagina.keys()):
        numeroProcesos += 1
        turnAroundActual = (procesosDePagina[key]["tiempoTerminacion"] - procesosDePagina[key]["tiempoInicio"])/10 #Tiempo final - inicial entre 10 para dar segundos

        print("Proceso: ",key," Turnaround: ", turnAroundActual)

        turnAroundPromedio += turnAroundActual
    
    turnAroundPromedio = turnAroundPromedio/numeroProcesos

    print("El turnaround promedio es: ", turnAroundPromedio) #Turnaoround promedio 

    print("Con: ",fallosDePaginaTotales," fallos de pagina") #fallos de página por proceso 

    print("numero de swaps: ", swapsTotales)#cantidad de operaciones swaps


    #------------- Reseteo de variables --------------------------------------

    memory = [None] * 2048 #Area de memoria

    areaSwapping = [None] * 4096 #Area de Swapping

    procesosDePagina = {} #Para organizar cada procesos de pagina segun un identificador "p" y por frames

    paginasManejoSwap = {} #Para manejo del swap por frames

    swapsTotales = 0 #contador de swaps totales

    fallosDePaginaTotales = 0 #contador de fallos de página totales

    tiempoMedida = 0 

    #Colas 
    if algoritmo:
        fifoSwap = []
    else:
        lruSwap = []

def C(comentario):
    print("el camentario es: ",comentario)