import sqlite3
import json
import time

conn = sqlite3.connect('footballhub.sqlite3')

def import_json():
    data = json.load(open('data.json', 'r'))

    for equipo in data['equipos']:
        sql = 'INSERT INTO  Equipos (nombre,estadio,champions_copa,logo,presidente,entrenador) VALUES (?,?,?,?,?,?)'
        valores = [equipo['nombre'], equipo['estadio'], equipo['champions_copa'], equipo['logo'], equipo['presidente'], equipo['entrenador']]
        cursor = conn.execute(sql, valores)
        conn.commit()

    for jugador in data['jugadores']:
        sql = 'INSERT INTO  Jugadores (nombre,apellido,altura,posicion,peso,foto,edad) VALUES (?,?,?,?,?,?,?)'
        valores = [jugador['nombre'], jugador['apellido'], jugador['altura'], jugador['posicion'], jugador['peso'], jugador['foto'], jugador['edad']]
        cursor = conn.execute(sql, valores)
        conn.commit()


def reset_tables():
    sql = 'DELETE FROM Equipos'
    cursor = conn.execute(sql)

    sql = 'DELETE FROM Jugadores'
    cursor = conn.execute(sql)

    conn.commit()

def show_equipos():
    print('-- Equipos --')
    sql = 'select * from Equipos'
    cursor = conn.execute(sql)

    for row in cursor:
        print('id:', row[0])
        print('nom:', row[1])
        print('jugadores:', row[2])
        print('estadio:', row[3])
        print('champions_copa:', row[4])
        print('logo:', row[5])
        print('presidente:',row[6])
        print('entrenador:', row[7])
        print("\n")

def show_jugadores():
    print('-- Jugadores --')
    sql = 'select * from jugadores'
    cursor = conn.execute(sql)
    """for row in rows:
        print(row)"""
    
    for row in cursor:
        print('id:', row[0])
        print('nombre:', row[1])
        print('equipo:', row[2])
        print('apellido:', row[3])
        print('altura:', row[4])
        print('posicion:', row[5])
        print('peso:', row[6])
        print('foto:',row[7])
        print('edad:', row[8])
        print("\n")

def delete_equipos():
    id = input("id?: ")
    sql = 'DELETE FROM Equipos WHERE id=?'
    valores = [id]
    conn.execute(sql,valores)
    conn.commit()

def delete_jugador():
    id = input("id?: ")
    sql = 'DELETE FROM Jugadores WHERE id=?'
    valores = [id]
    conn.execute(sql, valores)
    conn.commit()

def insert_equipo():
    nombre = input("Nombre del equipo: ")
    estadio = input("Nombre del estadio: ")
    champions_copa = input("Numero de champions ganados: ")
    logo = input("Inserta la url del logo: ")
    presidente = input("Presidente del club: ")
    entrenador = input("Nombre del entrenador del club: ")

    sql = 'INSERT INTO Equipos (nombre, estadio, champions_copa, logo, presidente, entrenador ) VALUES (?,?,?,?,?,?)'
    valores = [nombre, estadio, champions_copa, logo, presidente, entrenador]
    conn.execute(sql,valores)
    conn.commit()

def insert_jugador():
    nombre = input("Nombre del jugador: ")
    apellido = input("apellido del jugador: ")
    altura = input("Altura del jugador: ")
    posicion = input("Posicion que juega el jugador: ")
    peso = input("Peso del jugador: ")
    foto = input("Inserta la foto del jugador en url: ")
    edad = input("Edad del jugador: ")

    sql = 'INSERT INTO Jugadores (nombre, apellido, altura, posicion, peso, foto, edad ) VALUES (?,?,?,?,?,?,?)'
    valores = [nombre, apellido, altura, posicion, peso, foto, edad]
    conn.execute(sql, valores)
    conn.commit()

def update_equipo():
    id = int(input("id del usuario que quieres modificar los datos?:  "))
    nombre = input("Nombre del equipo: ")
    estadio = input("Nombre del estadio: ")
    champions_copa = input("Modificar numero de champions ganados: ")
    logo = input("Modificar la url del logo: ")
    presidente = input("Modificar presidente del club: ")
    entrenador = input("Modificar el entrenador del club: ")

    sql = 'UPDATE Equipos SET nombre = ?, estadio = ? , champions_copa=?, logo=?, presidente=?, entrenador=? WHERE id=?'
    valores = [nombre, estadio, champions_copa, logo, presidente, entrenador]
    conn.execute(sql,valores)
    conn.commit()

def update_jugador():
    pass

def main():
    while True:
        print("\nMenú principal:")
        print("1. Importar datos del json")
        print("2. Mostrar Equipos")
        print("3. Mostrar Jugadores")
        print("4. Resetear todas las tablas")
        print("5. Eliminar un equipo")
        print("6. Eliminar un jugador")
        print("7. Insertar un nuevo equipo")
        print("8. Insertar un nuevo Jugador")
        print("9. Modificar un equipo")
        print("10. Modificar un jugador")
        print("11. Salir")

        opcion = input("Ingrese su opción: ")
        if opcion == "1":
            import_json()
        elif opcion == "2":
            show_equipos()
        elif opcion == "3":
            show_jugadores()
        elif opcion == "4":
            reset_tables()
        elif opcion == "5":
            delete_equipos()
        elif opcion == "6":
            delete_jugador()
        elif opcion == "7":
            insert_equipo()
        elif opcion == "8":
            insert_jugador()
        elif opcion == "9":
            update_equipo()
        elif opcion == "10":
            update_jugador()
        elif opcion == "11":
            print("\nSaliendo....")
            time.sleep(2)
            break
        else:
            print("Opción inválida..")

if __name__ == '__main__':
    main()
