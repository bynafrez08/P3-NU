import sqlite3
import json
import hashlib

def register_user(username,password,email,name,surname):
    conn = sqlite3.connect('footballhub.sqlite3')
    sql = 'INSERT INTO users (username,password,email,name,surname) values (?,?,?,?,?)'
    valores = [username,password,email,name,surname]
    conn.execute(sql,valores)
    conn.commit()
    conn.close()

def add_user(username,password,email,name,surname,rol):
    conn = sqlite3.connect('footballhub.sqlite3')
    sql = 'INSERT INTO users (username,password,email,name,surname,rol) values (?,?,?,?,?,?)'
    valores = [username,password,email,name,surname,rol]
    conn.execute(sql,valores)
    conn.commit()
    conn.close()

def check_login(username,password):
    conn = sqlite3.connect('footballhub.sqlite3')
    cur = conn.cursor()
    cur.execute('SELECT username,password FROM users WHERE username=?', (username,))
    result = cur.fetchone()

    if result is not None:
        #obtener el valor de la columna contraseña ya que la contraseña esta en la posicion 1 de la bd (result[1]), y compararlo con la encriptada.
        hashed_password = result[1]
        # comparar el valor que pasa la variable "hashed_password" con la hasheada de la bd, si coinciden devuelve True y el usuario podra acceder a la pagina.
        if hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed_password:
            return True
    conn.close()
    return False

def delete_user(username):
    conn = sqlite3.connect('footballhub.sqlite3')
    cursor = conn.cursor()
    sql = 'DELETE FROM users WHERE username=?'
    valores = [username]
    cursor.execute(sql,valores)
    conn.commit()
    conn.close()

def user_perfil(username):
    conn = sqlite3.connect('footballhub.sqlite3')
    cur = conn.cursor()
    cur.execute('SELECT username,email,name,surname FROM users WHERE username=?',(username,))
    # obtener el resultado de la consulta
    row = cur.fetchone()
    conn.close()

    # si no encuentra el usuario devuelve None
    if row is None:
        return None
    else: # en caso contrario devuelve los siguientes campos.
        return {
            'username': row[0],
            'email': row[1],
            'name': row[2],
            'surname': row[3]
        }

def insertar_jugador(nombre,apellido,altura,posicion,peso,foto,edad,equipo):
    conn = sqlite3.connect('footballhub.sqlite3')
    sql = 'INSERT INTO Jugadores (nombre, apellido, altura, posicion, peso, foto, edad, equipo ) VALUES (?,?,?,?,?,?,?,?)'
    valores = [nombre, apellido, altura, posicion, peso, foto, edad, equipo]
    conn.execute(sql,valores)
    conn.commit()
    conn.close()


def insertar_equipo(nombre,jugadores,estadio,champions_copa,logo,presidente,entrenador):
    conn = sqlite3.connect('footballhub.sqlite3')
    sql = 'INSERT INTO Equipos (nombre,jugadores,estadio,champions_copa,logo,presidente,entrenador) VALUES (?,?,?,?,?,?,?)'
    valores = [nombre,jugadores,estadio,champions_copa,logo,presidente,entrenador]
    conn.execute(sql,valores)
    conn.commit()
    conn.close()


def show_jugadores(id_jugadores=None):
    conn = sqlite3.connect('footballhub.sqlite3')
    sql = 'SELECT DISTINCT j.id, j.nombre, j.apellido, j.altura, j.posicion, j.peso, j.edad, j.foto, e.nombre FROM jugadores as j JOIN equipos as e ON (j.equipo = e.id)'
    if id_jugadores is not None:
        sql += ' WHERE j.id=' + id_jugadores
    cursor = conn.execute(sql)

    jugadores = []

    for row in cursor:
        jugador = {
            'id': row[0],
            'nombre': row[1],
            'apellido': row[2],
            'altura': row[3],
            'posicion': row[4],
            'peso': row[5],
            'edad': row[6],
            'foto': row[7],
            'equipo': row[8]
        }
        jugadores.append(jugador)
    conn.close()
    return jugadores


def show_users():
    conn = sqlite3.connect('footballhub.sqlite3')
    cursor = conn.execute('SELECT username, email, name, surname, rol FROM users')

    users = []

    for row in cursor:
        user = {
            'username': row[0],
            'email': row[1],
            'name': row[2],
            'surname': row[3],
            'rol': row[4]
        }
        users.append(user)
    conn.close()
    return users

def show_equipos(id_equipos=None):
    conn = sqlite3.connect('footballhub.sqlite3')
    #sql = 'SELECT DISTINCT id, nombre, jugadores, estadio, champions_copa, logo, presidente, entrenador FROM equipos;'
    sql = 'SELECT DISTINCT e.id, e.nombre, j.nombre , e.estadio, e.champions_copa, e.logo, e.presidente, e.entrenador FROM Equipos as e JOIN jugadores as j ON (e.jugadores = j.id)'
    if id_equipos is not None:
        sql += ' WHERE e.id=' + id_equipos
    cursor = conn.execute(sql)

    equipos = []

    for row in cursor:
        equipo = {
            'id': row[0],
            'nombre': row[1],
            'jugadores': row[2],
            'estadio': row[3],
            'champions_copa': row[4],
            'logo': row[5],
            'presidente': row[6],
            'entrenador': row[7],
        }
        equipos.append(equipo)
    conn.close()
    return equipos

def api_jugador(id):
    conn = sqlite3.connect('footballhub.sqlite3')
    cursor = conn.execute('SELECT id, nombre, apellido, altura, posicion, peso, edad, foto FROM jugadores WHERE id = ?',(id,))

    jugadores = []

    for row in cursor:
        jugador = {
            'id' : row[0],
            'nombre': row[1],
            'apellido': row[2],
            'altura': row[3],
            'posicion': row[4],
            'peso': row[5],
            'edad': row[6],
            'foto': row[7]
        }
        jugadores.append(jugador)
    conn.close()
    return jugador

def api_equipos(id):
    conn = sqlite3.connect('footballhub.sqlite3')
    cursor = conn.execute('SELECT DISTINCT id, nombre, jugadores, estadio, champions_copa, logo, presidente, entrenador FROM equipos WHERE id = ?',(id,))

    equipos = []

    for row in cursor:
        equipo = {
            'id': row[0],
            'nombre': row[1],
            'jugadores': row[2],
            'estadio': row[3],
            'champions_copa': row[4],
            'logo': row[5],
            'presidente': row[6],
            'entrenador': row[7],
        }
        equipos.append(equipo)
    conn.close()
    return equipo

def del_jugador(id):
    conn = sqlite3.connect('footballhub.sqlite3')
    sql = 'DELETE FROM jugadores WHERE id= ?'
    values = [id]
    conn.execute(sql,values)
    conn.commit()
    conn.close()

def del_equipo(id):
    conn = sqlite3.connect('footballhub.sqlite3')
    sql = 'DELETE FROM equipos WHERE id= ?'
    values = [id]
    conn.execute(sql,values)
    conn.commit()
    conn.close()

def modify_jugador(id_jugadores,nombre,apellido,altura,posicion,peso,foto,edad,equipo):
    conn = sqlite3.connect('footballhub.sqlite3')
    sql = 'UPDATE jugadores SET nombre=?, apellido=?,altura=?,posicion=?,peso=?,foto=?,edad=?,equipo=? WHERE id=?'
    valores = [nombre,apellido,altura,posicion,peso,foto,edad,equipo,id_jugadores]
    conn.execute(sql,valores)
    conn.commit()
    conn.close()


def modify_equipo(nombre,jugadores,estadio,champions_copa,logo,presidente,entrenador,id_equipos):
    conn = sqlite3.connect('footballhub.sqlite3')
    sql = 'UPDATE equipos SET nombre=?, estadio=?,champions_copa=?,logo=?,presidente=?,entrenador=?, jugadores=? WHERE id=?'
    valores = [nombre,jugadores,estadio,champions_copa,logo,presidente,entrenador,id_equipos]
    conn.execute(sql,valores)
    conn.commit()
    conn.close()