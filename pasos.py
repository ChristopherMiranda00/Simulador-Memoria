import math

memoria = 2048
memoriaSwap = 4096
tamañoDePagina = 16
algoritmo = False 
M = [None] * memoria
S = [None] * memoriaSwap
paginasProcesos = {}
paginasSwap = {}
fifoSwap = []
lruSwap = []
tiempoMedida = 0
fallosDePagina = 0
swapsTotales = 0

def encuentraFrameEnSwap():
    for i in range(0,memoriaSwap,tamañoDePagina):
        if(S[i]==None): return i

    print('La memoria de swap está llena. Se requiere más para completar la secuencia de procesos.')
    return -1

def encuentraFrameEnMemoria():
    for i in range(0,memoria,tamañoDePagina):
        if(M[i]==None): return i
    return -1

def paginaFrame(i, p, pagina):
    val = None if p == None and pagina == None else [p,pagina]
    for j in range(0, tamañoDePagina):
        M[i + j] = val
            
def paginaSwap(i, p, pagina):
    val = None if p == None and pagina == None else [p,pagina]
    for j in range(0, tamañoDePagina):
        S[i + j] = val

def intercambio(nueva, procesoActualizar, frame):
    global tiempoMedida, fallosDePagina

    procesoAntes, paginaAntes = M[frame]

    sePuedeHacerSwap = encuentraFrameEnSwap()
    if sePuedeHacerSwap == -1:
        return False

    print("Página ", paginaAntes, " del proceso ", procesoAntes, " swappeada al marco ", math.floor(sePuedeHacerSwap/tamañoDePagina), " del área de swapping.")

    paginaSwap(sePuedeHacerSwap, procesoAntes, paginaAntes)

    if procesoAntes not in paginasSwap:
        paginasSwap[procesoAntes] = {}

    paginasSwap[procesoAntes][paginaAntes] = sePuedeHacerSwap

    del paginasProcesos[procesoAntes][paginaAntes]

    paginaFrame(frame, procesoActualizar, nueva)
    paginasProcesos[procesoActualizar][nueva] = frame
    
    tiempoMedida += 20
    return True

def escoje():
    if(algoritmo):
        frame = fifoSwap.pop()
        fifoSwap.insert(0, frame)
    else:
        frame = lruSwap.pop()
        lruSwap.insert(0, frame)
    return frame

def actualizaLru(pagina):
    lruSwap.remove(pagina)
    lruSwap.insert(0,pagina)

def A(d, p, m):
    global swapsTotales,tiempoMedida, fallosDePagina
    print("Obtener la dirección real correspondiente a la dirección virtual", d, "del proceso", p, end="")
    if m == 1:
        print(" y modificar dicha dirección")
    else:
        print()

    if not p in paginasProcesos:
        print("Error: no existe el proceso ", p, ".", sep="")
        print("No se ejecutará esta instrucción")
        return
    if d < 0 or d > len(paginasProcesos[p]) * tamañoDePagina:
        print("Error: la dirección virtual está fuera del rango de direcciones del proceso ", p, ".", sep="")
        print("No se ejecutará esta instrucción")
        return
    if m != 0 and m != 1:
        print("Error: el modo de acceso debe ser 0 (lectura) o 1 (escritura).")
        print("No se ejecutará esta instrucción")
        return

    pagina = math.floor(d / tamañoDePagina)
    calculo, i = math.modf(d / tamañoDePagina)
    desplazamiento = int(round(calculo, 4) * 16)
    
    if pagina not in paginasProcesos[p]:
        if pagina not in paginasSwap[p]:
            print("No existe esa dirección para el proceso ", p)
            print("No se ejecutará esta instrucción")
            return

        fallosDePagina += 1

        frame = encuentraFrameEnMemoria()

        if frame == -1:
            frame = escoje()     
            cambio = intercambio(pagina,p,frame)
            if not cambio:
                return
            swapsTotales += 2
        else:
            paginaFrame(frame,p,pagina)
            paginasProcesos[p][pagina] = frame
            tiempoMedida += 11
            if algoritmo:
                fifoSwap.insert(0, frame)
            else:
                lruSwap.insert(0, frame)
            swapsTotales += 1
        print("Se localizó la página ", pagina, " del proceso ", p, " que estaba en la posición ", paginasSwap[p][pagina], " y se cargó al marco ", math.floor(frame/tamañoDePagina), ".")
        paginaSwap = paginasSwap[p][pagina]
        paginaSwap(paginaSwap,None, None)
        del paginasSwap[p][pagina]

    elif not algoritmo:
        actualizaLru(paginasProcesos[p][pagina])

    tiempoMedida += 1
    frame = paginasProcesos[p][pagina]
    direccionReal = frame + desplazamiento
    print("Dirección virtual: ", d, ". ", end="", sep="")

    print("Dirección real:", direccionReal)

def P(n, p):
    global tiempoMedida, fallosDePagina, swapsTotales
    print("Asignar", n, "bytes al proceso", p)

    if n <= 0:
        print("Error: el tamaño del proceso debe ser mayor que cero.")
        print("No se ejecutará esta instrucción")
        return
    if n > 2048:
        print("Error: el tamaño del proceso no puede exceder 2048 bytes.")
        print("No se ejecutará esta instrucción")        
        return
    if p < 0:
        print("Error: el identificador del proceso debe ser igual o mayor que cero.")
        print("No se ejecutará esta instrucción")
        return
    if p in paginasProcesos:
        print("Error: ya existe un proceso con ese identificador.")
        print("No se ejecutará esta instrucción")
        return
    
    numeroPaginas = math.ceil(n / tamañoDePagina)

    frames = []

    paginasProcesos[p] = {}
    paginasProcesos[p]["tiempoInicial"] = tiempoMedida
    i = 0
    usandoPagina = 0
    while usandoPagina < numeroPaginas:

        if i >= memoria and usandoPagina < numeroPaginas:
            
            frame = escoje()

            cambio = intercambio(usandoPagina,p,frame)
            if not cambio:
                return
            
            frames.append(math.floor(frame/tamañoDePagina))

            swapsTotales += 1

            usandoPagina += 1
            
        while i < memoria:
            if M[i] == None:
                frames.append(math.floor(i/tamañoDePagina))
                paginasProcesos[p][usandoPagina] = i
                if(algoritmo):
                    fifoSwap.insert(0, i)
                else:
                    lruSwap.insert(0, i)
                paginaFrame(i, p, usandoPagina)
                tiempoMedida += 10
                usandoPagina += 1
                break
            i += tamañoDePagina

    print("Se asignaron los marcos de página", frames, "al proceso", p)

def L(p):
    global fifoSwap, lruSwap, paginasProcesos, paginasSwap, tiempoMedida
    print ("Liberar los marcos de página ocupados por el proceso ", p)
    if (paginasProcesos[p] == None):
        print ("El proceso ", p, " no se ha ejecutado")
        print("No se ejecutará esta instrucción")
        return
    if "tiempoFinal" in paginasProcesos[p]:
        print ("El proceso ", p, " ya fue liberado")
        print("No se ejecutará esta instrucción")
        return
    paginas = paginasProcesos[p]

    for key in paginas:
        if key!= "tiempoInicial":
            paginaFrame(paginas[key],None, None)

    if algoritmo:
        fifoSwap = [i for i in fifoSwap if i not in paginas.values()]
    else:
        lruSwap = [i for i in lruSwap if i not in paginas.values()]

    page_frames = [math.floor(paginas[i]/tamañoDePagina ) for i in paginas.keys() if i != 'tiempoInicial']
    print ("Se liberan los marcos de página de memoria real:", page_frames)

    cambio = {}
    if p in paginasSwap:
        cambio = paginasSwap[p]

        for key in cambio:
            paginaSwap(cambio[key], None, None)

        cambioPaginasFrames = [math.floor(i/tamañoDePagina) for i in cambio.values()]
        print ("Se liberan los marcos", cambioPaginasFrames, "del área de swapping")
        del paginasSwap[p]
    tiempoMedida += (len(paginas) + len(cambio) - 1) 
    paginasProcesos[p]["tiempoFinal"] = tiempoMedida

def E():
    print("Fin de las instrucciones")
    exit()

def F():
    global paginasProcesos, paginasSwap, lruSwap, fifoSwap, fallosDePagina, swapsTotales, tiempoMedida
    procesosContador = 0
    turnaroundPromedio = 0
    if len(paginasProcesos) == 0:
        print("No se tienen procesos en memoria.")
        print("No se pueden calcular el reporte de estadísticas.")
        return
     
    identificador = [i for i in paginasProcesos if "tiempoFinal" not in paginasProcesos[i] ]
    if len(identificador) > 0:
        print("Liberando procesos que aun siguen corriendo para calcular reporte de estadísticas.")
        print()
        for key in sorted(identificador):
            if "tiempoFinal" not in paginasProcesos[key] :
                print("L(", key, ")")
                L(key)
                print()

    print("Fin. Reporte de salida: ")
    for key in sorted(paginasProcesos.keys()):

        procesosContador += 1
        turnaroundActual = (paginasProcesos[key]["tiempoFinal"] - paginasProcesos[key]["tiempoInicial"])/10

        print("Proceso: ", key, "\t Turnaround time: ", turnaroundActual, ".", sep="")
        
        turnaroundPromedio += turnaroundActual
    
    turnaroundPromedio = turnaroundPromedio / procesosContador
    print("Turnaround promedio: ", turnaroundPromedio, sep="")
    print("Page faults: ", fallosDePagina, sep="")
    print("Operaciones de swap in/swap out: ", swapsTotales, sep="")
    if algoritmo:   
        fifoSwap = []
    else:     
        lruSwap = []
    M = [None] * memoria
    S = [None] * memoriaSwap
    
    paginasSwap = {}
    paginasProcesos = {}

    tiempoMedida = 0
    fallosDePagina = 0
    swapsTotales = 0

def C(comentario):
    print("el camentario es: ",comentario)