# *Proyecto Final - Simulador de Memoria*
---
#### Materia: *Sistemas Operativos*

##### Integrantes:
1. *CHRISTOPHER LUIS MIRANDA VANEGAS* - *A01022676* - *Campus Santa Fe*
2. *Miguel Alejandro Hernandez Garcia* - *A01654722* - *Campus Ciudad de México*
3. *Jesús Aristóteles Pacheco Ramírez* - *A001262378* - *Campus Guadalajara*

---
## 1. Aspectos generales

Las orientaciones de la tarea se encuentran disponibles en el siguiente link https://github.com/ChristopherMiranda00/Simulador-Memoria

Este documento es una guía sobre qué información debe entregar como parte del proyecto, y la estructura que debe seguir para organizar su entrega.

### 1.1 Objetivo
Ejercicio de programación para mostrar su comprensión de algunos de
los algoritmos de administración de memoria vistos en clase


### 1.2 Estructura del repositorio

El proyecto debe seguir la siguiente estructura de carpetas, la cual generamos por usted:
```
- /  # Raíz de todo el proyecto
    - README.md			    # Archivo con los datos del proyecto (este archivo)
    - Proyecto Final-1.pdf	# Documento PDF con los instrucciones del documento 
    - analizador.py			# Programa que realiza las operaciones
    - main.py		        # Programa con los incisos de las intrucciones
    - pasos.py		        # Programa que maneja instrucciones generales
    - Reportes              # Reportes y comparación con los diferentes algoritmos
    - prueba.txt            #Archivo con las instrucciones que usamos como prueba 
```

### 1.3 Como correr el proyecto

Contar en tu computadora con python, de ser necesario instalarlo de [aquí](https://python.uptodown.com/windows).

1. Primero, se necesita clonar el repositorio, con el siguiente comando:

   ```
    git clone https://github.com/ChristopherMiranda00/Simulador-Memoria
    ```

    Una vez que se haya descargado el repositorio, se tendrán la carpeta de manera local con los siguientes archivos:
     
     - Proyecto Final-1.pdf
     - analizador.py
     - pasos.py
     - main.py
     - prueba.txt
     - Reportes

    También el [README.md](README.md) que se encuentra en la carpeta raíz.


2. Una vez que tenga el repositorio en su computadora, abrir la carpeta del proyecto en una terminal nueva. 
  
 
3. En la terminal escribir el siguiente comando y darle enter:

      `
      main.py (algoritmo a usar, fifo o lru)
      `
  
      Ejemplo: 
      
          
          main.py lru 
          

 4. El programa pedirá un archivo de instruciones, se tiene que arrastrar el archivo `prueba.txt` a la terminal cuando este sea pedido .

 5. El programa empezará a correr y se mostrará el output pedido. 
 
 ## 2. Información adicional de los programas: 
 
 1. Lenguaje de programación utilizado: `python 3.7.5 `
 
 2. Número de total de líneas de los programas: 
    - main.py `34 líneas`
    - analizador.py `89 líneas`
    - pasos.py `359 líneas`
    - prueba.txt `11 líneas`
 
 3. Número total de lneas sin comentarios ni espacios de los programas :
    - main.py `28 líneas`
    - analizador.py `64 líneas`
    - pasos.py `231 líneas`
    - prueba.txt `11 líneas`
 
 
 ## 3. Reporte con la comparación de algoritmos 
 
1. Para acceder a las imágenes se necesita accesar a la carpeta de `Reporte`

2. Dentro de la carpeta aparecen 6 imágenes:
```
    - FIFO1.jpeg
        Ejemplo de como correr con el algoritmo FIFO. 
    - FIFO2.jpeg
        El despliegue de datos por algoritmo FIFO.
    - FIFO3.jpeg
        Estadisticas del programa (TURNAROUND, FALLOS DE PAGINA, NUMERO DE OPERACIONES DE SWAP).
    - LRU1.jpeg
        Ejemplo de como correr con el algoritmo LRU. 
    - LRU2.jpeg
        El despliegue de datos por algoritmo LRU.
    - LRU3.jpeg
        Estadisticas del programa (TURNAROUND, FALLOS DE PAGINA, NUMERO DE OPERACIONES DE SWAP).
```
    
    

 
