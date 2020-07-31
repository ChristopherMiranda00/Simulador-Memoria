import os

def instrucciones():
    listaDeInstrucciones = [] #Lista de Instrucciones
    #Introduccir PATH de las instrucciones
    entrada = input('Direccion del archivo de instrucciones:')
    path = entrada.rstrip('\r') #Quita todo lo que ocasiones un retorno de carro

    # Check that instruction file exists before parsing
    if not os.path.isfile(path):
        print('La direccion no existe')
        exit()
    
    with open(path) as file: #Abre el PATH como un File
        #Lee el arhivo y lo separa en lineas 
        filas = file.read().splitlines()

        for i, fila in enumerate(filas):
            secciones = ' '.join(fila.split()).split(' ') #Separa la linea en secciones para despues convertir cada seccion a su formato
            if secciones[0] == 'A': #La primera palabra es la instruccion A?
                if(len(secciones) != 4): #A solo puede tener 4 palabras "A d p m"
                    print('ERROR: Numero incorrecto de argumentos') #Manda el error
                else:
                    instruccion = [secciones[0]]
                    try:
                        #Se intenta por cada palabra convierte los ultimos 3 argumentos en enteros ya que se pasan como string y los mete en una lista
                        instruccion.append(int(secciones[1])) 
                        instruccion.append(int(secciones[2]))
                        instruccion.append(int(secciones[3]))
                        if instruccion[3] not in [0,1]: #El argumento 3 o "m" solo puede ser un 0 o un 1
                            print("Error: El argumento 3 o no es un 0 o un 1 ", instruccion[3])
                        else:
                            listaDeInstrucciones.append(instruccion) #Añade la instruccion a la lista de instrucciones
                    except ValueError:
                        print("Uno de los argumentos ingresados es incorrecto")
                        exit()
            
            elif secciones[0] == 'P':
                #número de argumentos P "#asginar num bytes" "#num proceso"
                if(len(secciones) != 3):
                    print('ERROR: Numero incorrecto de argumentos ')
                else:
                    instruccion = [secciones[0]]
                    try: 
                        #Se intenta por cada palabra convierte los ultimos 2 argumentos en enteros ya que se pasan como string y los mete en una lista
                        instruccion.append(int(secciones[1])) 
                        instruccion.append(int(secciones[2]))
                        listaDeInstrucciones.append(instruccion) #Añade la instruccion a la lista de instrucciones
                    except ValueError:
                        print("Uno de los argumentos ingresados es incorrecto")
                        exit()
            
            elif secciones[0] == 'L':
                #L solo puede tener 2 palabras "L "#proceso p" "
                if(len(secciones) != 2):
                    print('ERROR: Numero incorrecto de argumentos')
                else:
                    instruccion = [secciones[0]]
                    try:
                        #Se intenta por cada palabra convierte el último  argumento en entero ya que se pasa como string y lo mete en una lista
                        instruccion.append(int(secciones[1]))
                        listaDeInstrucciones.append(instruccion) #Añade la instruccion a la lista de instrucciones
                    except ValueError:
                        print("Uno de los argumentos ingresados es incorrecto")
                        exit()


            elif secciones[0] == 'F': #última línea de un conjunto de solicitudes
                instruccion = [secciones[0]]
                #Añade la instruccion a la lista de instrucciones
                listaDeInstrucciones.append(instruccion)

            elif secciones[0] == 'E': #Exit, últime línea del archivo 
                instruccion = [secciones[0]]
                #Añade la instruccion a la lista de instrucciones
                listaDeInstrucciones.append(instruccion)

            elif secciones[0] == 'C': #Comentarios
                instruccion = [secciones[0]]
                #Junta los comentarios que posteriormente serán despledados
                instruccion.append(' '.join(secciones[1::]))
                #Añade la instruccion a la lista de instrucciones
                listaDeInstrucciones.append(instruccion)

            else:
                #En caso que la instrución sea diferentes a las anteriores =ERROR
                print('Error: Ingreso una instruccion inexistente')

        return listaDeInstrucciones