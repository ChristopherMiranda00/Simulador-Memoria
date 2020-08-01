# *Proyecto Final - Simulador de Memroia*
---
#### Materia: *Sistemas Operativos*

##### Integrantes:
1. *CHRISTOPHER LUIS MIRANDA VANEGAS* - *A01022676* - *Campus Santa Fe*
2. *Miguel Alejandro Hernandez Garcia* - *A01654722* - *Campus Ciudad de México
3. *Aristo* - *A0* - *Campus *

---
## 1. Aspectos generales

Las orientaciones de la tarea se encuentran disponibles en la plataforma **Canvas**.

Este documento es una guía sobre qué información debe entregar como parte del proyecto, qué requerimientos técnicos debe cumplir y la estructura que debe seguir para organizar su entrega.

### 1.1 Requerimientos técnicos

A continuación se mencionan los requerimientos técnicos mínimos del proyecto, favor de tenerlos presente para que cumpla con todos.

* El equipo tiene la libertad de elegir las tecnologías de desarrollo a utilizar en el proyecto, sin embargo, debe tener presente que la solución final se deberá ejecutar en una de las siguientes plataformas en la nube: [Google Cloud Platform](https://cloud.google.com/?hl=es), [Amazon Web Services](https://aws.amazon.com/) o [Microsoft Azure](https://azure.microsoft.com/es-mx/).
* El proyecto deberá utilizar una interfaz Web.
* La arquitectura deberá estar separada claramente por capas (*frontend*, *backend*, *API RESTful*, datos y almacenamiento) según se necesite.
* Todo el código, *datasets* y la documentación del proyecto debe alojarse en este repositorio de GitHub. Favor de mantener la estructura de carpetas propuesta.

### 1.2 Estructura del repositorio

El proyecto debe seguir la siguiente estructura de carpetas, la cual generamos por usted:
```
- / 			        # Raíz de todo el proyecto
    - README.md			# Archivo con los datos del proyecto (este archivo)
    - frontend			# Carpeta con la solución del frontend (Web app)
    - backend			  # Carpeta con la solución del backend (CMS)
    - api			      # Carpeta con la solución de la API
    - datasets		  # Carpeta con los datasets y recursos utilizados (csv, json, audio, videos, entre otros)
    - dbs			      # Carpeta con los modelos, catálogos y scripts necesarios para generar las bases de datos
    - docs			    # Carpeta con la documentación del proyecto

### 1.2 Estructura del repositorio

El proyecto debe seguir la siguiente estructura de carpetas, la cual generamos por usted:
```
- / 			        # Raíz de todo el proyecto
    - README.md			# Archivo con los datos del proyecto (este archivo)
    - frontend			# Carpeta con la solución del frontend (Web app)
    - backend			  # Carpeta con la solución del backend (CMS)
    - api			      # Carpeta con la solución de la API
    - datasets		  # Carpeta con los datasets y recursos utilizados (csv, json, audio, videos, entre otros)
    - dbs			      # Carpeta con los modelos, catálogos y scripts necesarios para generar las bases de datos
    - docs			    # Carpeta con la documentación del proyecto
```

### 1.3 Documentación  del proyecto

Como parte de la entrega final del proyecto, se debe incluir la siguiente información:

* Descripción del problema a resolver.
* Diagrama con la arquitectura de la solución.
* Descripción de cada uno de los componentes de la solución.
* Guía de configuración, instalación y despliegue de la solución en la plataforma en la nube seleccionada.
* Documentación de la API. Puede ver un ejemplo en [Swagger](https://swagger.io/). 
* El código debe estar documentado siguiendo los estándares definidos para el lenguaje de programación seleccionado.

## 2. Descripción del proyecto

Como proyecto final para la materia de *Análisis y diseño de algoritmos*, se nos solicitó hacer una aplicación web en la cual un usuario pueda ver como funcionan diferentes algoritmos y las características de ambos, tanto de ordenamiento como de búsqueda.

Los algoritmos que se presentarán en las búsquedas son 2:

•Secuencial .

•Binaria.

Y los algoritmos de ordenamiento se dividirán en estables e inestables : 

•Ordenamiento de burbuja(Bubble Sort) .

•Ordenamiento de burbuja bidireccional (Cocktail Sort) .

•Ordenamiento por inserción (Insertion Sort) .

•Ordenamiento por casilleros (Bucket Sort) .

•Ordenamiento por cuentas (Counting Sort) .

•Ordenamiento por mezcla (Merge Sort) .

•Ordenamiento con árbol binario (Binary tree Sort) .

•Ordenamiento Radix (Radix Sort) .

•Ordenamiento Shell (Shell Sort) .

•Ordenamiento por selección (Selection Sort) .

•Ordenamiento por montículos (Heap Sort) .

•Ordenamiento rápido (Quick Sort)  .

Este proyecto cuenta con dos carpetas principales, un _frontend_ y un _backend_. Cada uno de estos aloja los documentos necesarios para poder correr la solución.

Al establecer conexión entre estas dos carpetas, se está mandando a llamar desde el backend, pero esto será explicado en su sección específica.

- **NOTA**
    - **No sé si haga falta algo de la descripción que quieran completar**
    - **La página aun no se encuentra desplegada, pero será actualizado cuando se haya desplegado.**

## 3. Solución

A continuación aparecen descritos los diferentes elementos que forman parte de la solución del proyecto.
