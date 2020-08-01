import math

memoria = 2048 
memoriaSwap = 4096
tamañoDePagina = 16 #Paginacion de 16
algoritmo = False #LRU por Default
M = [None] * memoria #Area de memoria
S = [None] * memoriaSwap #Area de Swapping
paginasProcesos = {} #Para organizar cada procesos de pagina segun un identificador "p" y por frames
paginasSwap = {} #Para manejo del swap por frames
fifoSwap = [] #cola para FIFO 
lruSwap = []  #cola para LRU
tiempoMedida = 0 #variable para medir el tiempo y luego calcular el rendimiento 
fallosDePagina = 0 #contador de fallos de página totales
swapsTotales = 0 #contador de swaps realizados 

#encuentraFrameEnSwap: 
def encuentraFrameEnSwap():
    for i in range(0,memoriaSwap,tamañoDePagina): # (0, 2048,16)
        if(S[i]==None): 
            return i #frame en swap 

    print("ERROR: Memoria de Swap llena")
    return -1

#verSiEstaLibreEnMemoria: busca la siguiente página disponible en memoria y la regresa
def encuentraFrameEnMemoria():
    #Itera de 0 hasta 4096 (tamaño de memoria), dando saltos de 16(tamañoDePaginas)
    for i in range(0,memoria,tamañoDePagina):
        if(M[i]==None): 
            return i #página en memoria 
    print("ERROR: La memoria esta llena")
    return -1

#pginaFrame: carga frame a memoria 
#@i: el frame a cargar
#@p: proceso anterior
#@pagina: pagina anterior
def paginaFrame(i, p, pagina):
    val = None if p == None and pagina == None else [p,pagina]
    for j in range(0, tamañoDePagina): #tamañoDePagina =16
        M[i + j] = val
            
#paginaSwap: carga página a memoria swap
#@i: la página a cargar
#@p: proceso anterior
#@pagina: pagina anterior 
def paginaSwap(i, p, pagina):
    val = None if p == None and pagina == None else [p,pagina]
    for j in range(0, tamañoDePagina): #tamañoDePagina =16
        S[i + j] = val

#intercambio: pone la página del proceso nuevo en la memoria y pone la página actual en el frame correspondiente en el área de swap 
#@nueva: número de pagina del nuevo frame
#@procesoActualizar: id del proceso del nuevo frame
#@frame: spacio en memoria que corresponde a donde el nuevo proceso se pondrá 
def intercambio(nueva, procesoActualizar, frame):
    global tiempoMedida, fallosDePagina

    procesoAntes, paginaAntes = M[frame] #obtine datos del proceso y la página anterior

    sePuedeHacerSwap = encuentraFrameEnSwap() #Encuentra el siguiente frame disponible 
    if sePuedeHacerSwap == -1:
        return False

    print("La página ", paginaAnterior, " del proceso ", procesoAnterior, " haciendo swapping al marco: ", math.floor(sePuedeHacerSwap/tamañoDePagina), " del área de swapping.")

    paginaSwap(sePuedeHacerSwap, procesoAntes, paginaAntes) #Carga la página swapiada en la memoria Swap

    if procesoAntes not in paginasSwap: #Si el proceso no esta en paginasManejoSwap, entonces la añade
        paginasSwap[procesoAntes] = {}

    #Guarda en paginasManejoSwap donde el proceso se guardar en swap
    paginasSwap[procesoAntes][paginaAntes] = sePuedeHacerSwap

    del paginasProcesos[procesoAntes][paginaAntes] #Quita los frames pasados de paginasManejoSwap

    #Carga la página al frame 
    paginaFrame(frame, procesoActualizar, nueva)
    paginasProcesos[procesoActualizar][nueva] = frame
    
    tiempoMedida += 20  #incrementa el tiempo 2 segundos 
    return True

#escoge:si es FIFO O LRU, escoge que frame remover de memoria y colocar en swap
def escoje():
    if(algoritmo):#FIFO = true 
        #Guarda el siguiente frame de la cola de FIFO
        frame = fifoSwap.pop()
        #Lo añade a la cola de swaps de FIFO
        fifoSwap.insert(0, frame)
    else: #LRU
        #Guarda el siguiente frame de la cola de LRU
        frame = lruSwap.pop()
        #Lo añade a la cola de swaps de LRU
        lruSwap.insert(0, frame)
    return frame

#ActualizarLRU 
#@pagina: que se quiere mover de lugar 
def actualizaLru(pagina):
    lruSwap.remove(pagina)
    lruSwap.insert(0,pagina)

#Accede a la memoria virtual del proceso dado
#@d: la direccion virtual
#@p: id del proceso
#@m: 0 es leer y 1 es escribir
def A(d, p, m):
    global swapsTotales,tiempoMedida, fallosDePagina
    print("obtiene la direccion virtual: ",d," del proceso dado: ",p)
    #Verifica la instruccion m 
    if m == 1:
        print(" y modificar dicha dirección")
    else:
        print()

    #Analizador de casos inválidos
    if not p in paginasProcesos:
        print("ERROR: No existe el proceso: ",p)
        return
    if d < 0 or d > len(paginasProcesos[p]) * tamañoDePagina:
        print("ERROR: La direccion virtual es incorrecta o es demasiado grande")   
        return
    if m != 0 and m != 1:
        print("ERROR: Se ingreso un valor de m diferente de 0 o 1")
        return

    #Direccion Fisica calculo
    pagina = math.floor(d / tamañoDePagina)
    calculo, i = math.modf(d / tamañoDePagina)
    desplazamiento = int(round(calculo, 4) * 16) #Calculo desplazamiento en enteros
    
    if pagina not in paginasProcesos[p]:
        if pagina not in paginasSwap[p]: #checa que la página exista 
            print("ERROR: No hay direccion asociada al proceso: ",p)
            return

        fallosDePagina += 1 #almacena el fallo de página

        frame = encuentraFrameEnMemoria() #checa si la memoria esta libre

        #Si la memoria no esta libre, escoge para el swap
        if frame == -1:
            frame = escoje()     
            cambio = intercambio(pagina,p,frame)
            if not cambio:
                return
            swapsTotales += 2 #añade al contador de swaps
        else:
            paginaFrame(frame,p,pagina)
            paginasProcesos[p][pagina] = frame
            tiempoMedida += 11 #se suma tiempo de cargar el frame 
            if algoritmo:
                #FIFO
                #Si sea usa fifo, se agrega el frame a la cola de fifo
                fifoSwap.insert(0, frame)
            else:
                 #LRU
                #Si sea usa lru, se agrega el frame a la cola de lru
                lruSwap.insert(0, frame)
            swapsTotales += 1
        print("La pagina: ",pagina," del proceso dado: ",p," en la posicion: ", paginasSwap[p][pagina], " se localizó y cargo al marco: ", math.floor(frame/tamañoDePagina), ".")
        
        #Borra esta pagina de la areaDeSwap
        paginaSwap = paginasSwap[p][pagina]
        paginaSwap(paginaSwap,None, None)
        del paginasSwap[p][pagina]

    elif not algoritmo:
        #Si la página esta en memoria y se usa el algoritmo lru, entonces se actualiza la cola 
        actualizaLru(paginasProcesos[p][pagina])

    tiempoMedida += 1 #Se añade tiempo de escritura y lectura
    frame = paginasProcesos[p][pagina] #la direccion del frame donde la página se va a guardar
    direccionReal = frame + desplazamiento
    print("La direccion Virtual es: ",d)
    print("La direccion Real es: ",direccionReal)

#P: carga un proceso a memoria[]
#@n: número de bytes 
#@p: ID del proceso 
def P(n, p): #Paso[1] = bytes a asignar, Paso[2] = proceso
    global tiempoMedida, fallosDePagina, swapsTotales
    print("Para la instruccion P asignammos: ", n, "bytes al proceso: ", p)

    #Anlizador de casos invaliados 
    if n <= 0:
        print("EROR: el tamaño del proceso debe ser mayor que cero.")
        return
    if n > 2048:
        print("EROR: el tamaño del proceso no puede exceder 2048 bytes.")
        print("No se ejecutará esta instrucción")        
        return
    if p < 0:
        print("ERROR: no puede haber procesos menores a 0")
        return
    if p in paginasProcesos:
        print("Ese procesos ya existe")
        return
    
    numeroPaginas = math.ceil(n / tamañoDePagina)#Calcular cuantas páginas son necesarias para cargar el proceso

    frames = []#frames usados 

    paginasProcesos[p] = {}
    paginasProcesos[p]["tiempoInicial"] = tiempoMedida #Guarda el tiempo de inico del proceso 
    i = 0
    usandoPagina = 0
    while usandoPagina < numeroPaginas:

        #Si no hay frames vacios y el proceso no se a cargado completamente
        if i >= memoria and usandoPagina < numeroPaginas:
            
            frame = escoje()

            cambio = intercambio(usandoPagina,p,frame)
            if not cambio:
                return

            #guarda el frame cargado para luego desplegarlo
            frames.append(math.floor(frame/tamañoDePagina)) #16 es en número de página

            #Suma al contador de Swaps 
            swapsTotales += 1

            usandoPagina += 1
        
        #Encuentra el primer o siguiente frame vacio 
        while i < memoria:#Mientras sea menor al tamaño de memoria (2048), guardas el frame
        #Si en la manejoDeFramesVaciones no hay nada, se guarda el frame 
            if M[i] == None:
                frames.append(math.floor(i/tamañoDePagina)) #guarda el frame cargado para luego desplegarlo
                paginasProcesos[p][usandoPagina] = i
                if(algoritmo):
                    #FIFO
                    #Si sea usa fifo, se agrega el frame a la cola de fifo
                    fifoSwap.insert(0, i)
                else:
                    #LRU
                    #Si sea usa lru, se agrega el frame a la cola de lru
                    lruSwap.insert(0, i)

                paginaFrame(i, p, usandoPagina) #Carga este frame
                tiempoMedida += 10 #Suma 1 segundo al tiempo de cargar la página en memoria
                usandoPagina += 1
                break
            i += tamañoDePagina #Se mueve el aisugeinte frame (16 bytes)

    print("Marcos de pagina: ", frames,"al proceso: ",p)

#L: Libera un espacio de memoria donde se encontraba un proceso
#@p: El proceso a liberar 
def L(p):
    global fifoSwap, lruSwap, paginasProcesos, paginasSwap, tiempoMedida
    #Revisa si el proceso existe
    if (paginasProcesos[p] == None):
        print("No existe el proceso: ",p)
        return
    if "tiempoFinal" in paginasProcesos[p]:
        print ("El proceso ", p, " ya sé liberó ")
        return

    paginas = paginasProcesos[p]#Guarda el proceso

    for key in paginas:
        if key!= "tiempoInicial":
            paginaFrame(paginas[key],None, None)

    #Dependiendo del algoritmo utilizado 
    if algoritmo:#FIFO = true
        #Liberar la cola de FIFO de los frames del proceso que se quiere liberar sin alterar los demas. 
        fifoSwap = [i for i in fifoSwap if i not in paginas.values()]
    else:
        #LRU = false
        #Liberar la cola de LRU de los frames del proceso que se quiere liberar sin alterar los demas.
        lruSwap = [i for i in lruSwap if i not in paginas.values()]

    framesDePagina = [math.floor(paginas[i]/tamañoDePagina ) for i in paginas.keys() if i != 'tiempoInicial']
    print ("Se liberan los marcos de página de memoria real:", framesDePagina)

    cambio = {}
    if p in paginasSwap:
        cambio = paginasSwap[p]

        for key in cambio:
            paginaSwap(cambio[key], None, None)

        cambioPaginasFrames = [math.floor(i/tamañoDePagina) for i in cambio.values()]
        print ("Los marcos de memoria", cambioPaginasFrames, " fueron liberados del área de swapping")
        del paginasSwap[p]
    tiempoMedida += (len(paginas) + len(cambio) - 1) 
    paginasProcesos[p]["tiempoFinal"] = tiempoMedida

#E: Final del programa 
def E():
    print("Fin de las instrucciones, vuelva pronto!!!") #Mensaje Despedida
    exit()

#F: Este proceso es la terminación de un bloque de instrucciones y el output son las estadísticas 
def F():
    global paginasProcesos, paginasSwap, lruSwap, fifoSwap, fallosDePagina, swapsTotales, tiempoMedida
    procesosContador = 0 # contador de los procesos
    turnaroundPromedio = 0 # se hace la suma del turnAroundActual y se divide entre en número de procesos
    if len(paginasProcesos) == 0:
        print("No hay procesos guardados, por ende no se puede calcular el reporte")
        return
     
    identificador = [i for i in paginasProcesos if "tiempoFinal" not in paginasProcesos[i] ]
    if len(identificador) > 0:
        print("Se liberan procesos que estan corriendo al momento")
        print()
        #Tiempo de Turnaround
        for key in sorted(identificador):
            if "tiempoFinal" not in paginasProcesos[key] :
                print("L(", key, ")")
                L(key)
                print()

    print("Reporte; ")
    for key in sorted(paginasProcesos.keys()):

        procesosContador += 1
        turnaroundActual = (paginasProcesos[key]["tiempoFinal"] - paginasProcesos[key]["tiempoInicial"])/10

        print("Proceso: ", key, "\t Turnaround: ", turnaroundActual)
        
        turnaroundPromedio += turnaroundActual
    
    turnaroundPromedio = turnaroundPromedio / procesosContador

    print("El turnaround promedio es: ", turnaroundPromedio) #Turnaround promedio
    print("Con: ", fallosDePagina, " fallos de página. ") #fallos de página por proceso 
    print("Número de operaciones de swap : ", swapsTotales) #cantidad de operaciones swaps

    #------------- Reseteo de variables --------------------------------------
    #Colas
    if algoritmo:   
        fifoSwap = []
    else:     
        lruSwap = []

    M = [None] * memoria #Area de memoria 
    S = [None] * memoriaSwap #Area de Swapping
    
    paginasSwap = {} #Para manejo del swap por frames

    paginasProcesos = {} #Para organizar cada procesos de pagina segun un identificador "p" y por frames

    tiempoMedida = 0
    fallosDePagina = 0 #contador de fallos de página totales
    swapsTotales = 0 #contador de swaps totales

#C: Esta instrucción es para comentario 
def C(comentario):
    print("El camentario es: ",comentario)

#----------------------------------- FIN DEL PROGRAMA --------------------------------------------