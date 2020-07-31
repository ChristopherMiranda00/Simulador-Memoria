import sys
from analizador import instrucciones
import pasos

def main():
    # Evita que ingreses argumentos invalidos o mas de los solicitados, sirve de proteccion
    if(len(sys.argv) < 2 or sys.argv[1] not in ['fifo', 'lru']):
        print('Forma: %s (fifo|lru)' % sys.argv[0])
        exit()
    print('Usando: ', sys.argv[1])
    #True es FIFO y FALSE es LRU
    pasos.algoritmo = True if sys.argv[1] == 'fifo' else False
    #Lista de instrucciones
    lista = instrucciones()
    for paso in lista:
        print("\n", ' '.join(str(x) for x in paso), sep="")
    #Añade las llamadas a cada instruccion, manda los argumentos correspondientes segun la misma instruccion
        if paso[0] == 'P': #Cargar un proceso
            pasos.P(paso[1], paso[2]) #Paso[1] = bytes a asignar, Paso[2] = proceso
        elif paso[0] == 'A': #Accesar la direccion virtual D del proceso P
            pasos.A(paso[1], paso[2], paso[3]) #Paso[1] = Direccion Virtual, Paso[2] = proceso, Paso[3] = Si es 0 solo lee la direccion, si es 1 se modifica Direccion Virtual
        elif paso[0] == 'L': #Liderar las paginas del proceso de P
            pasos.L(paso[1]) #Paso[1] = proceso
        elif paso[0] == 'F': #Final de solucitud
            pasos.F()
        elif paso[0] == 'E': #Final del programa
            pasos.E()
        elif paso[0] == 'C':
            pasos.C(paso[1]) #paso[1] es un string
        elif paso[0] != 'C': #Comentarios
            print("No es una instruccion")
            exit()

main()