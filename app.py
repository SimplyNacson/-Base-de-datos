from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

# --- Configuración de la aplicación ---
app = Flask(__name__)
app.secret_key = 'your_secret_key'




# --- Configuración de la base de datos ---
db_config = {
    'host': 'localhost',
    'user': 'rooty',
    'password': 'password',
    'database': 'formulario'
}




# --- Funciones auxiliares ---
def insertar_usuario(nombre, email, contrasena):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO usuarios (nombre, email, contrasena) VALUES (%s, %s, %s)',
            (nombre, email, contrasena)
        )
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        flash('Error al insertar el usuario.')
    finally:
        conn.close()

def obtener_usuarios():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre, email FROM usuarios')
        usuarios = cursor.fetchall()
        return usuarios
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        flash('Error al obtener los usuarios.')
        return []
    finally:
        conn.close()





# --- Rutas principales ---
@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    nombre = request.form['nombre']
    email = request.form['email']
    contrasena = request.form['contrasena']

    if not nombre or not email or not contrasena:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('formulario'))

    insertar_usuario(nombre, email, contrasena)
    return redirect(url_for('exito'))

@app.route('/usuarios')
def mostrar_usuarios():
    usuarios = obtener_usuarios()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM usuarios WHERE id = %s', (id,))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        flash('Error al eliminar el usuario.')
    finally:
        conn.close()
    return redirect(url_for('mostrar_usuarios'))






# --- Rutas para actualizar usuario ---
@app.route('/actualizar_usuario/<int:id>', methods=['GET'])
def mostrar_formulario_actualizar_usuario(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('SELECT nombre, email FROM usuarios WHERE id = %s', (id,))
        usuario = cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        flash('Error al obtener los datos del usuario.')
        usuario = None
    finally:
        conn.close()

    if usuario:
        return render_template('actualizar_usuario.html', id=id, nombre=usuario[0], email=usuario[1])
    else:
        return redirect(url_for('mostrar_usuarios'))

@app.route('/actualizar_usuario/<int:id>', methods=['POST'])
def actualizar_usuario(id):
    nuevo_nombre = request.form['nuevo_nombre']
    nuevo_email = request.form['nuevo_email']
    nueva_contrasena = request.form['nueva_contrasena']

    if not nuevo_nombre or not nuevo_email or not nueva_contrasena:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('mostrar_formulario_actualizar_usuario', id=id))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE usuarios SET nombre = %s, email = %s, contrasena = %s WHERE id = %s',
            (nuevo_nombre, nuevo_email, nueva_contrasena, id)
        )
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        flash('Error al actualizar el usuario.')
    finally:
        conn.close()

    return redirect(url_for('mostrar_usuarios'))







# --- Ruta de éxito ---
@app.route('/exito')
def exito():
    return render_template('exito.html')

# --- Ejecutar la aplicación ---
if __name__ == '__main__':
    app.run(debug=True)