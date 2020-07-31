import math

memoria = 2048
memoriaSwap = 4096
tamañoDePagina = 16
algoritmo = False 
M = [None] * memoria

S = [None] * memoriaSwap

paginasProcesos = {}

swapped_pages = {}

# Queue of pages used for FIFO Strategy
fifo_next_swap = []

# Queue of pages used for LRU Strategy
lru_next_swap = []

# Current time for measurments (measured in 10ths of a second due to problems with python and floating point sums)
current_time = 0

# Amount of page faults that have occured
page_faults = 0

# Amount of swap in / swap out operations
total_swaps = 0

# Finds next available page in swap memory, and returns it
def findAvailableFrameInSwapMemory():
    for i in range(0,SWAP_memoria,tamañoDePagina):
        if(S[i]==None): return i

    print('La memoria de swap está llena. Se requiere más para completar la secuencia de procesos.')
    print('No se ejecutará esta instrucción.')
    return -1


# Finds next available page in memory, and returns it
def findAvailableFrameInMemory():
    for i in range(0,memoria,tamañoDePagina):
        if(M[i]==None): return i

    return -1


# Loads page i with values val to memory
# i: page
# val: process or value to set
def loadPageToFrame(i, process, page):
    val = None if process == None and page == None else [process,page]
    for j in range(0, tamañoDePagina):
        M[i + j] = val
            

# Loads page i with values val to swap memory
# i: page
# val: process or value to set
def loadPageToSwap(i, process, page):
    val = None if process == None and page == None else [process,page]
    for j in range(0, tamañoDePagina):
        S[i + j] = val


# Puts the new process's new page into memory, in the next frame's current 
#  space of memory, and puts the current page in that frame into the swap area
# new_page: page number of the new frame
# new_process: process id of the new frame
# next_frame: space in memory that corresponds to where the new process will be placed
def swap(new_page, new_process, next_frame):
    global current_time, page_faults

    # Get info of the previous process and its page at that space in memory
    old_process, old_page = M[next_frame]


    # Find next available frame in swap memory
    available_at_swap = findAvailableFrameInSwapMemory()
    if available_at_swap == -1:
        return False

    print("Página ", old_page, " del proceso ", old_process, " swappeada al marco ", math.floor(available_at_swap/tamañoDePagina), " del área de swapping.")
    # Load swapped page to swap memory
    loadPageToSwap(available_at_swap, old_process, old_page)

    # If process is not already in swapped_pages, add it
    if old_process not in swapped_pages:
        swapped_pages[old_process] = {}

    # Store in swapped_pages where the process will be stored in swap
    swapped_pages[old_process][old_page] = available_at_swap

    # Remove old frame from proc_pages
    del paginasProcesos[old_process][old_page]

    # Load page to the frame
    loadPageToFrame(next_frame, new_process, new_page)
    paginasProcesos[new_process][new_page] = next_frame
    
    # Update current time, 2 seconds passed due to writing both to memory and swap
    current_time += 20
    return True


# Uses strategy to choose which frame to remove from memory and place to swap
def chooseNext():
    # Choose which frame to use next
    if(algoritmo):
        # FIFO
        # Get next frame to be swapped, and the process it corresponds to
        next_frame = fifo_next_swap.pop()
        # Add it back to queue, since it will be reused
        fifo_next_swap.insert(0, next_frame)
    else:
        # LRU
        # Get next frame to be swapped, and the process it corresponds to
        next_frame = lru_next_swap.pop()
        # Add it back to queue, since it will be reused
        lru_next_swap.insert(0, next_frame)
    return next_frame


# Updates an exsiting entry in the lru queue, placing it to the end of the queue
def updateLRU(page):
    lru_next_swap.remove(page)
    lru_next_swap.insert(0,page)


# Access virtual address "d" of process "p".
# d: virtual address (0 <= d <= max virtual address of "p")
# p: process ID
# m: mode (0 - read only, 1 - write)
def A(d, p, m):
    global total_swaps,current_time, page_faults
    print("Obtener la dirección real correspondiente a la dirección virtual", d, "del proceso", p, end="")
    if m == 1:
        print(" y modificar dicha dirección")
    else:
        print()

    # Handle invalid cases
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

    # Calculate the physical address.
    # The page number of the process (e.g. 0, 1, 2...)
    page = math.floor(d / tamañoDePagina)
    # The displacement from the start of the page.
    fraction, whole = math.modf(d / tamañoDePagina)
    disp = int(round(fraction, 4) * 16)
    
    if page not in paginasProcesos[p]:
        # Checks that page exists first
        if page not in swapped_pages[p]:
            print("No existe esa dirección para el proceso ", p)
            print("No se ejecutará esta instrucción")
            return

        # page is in the swapping area
        # choose next frame to swap and swap it

        # Store page fault
        page_faults += 1

        # Check first if there is free memory
        next_frame = findAvailableFrameInMemory()

        # If no memory is free, choose which to swap
        if next_frame == -1:
            next_frame = chooseNext()     
            swapped = swap(page,p,next_frame)
            if not swapped:
                return
            # Adds a swap out and a swap in to the stored count
            total_swaps += 2
        else:
            loadPageToFrame(next_frame,p,page)
            paginasProcesos[p][page] = next_frame
            # Add time to load page to frame and off  
            current_time += 11
            if algoritmo:
                # FIFO
                fifo_next_swap.insert(0, next_frame)
            else:
                # LRU
                lru_next_swap.insert(0, next_frame)
            # Since only moving out of swap, only a swap out is counted 
            total_swaps += 1
        print("Se localizó la página ", page, " del proceso ", p, " que estaba en la posición ", swapped_pages[p][page], " y se cargó al marco ", math.floor(next_frame/tamañoDePagina), ".")

        # Remove from this page from area
        page_in_swaparea = swapped_pages[p][page]
        loadPageToSwap(page_in_swaparea,None, None)
        del swapped_pages[p][page]

    elif not algoritmo:
        # if the page is already in memory,and we are using lru
        # update lru queue to move the current page being
        updateLRU(paginasProcesos[p][page])

    # Adds read/write time
    current_time += 1
    # The address of the frame where the page is stored.
    frame = paginasProcesos[p][page]
    addr = frame + disp
    print("Dirección virtual: ", d, ". ", end="", sep="")

    print("Dirección real:", addr)

# Load a process to memory (M).
# n: number of bytes (1 <= n <= 2048)
# p: process ID
# Command example: P 534 5834
def P(n, p):
    global current_time, page_faults, total_swaps
    print("Asignar", n, "bytes al proceso", p)

    # Handle invalid cases
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
    
    # Calculate how many pages are needed to load the process.
    num_of_pages = math.ceil(n / tamañoDePagina)

    # Frames used.
    frames = []

    paginasProcesos[p] = {}
    # Save process start time
    paginasProcesos[p]["start_time"] = current_time
    i = 0
    current_page = 0
    while current_page < num_of_pages:

        # If there are no empty frames and
        # the process hasn't been loaded completely.
        if i >= memoria and current_page < num_of_pages:
            
            next_frame = chooseNext()

            swapped = swap(current_page,p,next_frame)
            if not swapped:
                return
            
            # Store loaded frame to display and store
            frames.append(math.floor(next_frame/tamañoDePagina))

            # Adds a swap in operation
            total_swaps += 1

            current_page += 1
            
            
        # Find first/next empty frame.
        while i < memoria:
            if M[i] == None:
                # Store loaded frame to display and store
                frames.append(math.floor(i/tamañoDePagina))
                paginasProcesos[p][current_page] = i
                if(algoritmo):
                    # If using fifo, add each used frame into the fifo queue
                    fifo_next_swap.insert(0, i)
                else:
                    # If using lru, add each frame into the lru queue 
                    lru_next_swap.insert(0, i)
                # Load to this frame.
                loadPageToFrame(i, p, current_page)

                # Updates time, loading page to memory takes 1s
                current_time += 10

                current_page += 1
                break
            # Move to next frame.
            i += tamañoDePagina

    print("Se asignaron los marcos de página", frames, "al proceso", p)

def L(p):
    global fifo_next_swap, lru_next_swap, paginasProcesos, swapped_pages, current_time
    print ("Liberar los marcos de página ocupados por el proceso ", p)
    if (paginasProcesos[p] == None):
        print ("El proceso ", p, " no se ha ejecutado")
        print("No se ejecutará esta instrucción")
        return
    if "end_time" in paginasProcesos[p]:
        print ("El proceso ", p, " ya fue liberado")
        print("No se ejecutará esta instrucción")
        return
    # Frees up M
    pages = paginasProcesos[p]

    for key in pages:
        if key!= "start_time":
            loadPageToFrame(pages[key],None, None)

    if algoritmo:
        # Free up fifo queue of p's frames, only keeps frames that are not in the
        #  process being freed up
        fifo_next_swap = [i for i in fifo_next_swap if i not in pages.values()]
    else:
        # free up lru queue of p's frames, only keeps frames that are not in the 
        #  process being freed up
        lru_next_swap = [i for i in lru_next_swap if i not in pages.values()]

    page_frames = [math.floor(pages[i]/tamañoDePagina ) for i in pages.keys() if i != 'start_time']
    print ("Se liberan los marcos de página de memoria real:", page_frames)

    # Frees up S
    swapped = {}
    if p in swapped_pages:
        swapped = swapped_pages[p]

        for key in swapped:
            loadPageToSwap(swapped[key], None, None)

        swapped_page_frames = [math.floor(i/tamañoDePagina) for i in swapped.values()]
        print ("Se liberan los marcos", swapped_page_frames, "del área de swapping")
        del swapped_pages[p]

    # Update time, for each page freed up in memory and swapped, 0.1s pass ,(-1 because of "start_time")
    current_time += (len(pages) + len(swapped) - 1) 

    # Store current time for turnaround
    paginasProcesos[p]["end_time"] = current_time

def E():
    print("Fin de las instrucciones")
    exit()

def F():
    global paginasProcesos, swapped_pages, lru_next_swap, fifo_next_swap, page_faults, total_swaps, current_time
    # Number of processes counted
    processes = 0
    # Variable to store current sum and then divide to calculate verage
    average_turn_around = 0
    if len(paginasProcesos) == 0:
        print("No se tienen procesos en memoria.")
        print("No se pueden calcular el reporte de estadísticas.")
        return
     
    check_values = [i for i in paginasProcesos if "end_time" not in paginasProcesos[i] ]
    if len(check_values) > 0:
        print("Liberando procesos que aun siguen corriendo para calcular reporte de estadísticas.")
        print()
        # Turnaround time
        for key in sorted(check_values):
            if "end_time" not in paginasProcesos[key] :
                print("L(", key, ")")
                L(key)
                print()

    print("Fin. Reporte de salida: ")
    for key in sorted(paginasProcesos.keys()):

        processes += 1
        current_turn_around = (paginasProcesos[key]["end_time"] - paginasProcesos[key]["start_time"])/10

        print("Proceso: ", key, "\t Turnaround time: ", current_turn_around, ".", sep="")
        
        average_turn_around += current_turn_around
    
    average_turn_around = average_turn_around / processes
    
    # Avg turnaround
    print("Turnaround promedio: ", average_turn_around, sep="")

    # Page faults per process (when page not in memory is needed, NOT FROM P)
    print("Page faults: ", page_faults, sep="")

    # Amount of Swap in / swap out operations
    print("Operaciones de swap in/swap out: ", total_swaps, sep="")

    # Reset variables
    
    # Queues
    if algoritmo:   
        # Queue of pages used for FIFO Strategy
        fifo_next_swap = []
    else:     
        # Queue of pages used for LRU Strategy
        lru_next_swap = []
    
    # Memory
    M = [None] * memoria
    # Swapping area
    S = [None] * memoriaSwap
    
    # dictionaries
    swapped_pages = {}
    paginasProcesos = {}

    # Data for statistics

    # Current time for measurments
    current_time = 0
    # Amount of page faults that have occured
    page_faults = 0
    # Amount of swap in / swap out operations
    total_swaps = 0

def C(comentario):
    print("el camentario es: ",comentario)