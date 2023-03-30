from flask import Flask, render_template, redirect, url_for, jsonify, request, session, flash
import hashlib
import db_futbol
import sqlite3
from functools import wraps

##referencias:
    # https://www.youtube.com/watch?v=iIhAfX4iek0&list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX&index=5&ab_channel=TechWithTim
    # https://www.youtube.com/watch?v=qbnqNWXf_tU&list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX&index=6&ab_channel=TechWithTim
    # https://github.com/henry-richard7/Flask-Simple-Login-Sqlite3/blob/main/flask-app.py
    # https://www.youtube.com/watch?v=T1PLBEEZU8o&ab_channel=JulianNash (crear categorias con flash min: 12:40)
    # https://datagy.io/python-sha256/ https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python (encriptar la contraseña)

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'nafsu_secret_key'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'POST': # se envia los datos del formalario que proporciona el usuario por post, que es el usernama y password.
        username = request.form['username']
        password = request.form['password']

        # pasar los datos proporcionados del usuario en la funcion check_login para comprabar las credenciales desde la bd.
        if db_futbol.check_login(username,password):
            # la session se inicia con el campo username que da el usuario y se redirige a home.
            session['username'] = username
            return redirect(url_for('home'))
        else:
            # en la caso de que las credenciales son incorrectas.
            flash('Credenciales incorrectas', 'danger')
            return redirect(url_for('login'))
    else:
        return render_template('login.html') # si no se ha enviado ningun formulario vuelve a login.

@app.route('/home/', methods=['GET','POST'])
def home():
    # condicion para comprobar si el nombre de usuario esta en la session renderizar el index.html y pasarle el argumeto username. Y si no devuele al login.
    if 'username' in session:
        return render_template('index.html',username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/register/', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username  = request.form['username']
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        surname = request.form['surname']

        #encriptar la contraseña en la bd
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        db_futbol.register_user(username,hashed_password,email,name,surname)
        flash(f'Se ha creado el usuario {username}','success')
        return redirect(url_for('index'))

    else:
        return render_template('register.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session: # mostrar el siguiete mensaje si el usuario no haya iniciado la session.
            flash('Debes iniciar sesión para acceder a esta página.','danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/logout/')
def logout():
    # session.pop para eliminar la cookie de session.
    session.pop("username",None)
    return redirect(url_for("login"))

@app.route('/perfil/<username>/delete')
@login_required
def eliminar_usuario(username):
     # eliminar la cuenta y la cookie de session si el usuario ha iniciado correctamente la session. Si no redirige al login
    if 'username' in session:
       db_futbol.delete_user(username)
       session.pop('username', None)
       flash(f'Usuario {username} eliminado','success')
       return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/perfil/')
@login_required
def perfil():
    # si el usuario ha iniciado la sesion recuperamos el username de la sesion y mostrar la informacion del per que esta en al bd. en el caso contrario devuelve al login.
    if 'username' in session:
        username = session['username']
        valores = db_futbol.user_perfil(username)
        return render_template('perfil.html',valores=valores)
    else:
        return redirect(url_for('login'))

@app.route('/jugadores/')
@login_required
def jugadores():
    jugadores = db_futbol.show_jugadores()
    return render_template('jugadores.html', datos=jugadores)

@app.route('/jugadores/<id>/delete/')
@login_required
def del_jugador(id):
    db_futbol.del_jugador(id)
    return redirect(url_for('jugadores'))

@app.route('/api/jugadores/')
@login_required
def api_jugadores():
    jugadores = db_futbol.show_jugadores()
    return jsonify({'jugadores': jugadores})

@app.route('/api/jugadores/<int:id>/')
@login_required
def api_jugador(id):
    jugador = db_futbol.api_jugador(id)
    return jsonify({'jugador': jugador})

@app.route('/jugadores/<id>')
@login_required
def jugador(id):
    jugador = db_futbol.show_jugadores(id)
    return render_template('jugadores.html', datos=jugador)


@app.route('/jugadores/<id_jugadores>/modify/', methods=['GET','POST'])
@login_required
def modify_jugadores(id_jugadores):
    if request.method == 'GET':
        equipos = db_futbol.show_equipos()
        jugadores = db_futbol.show_jugadores(id_jugadores)

        return render_template('modify_jugadores.html', jugador=jugadores[0], equipos=equipos)

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        altura = request.form['altura']
        posicion = request.form['posicion']
        peso = request.form['peso']
        foto = request.form['foto']
        edad = request.form['edad']
        equipo = request.form['equipo']

        db_futbol.modify_jugador(id_jugadores,nombre, apellido, altura, posicion, peso, foto, edad, equipo)
        return redirect(url_for('jugadores'))


@app.route('/jugadores/insertar/', methods=['GET','POST'])
@login_required
def insertar_jugador():
    if request.method == 'GET':
        jugadores = db_futbol.show_jugadores()
        equipos = db_futbol.show_equipos()
        return render_template('insertar_jugador.html',jugadores=jugadores,equipos=equipos)

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        altura = request.form['altura']
        posicion = request.form['posicion']
        peso = request.form['peso']
        foto = request.form['foto']
        edad = request.form['edad']
        equipo = request.form['equipo']

        db_futbol.insertar_jugador(nombre,apellido,altura,posicion,peso,foto,edad,equipo)
        return redirect(url_for('jugadores'))

@app.route('/equipos/')
@login_required
def equipos():
    equipos = db_futbol.show_equipos()
    return render_template('equipos.html',datos=equipos)

@app.route('/equipos/<id>/delete/')
@login_required
def del_equipo(id):
    db_futbol.del_equipo(id)
    return redirect(url_for('equipos'))

@app.route('/api/equipos/')
@login_required
def api_equipos():
    equipos = db_futbol.show_equipos()
    return jsonify({'equipos': equipos})

@app.route('/api/equipos/<int:id>/')
@login_required
def api_equipo(id):
    equipo = db_futbol.api_equipos(id)
    return jsonify({'equipo': equipo})

@app.route('/equipos/insertar/', methods=['GET','POST'])
@login_required
def insertar_equipo():
    if request.method == 'GET':
        jugadores = db_futbol.show_jugadores()
        equipos = db_futbol.show_equipos()
        return render_template('insertar_equipo.html',jugadores=jugadores,equipos=equipos)

    if request.method == 'POST':
        nombre = request.form['nombre']
        jugadores = request.form['jugadores']
        estadio = request.form['estadio']
        champions_copa = request.form['champions_copa']
        logo = request.form['logo']
        presidente = request.form['presidente']
        entrenador = request.form['entrenador']

        db_futbol.insertar_equipo(nombre,jugadores,estadio,champions_copa,logo,presidente,entrenador)
        return redirect(url_for('equipos'))


@app.route('/equipos/<id_equipos>/modify/', methods=['GET','POST'])
@login_required
def modify_equipos(id_equipos):
    if request.method == 'GET':
        equipos = db_futbol.show_equipos(id_equipos)
        jugadores = db_futbol.show_jugadores()

        return render_template('modify_equipos.html', jugadores=jugadores, equipo=equipos[0])

    if request.method == 'POST':
        nombre = request.form['nombre']
        jugadores = request.form['jugadores']
        estadio = request.form['estadio']
        champions_copa = request.form['champions_copa']
        logo = request.form['logo']
        presidente = request.form['presidente']
        entrenador = request.form['entrenador']

        db_futbol.modify_equipo(id_equipos,nombre,jugadores,estadio,champions_copa,logo,presidente,entrenador)
        return redirect(url_for('equipos'))


if __name__ == '__main__':
    app.run(debug=True)
