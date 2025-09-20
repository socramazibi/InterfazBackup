# InterfazBackup

# Backup Manager de Juegos

# Aplicación en Python con interfaz gráfica para crear y gestionar copias de seguridad de tus juegos de manera fácil y centralizada.

# 📝 Descripción

Este programa permite:

Crear copias de seguridad de cualquier juego.

Restaurar copias anteriores.

Eliminar copias que ya no necesites.

Abrir la carpeta del juego o la carpeta donde se guardan las copias.

Mantener un registro de copias por juego, mostrando únicamente las copias correspondientes al juego seleccionado.

Mostrar una barra de progreso al crear las copias.

Todas las ventanas emergentes (mensajes, diálogo de nombre, progreso) aparecen centradas en la aplicación para mejor visualización.

Cada copia se guarda en un archivo ZIP dentro de una carpeta con el nombre del juego, dentro de la carpeta de destino seleccionada por el usuario.

#

# ⚙️ Cómo funciona

Añadir un juego

Pulsa “Añadir juego”.

Introduce un nombre para el juego.

Selecciona la carpeta donde está instalado el juego.

Selecciona la carpeta donde se guardarán las copias.

El programa creará una subcarpeta con el nombre del juego en la carpeta de destino.

Seleccionar un juego

Haz clic en el juego en la lista de la izquierda.

Se habilitarán los botones de acción: abrir carpeta del juego, abrir carpeta de copias y crear copia.

Crear copia de seguridad

Pulsa “Crear copia”.

Aparecerá una ventana de progreso mostrando el avance de la copia.

Al finalizar, se añadirá la copia a la lista de copias del juego seleccionado.

Restaurar copia

Selecciona una copia de la lista de copias.

Pulsa “Restaurar copia”.

El contenido del ZIP reemplazará los archivos actuales del juego.

Eliminar copia

Selecciona una copia de la lista.

Pulsa “Eliminar copia” para borrarla permanentemente.

Abrir carpetas

Botones para abrir la carpeta del juego o la carpeta donde se guardan las copias directamente desde la aplicación.


# 💻 Requisitos

Python 3.7 o superior.

Librerías estándar:

tkinter (interfaz gráfica)

zipfile (compresión)

threading, os, shutil, datetime, json

#

# 🛠️ Uso

Ejecuta el programa con Python:

# 🧑‍💻 Créditos

ChatGPT (GPT-5): desarrollo del código, estructura del programa y funciones.

socramazibi: pruebas de la aplicación, sugerencias y mejoras en la interfaz y funcionalidades.

#

<img width="793" height="521" alt="imagen" src="https://github.com/user-attachments/assets/141bb59d-fd0b-4128-bc07-15f6ea6db31e" />


----------------------------------------------------------------------------------------------------------------------------------------


<img width="791" height="519" alt="imagen" src="https://github.com/user-attachments/assets/718e1f7e-b1fe-477c-9a62-6a70ae913e25" />

