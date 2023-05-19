from flask import Flask
from flask import render_template,request, redirect,url_for,session, flash
from flaskext.mysql import MySQL
from flask import send_from_directory
from datetime import datetime
import os

app=Flask(__name__)
# Base de datos con sql express/desarrollador
app=Flask(__name__)
app.secret_key="tienda"
mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='tienda'
mysql.init_app(app)
# ruta de inicio
@app.route("/")
def usuario():
    return redirect('/inicio')

@app.route("/inicio")
def usuario2():
    return render_template('sitio/index.html')
# Ruta para cerrar seccion
@app.route("/cerrar")
def cerrar():
    session.clear()
    return redirect('/')

# Ruta para iniciar sesion como admin
@app.route("/admin")
def admin():
    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente":
        return redirect('/')
    return render_template('admin/admin.html')

@app.route("/agrepro", methods=['POST'])
def agrepro():
    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente":
        return redirect('/')
    codigo = request.form['Codigo']
    nombre = request.form['Nombre']
    precio_compra = request.form['Prec']
    precio_venta = request.form['Prev']
    existencias = request.form['Existen']
    restriccion = request.form['Rest']
    _img=request.files['imagen']

    if _img.filename != '':
        _img.save(f"reTIEN\{_img.filename}")
        
    query = "INSERT INTO productos (codigo, Nombre, preciodecompra, preciodeventa, existencia, restriccion,imagen) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (codigo, nombre, precio_compra, precio_venta, existencias, restriccion,_img.filename)
    
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    return redirect('/agregar')

@app.route("/agreclie", methods=['POST'])
def agreclie():
    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente":
        return redirect('/')
    codigo = request.form['Codigo']
    nombre = request.form['Nombre']
    edad = request.form['Prec']
    Nombreusuario = request.form['Prev']
    Email = request.form['Existen']
    Contraseña = request.form['Rest']

        
    query = "INSERT INTO clientes (id, nombre, edad, usuario, correo, contra) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (codigo, nombre, edad, Nombreusuario, Email, Contraseña)
    
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    return redirect('/agregar2')

@app.route("/mostrar")
def mostrar():
    if not 'login' in session:
        return redirect('/')
        
    sql="SELECT * FROM `productos`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    productos=cursor.fetchall()
    conn.commit()
    return render_template('sitio/Productos.html',productos=productos)



@app.route("/mostcarr")
def mostcarr():
    if not 'login' in session:
        return redirect('/')

    sql="SELECT * FROM `carrito` WHERE Correo=%s;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql, session["correo"])
    carrito=cursor.fetchall()
    conn.commit()
    sql1="SELECT SUM(Total) FROM `carrito` WHERE Correo=%s"
    conn1=mysql.connect()
    cursor1=conn1.cursor()
    cursor1.execute(sql1, session["correo"])
    resultado = cursor1.fetchone()
    suma_total = resultado[0] if resultado[0] else 0

    conn1.commit()
    return render_template('sitio/carrito.html',carrito=carrito,suma_total=suma_total)


@app.route("/agregar")
def agre():
    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente":
        return redirect('/')
    sql="SELECT * FROM `productos`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    productos=cursor.fetchall()
    conn.commit()
    return render_template('admin/masprodad.html',productos=productos)

@app.route("/agregar2")
def agre2():
    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente":
        return redirect('/')
    sql="SELECT * FROM `clientes`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    productos=cursor.fetchall()
    conn.commit()
    return render_template('admin/mclientes.html',productos=productos)

@app.route("/cliente")
def clientes():

    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente":
        return redirect('/')
        
    sql="SELECT * FROM `clientes`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    productos=cursor.fetchall()
    conn.commit()
    return render_template('admin/mclientes.html',productos=productos)

@app.route("/ticket")
def ticket():

    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente":
        return redirect('/')
        
    sql="SELECT * FROM `ticket`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    productos=cursor.fetchall()
    conn.commit()
    return render_template('admin/mtick.html',productos=productos)

@app.route('/destroy/<int:id>')
def destroy(id):
    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente" or session["rango"]=="empleado":
        return redirect('/admin')
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM productos WHERE Codigo=%s",(id))
    productos=cursor.fetchall()
    conn.commit()
    return redirect('/agregar')

@app.route('/edid/<int:id>')
def edid(id):
    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente" or session["rango"]=="empleado":
        return redirect('/admin')
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE Codigo=%s",(id))
    productos=cursor.fetchall()
    conn.commit()
    return render_template('invet/edid.html',productos=productos)

@app.route("/act", methods=['POST'])
def act():
    if not 'login' in session:
        return redirect('/')
    
    if session["rango"]=="cliente" or session["rango"]=="empleado":
        return redirect('/')
    id=request.form['Codigo']
    _nom=request.form['Nombre']
    _prev=request.form['preciodecompra']
    _prec=request.form['preciodeventa']
    _exi=request.form['existencia']
    _rest=request.form['restriccion']
    _img=request.files['imagen']

    if _img.filename != '':
        _img.save(f"reTIEN\{_img.filename}")
        
    sql="UPDATE productos SET `Nombre`=%s, `preciodecompra`=%s, `preciodeventa`=%s, `existencia`=%s, `restriccion`=%s,`imagen`=%s WHERE codigo=%s ;"
    datos=(_nom,_prev,_prec,_exi,_rest,_img.filename,id)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/agregar')

@app.route("/act2", methods=['POST'])
def act2():
    if not 'login' in session:
        return redirect('/')
    
    if session["rango"]=="cliente":
        return redirect('/')
    id=request.form['Codigo']
    _nom=request.form['Nombre']
    _prev=request.form['preciodecompra']
    _prec=request.form['preciodeventa']
    _exi=request.form['existencia']
    _rest=request.form['restriccion']
    sql="UPDATE productos SET `Nombre`=%s, `preciodecompra`=%s, `preciodeventa`=%s, `existencia`=%s, `restriccion`=%s WHERE codigo=%s ;"
    datos=(_nom,_prev,_prec	,_exi,_rest,id)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/productoad')
#Actualizar clientes.
@app.route("/act3", methods=['POST'])
def act3():
    if not 'login' in session:
        return redirect('/')
    
    if session["rango"]=="cliente" or session["rango"]=="empleado":
        return redirect('/')
    id=request.form['id']
    _nom=request.form['nombre']
    _prev=request.form['edad']
    _prec=request.form['usuario']
    _exi=request.form['correo']
    _rest=request.form['contra']
    #_img=request.files['imagen']

    #if _img.filename != '':
    #    _img.save(f"reTIEN\{_img.filename}")
    sql="UPDATE clientes SET `nombre`=%s, `edad`=%s, `usuario`=%s, `correo`=%s, `contra`=%s WHERE id=%s ;"
    datos=(_nom,_prev,_prec,_exi,_rest,id)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/cliente')

@app.route('/agregacarrito', methods=['POST'])
def agregar_al_carrito():
     
     producto = request.form.get('producto')
     precio = request.form.get('precio')
     cantidad = request.form.get('cantidad')
     correo = session.get('correo')
     total = int(precio) * int(cantidad)
     conn=mysql.connect()
     cursor=conn.cursor()
     
     sql = "INSERT INTO carrito (Producto, Precio, Cantidad, Total, Correo) VALUES (%s, %s, %s, %s, %s)"
     values = (producto, precio, cantidad, total, correo)
     cursor.execute(sql, values)
     conn.commit()
     cursor.close()
     return "Producto agregado al carrito"


# Ruta de inicio de seccion correcto como admin
@app.route("/Loginadmin")
def Loginadmin():
    if 'login' in session and session.get('rango') == 'admin' or 'login' in session and session.get('rango') == 'empleado':
        return redirect('/admin')
    if 'login' in session and session.get('rango') == 'cliente':
        return redirect('/mostrar')
    return render_template('admin/loginadmin.html')
     
@app.route("/Loginadmin", methods=['POST'])
def ad_log():
    _corr = request.form['txtcorreo']
    _con = request.form['txtcontra']

    if _corr == '' or _con == "":
        flash('Recuerda llenar los datos de los campos')
        return render_template('admin/loginadmin.html')

    sql_admin = "SELECT * FROM `administrador` WHERE correo = %s;"
    sql_clientes = "SELECT * FROM `clientes` WHERE correo = %s;"
    sql_empleados = "SELECT * FROM `trabajador` WHERE correo = %s;"

    conn = mysql.connect()
    cursor = conn.cursor()

    # Consulta para administradores
    cursor.execute(sql_admin, (_corr,))
    admin_result = cursor.fetchall()

    # Consulta para usuarios
    cursor.execute(sql_clientes, (_corr,))
    usuario_result = cursor.fetchall()

     # Consulta para empleados
    cursor.execute(sql_empleados, (_corr,))
    empleado_result = cursor.fetchall()

    conn.commit()

    if not admin_result and not usuario_result and not empleado_result:
        return render_template('admin/loginadmin.html')

    if admin_result and _corr == admin_result[0][4] and _con == admin_result[0][5]:
        session["login"] = "admin"
        session["usuario"] = admin_result[0][1]
        session["rango"] = "admin"
        session["correo"] = admin_result[0][4]
        session["edad"] = 99
        return redirect('/admin')

    if empleado_result and _corr == empleado_result[0][5] and _con == empleado_result[0][6]:
        session["login"] = "admin"
        session["usuario"] = empleado_result[0][4]
        session["rango"] = "empleado"
        session["correo"] = empleado_result[0][5]
        session["edad"] = 99
        return redirect('/admin')

    if usuario_result and _corr == usuario_result[0][4] and _con == usuario_result[0][5]:
        session["login"] = "usuario"
        session["usuario"] = usuario_result[0][1]
        session["rango"] = "cliente"
        session["correo"] = usuario_result[0][4]
        session["edad"] = usuario_result[0][2]
        return redirect('/mostrar')

    return render_template('admin/loginadmin.html')
'''
@app.route("/Productos")
def productos1():
    if 'login' in session:
        return redirect('sitio/Productos.html')
    return render_template('/')
'''
# Cargar imagenes    
CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)

CARPETA1= os.path.join('reTIEN')
app.config['CARPETA1']=CARPETA1

@app.route('/reTIEN/<nombreFoto1>')
def reTIEN(nombreFoto1):
    return send_from_directory(app.config['CARPETA1'],nombreFoto1)

# Fin de cargar imagenes
if __name__ == '__main__':
    app.run(debug=True)



