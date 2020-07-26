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
        lines = file.read().splitlines()

        for i, line in enumerate(lines):
            words = ' '.join(line.split()).split(' ') #Separa la linea en palabras
            if words[0] == 'A': #La primera palabra es la instruccion A?
                if(len(words) != 4): #A solo puede tener 4 palabras "A d p m"
                    print('ERROR: Numero incorrecto de argumentos ', i+1, '.', sep="") #Manda el error y pasa a la siguiente linea
                else:
                    instruccion = [words[0]]
                    try:
                        #Por cada palabra convierte los ultimos 3 argumentos en enteros ya que se pasan como string y los mete en una lista
                        instruccion.append(int(words[1])) 
                        instruccion.append(int(words[2]))
                        instruccion.append(int(words[3]))
                        if instruccion[3] not in [0,1]: #El argumento 3 o "m" solo puede ser un 0 o un 1
                            print("Error: El argumento 3 o no es un 0 o un 1 ", instruccion[3])
                        else:
                            listaDeInstrucciones.append(instruccion) #Añade la instruccion a la lista de instrucciones
                    except ValueError:
                        print("Uno de los argumentos ingresados es incorrecto")
                        exit()
        return listaDeInstrucciones