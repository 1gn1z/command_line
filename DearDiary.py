# Importamos datetime para el manejo de las fechas.
# Sys para salir del programa
# Getpass para pedir al usuario la contraseña usando un método seguro
# OrderedDict para usar un diccionari ordenado (en el menú)
# Peewee para el manejo de las tables de la base de datos (sqlite3)

# Importamos pyfiglet, para hacer banners :3
from pyfiglet import Figlet


import datetime
import sys
import getpass
from collections import OrderedDict

from peewee import *


# Creamos la base de datos, llamada "diary.db", y almacenada el la variable "db"
db = SqliteDatabase('diary.db')

#------------------------------------------------------------------------------------------------------------------------------------

# Clase de Entrada. 
# Variable "content" igual a textfield, que será el contenido de esa entrada del diario.
# Variable "timestamp" igual a un datetime.datetime.now para que la entrada se guarde con esa fecha y hora en la que fue guardada.

# Clase META: Dentro de la clase Entry, database es igual a "db", que es la base de datos que creamos anteriormente

class Entry(Model):
    """Create the table 'Entry', whit their respective fields:
    'content' and 'timestamp'"""
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

#------------------------------------------------------------------------------------------------------------------------------------

# Conexion de la base de datos y creacion de tablas.
# db.connect() hace la conexion a la base de datos.
# db.create_tables. Crea la tabla de la base de datos, mapeandola desde la clase "Entry" via Peewwee :3


def create_n_connect():
    """Connects to the database and create the tables"""
    db.connect()
    db.create_tables([Entry], safe=True)

#------------------------------------------------------------------------------------------------------------------------------------

# Creacion del menu.
# choice = None, la opcion que nos pase el usuario.
# mientras la opcion sea diferente de 'q':

# iteracion con bucle for de las llaves y valores del dicccionairo ordenado que despliga las opciones del menu.
# accedemos a los items del menu, menu.items que son los datos por los que itera el bucle FOR.

# Imprimimos la llave (la letra de la eleccion), y el DOCSTRING (__doc__) del valor, que es el nombre de las funciones, de las cuales
# se toma el docstring de las funciones, que es la descripcion de la opcion (add entry, view entries, etc.)

def menu_loop():
    """Show Menu"""
    choice = None
    while choice != 'q':
        for key, value in menu.items():

            print((f'{key}) {value.__doc__}'))
        choice = input('\nAction: ').lower().strip()

        if choice in menu:
            menu[choice]()

#------------------------------------------------------------------------------------------------------------------------------------

# Funcion para añadir una entrada al diario
# prints de instrucciones, en Windows hay que hacer ctri + z para el final del uso del teclado.

# data, con sys.stdin.read, vamos a aceptar TODOO lo que el usuario escriba, y se almacena en esta variable "data"

# if data:, si en data hay algo, es decir si data NO esta vacia:

# con un if aninado, preguntamos al usuario si quiere guardar la entrada, y le quitamos los espacios con strip y la convertimos
# a minusculas, para poder compararla sin ningun problema en nuestro condicional.

# Si el condicional anterior se cumple, es decir, si el usuario indica que SI quiere guardar, guardamos la entrada con nuestra
# clase (tabla) "Entry", y usamos su método "create".

# E indicamos en sus parametros que el contenido "content" es igual a "data", osea lo que el usuario escribio.

def add_entry():
    """Add entry"""
    print("\nEnter your toughts.")
    print("Press ctrl + Z on Windows or ctrl + D on Mac to finish\n")
    data = sys.stdin.read().strip()

    if data:
        if input("\nDo you want to save your entry? [Y/n] "
                 ).lower().strip() != 'n':
            Entry.create(content=data)
        print("\nYour entry was saved succesfully\n")

#------------------------------------------------------------------------------------------------------------------------------------

# Funcion para ver las entradas, y acepta como parametro el "search_query", que el usuario busque via texto.
# entries. Con select() manejamos TODOS los registros de la tabla.
# y con ordered by, ordenamos con su fecha, de manera descendente, de la mas nueva a la mas antigua

# Si hay datos en la search_query, las entradas seran igual a las mismas, donde la entrada (Entry, sea la que sea), contenga "contains"
# el search query.

# Con un ciclo for, iteramos en todas las entradas, para irlas mostrando.

# timestamp, es igual a la fecha de la entrada (entry.timestamp). Y con strftime le damos formato a la fecha.

# print('-'*len(timestamp)). Se muestra el caracter '-', de la longitud (len), del timestam, caracteres usados de separador

# imprimimos el timestamp de la entrada
# imprimimos el contenido de la entrada
# cerramos con una nueva impresion del caracter - usado de separador

# Imprimimos varias opciones (next entry, delete entry, edit entry y return to  menu)

# Siguiente accion "next_action" = pedimos al usuario la opcion, le quitamos los espacios de delante y atras con strip y la volvemos minuscula
# para poder compararla sin nungun problema en nuestras condicionales.

# Si la siguiente accion "next_action" es igual a "q".
# dejamos unos espacios y con break terminamos el ciclo.

# si "next_action" = d, llamamos a la funcion que borra la entrada "delete_entry"

def view_entries(search_query=None):
    """View all entries"""
    entries = Entry.select().order_by(Entry.timestamp.desc())

    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        timestamp = entry.timestamp.strftime('%d/%m/%Y %A  %I:%M%p')
        print()
        print('-'*len(timestamp))
        print('\n')
        print(timestamp)
        print('\n')
        print(entry.content)
        print('\n')
        print('-'*len(timestamp))
        print()
        print('n) next entry')
        print('d) delete entry')
        print('e) edit entry')
        print('q) return to menu')

        next_action = input('Action: [Ndeq] ').lower().strip()
        if next_action == 'q':
            print('\n\n')
            break
        elif next_action == 'd':
            delete_entry(entry)

# Llamada a la funcion "edit_entry", para guardar la edicion.        
        # elif next_action == 'e':
        #     edit_entry(entry)

#------------------------------------------------------------------------------------------------------------------------------------
# Funcion view_entries_date.
# funciona exactamente iguak que la anterior (view_entries). PERO! con esta funcion podemos buscar por fecha, no por texto.

def view_entries_date(search_dates=None):
    """View all entries"""

    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_dates:
        entries = entries.where(Entry.timestamp.contains(search_dates))

    for entry in entries:
        timestamp = entry.timestamp.strftime('%d/%m/%Y %A  %I:%M%p')
        print()
        print('-'*len(timestamp))
        print('\n')
        print(timestamp)
        print('\n')
        print(entry.content)
        print('\n')
        print('-'*len(timestamp))
        print()
        print('n) next entry')
        print('d) delete entry')
        print('e) edit entry')
        print('q) return to menu')

        next_action = input('Action: [Ndq] ').lower().strip()

        if next_action == 'q':
            print('\n\n')
            break

        elif next_action == 'd':
            delete_entry(entry)

# Llamada a la funcion "edit_entry", para guardar la edicion.        

        # elif next_action == 'e':
        #     edit_entry(entry)

#------------------------------------------------------------------------------------------------------------------------------------

# FUNCIONES 

# Funcion para buscar entradas.
# el search_query es igual a lo que introduzca (input) el usuario.
# llamamos a la funcion "view_entries", que acepta como párametro el search query.

def search_entries():
    """Search entries"""
    search_query = input('Search query: ').strip()
    view_entries(search_query)


# Funcion para buscar entradas por fecha.
# funciona igual que la anterior "search_entries", aceptando como párametro el search_dates.

def search_dates():
    """Search by dates"""
    search_dates = input('Search date: ')
    view_entries_date(search_dates)


# Funcion para eliminar una entrada.
# Preguntamos al usuario si esta seguro que quiere borrar la entrada, y pide una confirmacion.

# Si la accion es estrictamente igual a 'y', borramos la entrada usando el método "delete_instance()" (entre.delete_instance)

def delete_entry(entry):
    """Delete an entry"""
    action = input('Are you sure you want to delete this entry? [Y/n] '
                   ).lower().strip()

    if action == 'y':
        entry.delete_instance()


# Funcion para editar una entrada.
# Los datos "data" son los correspondientes a esa entrada en particular.
#
# Si hay "data" (el contenido de la entrada).
# Preguntamos con un "if input", al usuario si quiere guardar la edicion, si la opcion es diferente de 'n', guardamos el edit

# entry.update(content=data). Con el metodo update se actualizan los datos, y el contenido "content=data" es igual a la edicion
# de la entrada.

# Imprimimos un mensaje que la edicion se guardo satisfactoriamente.


# def edit_entry(entry):
#     """Edit an Entry"""
#     data = sys.stdin.read().strip()

#     if data:
#         if input("\nDo you want to save your edition? [Y/n] ").lower().strip() != 'n':
#             entry.update(content=data)
#             print()
#             print('Edit save succesfully')
#             print("\n")


# Funcion de validacion, simplemente retorna la cadena indicada que es el password para poder acceder al diario.

def validation(password):
    return password == 'XX531'

# Funcion quit, para quitar el programa
# action, le dice al usuario que si esta seguro de salir del programa.
# Si la accion es igual a 'y', salimos del programa, con la funcion "sys.exit", parte del modulo "sys"
# Si no, nos devuelve al menú.


def quit():
    """Quit program"""
    action = input('Are you sure you want to EXIT the program? [Y/n] '
                   ).lower().strip()

    if action == 'y':
        sys.exit(1)
    else:
        print('\n\n')
        menu_loop()

#------------------------------------------------------------------------------------------------------------------------------------

# Menu con el diccionario ordenado

# EL menu lo hicimos con un diccionario ordenado "OrdederDict".
# La llave del diccionario son las letras. 
# Y para mostrar el ordered dict de las clases que representas las letras, simplemente llamamos al nombre de la funcion (que es
# el valor de la llave del diccionario, la letra que lo representa), ya que anteriormente definimos que lo que se imprimira 
# es el docstring de la funcion (print((f'{key}) {value.__doc__}')), de nuestra funcion "menu_loop"


menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries and view_entries_date),
    ('s', search_entries),
    ('x', search_dates),
#    ('e', edit_entry),      # Añadimos la opcion de editar la edicion
    ('q', quit)
])

#------------------------------------------------------------------------------------------------------------------------------------

# Comprobamos que el modulo no se pueda importar, con if name = main de la primera linea de este bloque

#   if __name__ == '__main__':

# Verificacion que el password sea el correcto, dando 3 intentos al usuario de ingresar la contraseña correcta.
# intentos "tries" = 0
# mientras intentos sea menor que 3
# a intentos le sumamos 1
#
# password igual a getpass. 
# La funcion getpass del metodo del mismo nombre permite recibir el pass de modo seguro (no se ve lo que se esta typeando).
# imprimimos una bienvenida, una indicacion al usuario que necesita una contraseña y mostrar el intento

# Si la "validation" que acepta de parametro "password", es decir si la contraseña pasada es la correcta
# Y los intentos son menores que 3

# Imprimimos mensaje de bienvenida e indicamos que tiene acceso al diario.
# Y llamamos a las funciones "create_n_connect()" y "menu_loop()".

# Si los intentos son mayores o iguales a 3:
# imprimimos que la contraseña es incorrecta, y que un password es requerido para tener acceso al diario.
# finalmente salimos del programa con "sys.exit()"


# BANNER LISTO - Banner 'Dear Diary'


banner1 = Figlet(font='graffiti')
banner1_print = print(banner1.renderText('Dear Diary'))    # Simplemente lo imprimimos, para que se muestre al inicio



def validacion_e_ingreso():

    tries = 0
    while tries < 3:
        tries += 1
        password = getpass.getpass(
                                    '\nYou need a password to get acces :p\n'
                                    '\nTry #' + str(tries) + '\nPassword: ')

        if validation(password) and tries <= 3:
# BANNER2 

            banner2 = Figlet(font='doom')
            banner2_print = print(banner2.renderText('Welcome!!!'))    # Se imprime cuando ya hay acceso

#            print('\nWelcome!!!\n\nyou have acces to the diary :)\n')
            create_n_connect()
            menu_loop()
        elif tries >= 3:
            print('\nIncorrect password.\nPassword required to access diary\n')
            sys.exit(1)

if __name__ == '__main__':

    validacion_e_ingreso()
#------------------------------------------------------------------------------------------------------------------------------------


























