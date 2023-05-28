from flask import Flask
from flask import render_template,request, redirect,url_for,session, flash, make_response
from flaskext.mysql import MySQL
from flask import send_from_directory
from datetime import datetime
import random
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

#Ruta inicio 2.
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

#Agregar producto.
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
    _img = request.files['imagen']
    
    if codigo == '' or nombre == '' or precio_compra == '0' or precio_venta == '0' or existencias == '0':
        return redirect('/agregar')  # Redireccionar si hay campos vacíos o valores de 0
    
    conn = mysql.connect()
    cursor = conn.cursor()
    
    # Verificar si el código ya existe en la base de datos
    query_select = "SELECT * FROM productos WHERE codigo = %s"
    select_values = (codigo,)
    cursor.execute(query_select, select_values)
    result = cursor.fetchone()
    
    if result:
        # Generar un nuevo código que no esté en la base de datos
        new_codigo = random.randint(1, 99999999999)
        while check_codigo_exist(new_codigo):
            new_codigo =random.randint(1, 99999999999)
        
        codigo = new_codigo
    
    # Verificar si el nombre ya existe en la base de datos
    query_select = "SELECT * FROM productos WHERE Nombre = %s"
    select_values = (nombre,)
    cursor.execute(query_select, select_values)
    result = cursor.fetchone()
    
    if result:
        return redirect('/agregar')  # Redireccionar si el nombre ya existe
    
    if _img.filename != '':
        _img.save(f"reTIEN\{_img.filename}")
    else:
       return redirect('/agregar')
        
    query_insert = "INSERT INTO productos (codigo, Nombre, preciodecompra, preciodeventa, existencia, restriccion, imagen) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    insert_values = (codigo, nombre, precio_compra, precio_venta, existencias, restriccion, _img.filename)
    
    cursor.execute(query_insert, insert_values)
    conn.commit()
    
    return redirect('/agregar')  # Redireccionar a la página de agregar después de realizar la inserción



def check_codigo_exist(codigo):
    # Verificar si el código ya existe en la base de datos
    conn = mysql.connect()
    cursor = conn.cursor()
    
    query_select = "SELECT * FROM productos WHERE codigo = %s"
    select_values = (codigo,)
    cursor.execute(query_select, select_values)
    result = cursor.fetchone()
    
    if result:
        return True  # El código existe
    else:
        return False  # El código no existe


#Agregar cliente.
@app.route("/agreclie", methods=['POST'])
def agreclie():
    if not 'login' in session:
        return redirect('/')
    if session["rango"] == "cliente":
        return redirect('/')

    codigo = request.form['Codigo']
    nombre = request.form['Nombre']
    edad = request.form['Prec']
    Nombreusuario = request.form['Prev']
    Email = request.form['Existen']
    Contraseña = request.form['Rest']

    conn = mysql.connect()
    cursor = conn.cursor()

    # Verificar si la ID ya existe
    query_id_exists = "SELECT COUNT(*) FROM clientes WHERE id = %s"
    cursor.execute(query_id_exists, (codigo,))
    count_id = cursor.fetchone()[0]
    if count_id > 0:
        # La ID ya existe, generar una nueva ID única
        while True:
            nueva_codigo = random.randint(1, 99999999999)
            cursor.execute(query_id_exists, (nueva_codigo,))
            count_nueva_id = cursor.fetchone()[0]
            if count_nueva_id == 0:
                codigo = nueva_codigo  # Asignar la nueva ID única
                break

    # Verificar si el correo electrónico ya existe
    query_email_exists = "SELECT COUNT(*) FROM clientes WHERE correo = %s"
    cursor.execute(query_email_exists, (Email,))
    count_email = cursor.fetchone()[0]
    if count_email > 0:
        return redirect('/agregar2')  # El correo electrónico ya existe, no insertar en la base de datos

    # Insertar el nuevo cliente en la base de datos
    query_insert = "INSERT INTO clientes (id, nombre, edad, usuario, correo, contra) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (codigo, nombre, edad, Nombreusuario, Email, Contraseña)
    cursor.execute(query_insert, values)
    conn.commit()

    return redirect('/agregar2')

#Agregar trabajador.
@app.route("/agretra", methods=['POST'])
def agretra():
    if not 'login' in session:
        return redirect('/')
    if session["rango"] == "cliente":
        return redirect('/')
    
    codigo = request.form['Codigo']
    nombre = request.form['Nombre']
    Horario = request.form['Prec']
    Salario = request.form['Prev']
    Usuario = request.form['Existen']
    Correo = request.form['Rest']
    Contraseña = request.form['Contra']
    
    conn = mysql.connect()
    cursor = conn.cursor()
    query_check_id = "SELECT * FROM trabajador WHERE id = %s"
    cursor.execute(query_check_id, (codigo,))
    result = cursor.fetchone()
    if result:
        # Generar una nueva ID que no esté presente en la base de datos
        new_id = None
        while True:
            new_id = random.randint(1,99999999999)
            cursor.execute(query_check_id, (new_id,))
            count_nueva_id = cursor.fetchone()
            if count_nueva_id is None:
                codigo = new_id  # Asignar la nueva ID única
                break
    # Verificar si el correo ya existe en la base de datos
    query_check_correo = "SELECT * FROM trabajador WHERE correo = %s"
    cursor.execute(query_check_correo, (Correo))
    result = cursor.fetchone()
    if result:
        return redirect('/trabajadores')
    
    query_insert = "INSERT INTO trabajador (id, nombre, horario, salario, usuario, correo, contra) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (codigo, nombre, Horario, Salario, Usuario, Correo, Contraseña)
    
    cursor.execute(query_insert, values)
    conn.commit()
    
    return redirect('/agregar3')

#Mostrar.
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

#Mostrar carro.
@app.route("/mostcarr")
def mostcarr():
    if 'login' not in session:
        return redirect('/')

    conn = mysql.connect()
    cursor = conn.cursor()
    
    # Obtener los productos en el carrito del usuario actual
    sql = "SELECT * FROM `carrito` WHERE Correo = %s;"
    cursor.execute(sql, (session["correo"],))
    carrito = cursor.fetchall()
    
    # Calcular la suma total de los precios actualizados
    suma_total = 0
    for item in carrito:
        producto = item[1]
        cantidad = item[3]
        
        # Obtener el precio actual del producto desde la tabla "productos"
        sql_precio = "SELECT * FROM `productos` WHERE Nombre = %s;"
        cursor.execute(sql_precio, (producto,))
        producto_info = cursor.fetchone()
        precio_actual = producto_info[3]
        cantidad_disponible = producto_info[4]
        
        # Verificar si hay suficiente cantidad de producto
        if cantidad > cantidad_disponible:
            cantidad = cantidad_disponible  # Establecer la cantidad máxima disponible
        
        # Actualizar el precio en el registro del carrito
        nuevo_total = int(precio_actual) * int(cantidad)
        sql_update_precio = "UPDATE `carrito` SET Precio = %s, Total = %s, Cantidad = %s WHERE Producto = %s AND Correo = %s;"
        cursor.execute(sql_update_precio, (precio_actual, nuevo_total, cantidad, producto, session["correo"]))
        
        # Sumar al total
        suma_total += nuevo_total
    
    conn.commit()
    
    return render_template('sitio/carrito.html', carrito=carrito, suma_total=suma_total)


@app.route('/destroycarro/<nombre>')
def destroycarro(nombre):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM carrito WHERE Producto=%s", (nombre,))
    productos=cursor.fetchall()
    conn.commit()
    return redirect('/mostcarr')


@app.route('/agregacarrito', methods=['POST'])
def agregar_al_carrito():
    producto = request.form.get('producto')
    correo = session.get('correo')
    
    # Obtener el precio actual y cantidad disponible del producto
    conn = mysql.connect()
    cursor = conn.cursor()
    sql_select_info = "SELECT preciodeventa, existencia FROM productos WHERE Nombre = %s"
    cursor.execute(sql_select_info, (producto,))
    result = cursor.fetchone()
    if result:
        precio = result[0]
        cantidad_disponible = result[1]
        cantidad = int(request.form.get('cantidad'))
        total = int(precio) * cantidad

        # Verificar si hay datos para el producto y correo especificados
        sql_select = "SELECT * FROM carrito WHERE Producto = %s AND Correo = %s"
        select_values = (producto, correo)
        cursor.execute(sql_select, select_values)
        result = cursor.fetchone()
        if result:
            # Actualizar la cantidad del registro existente
            cantidad_actual = int(result[3])
            nueva_cantidad = cantidad_actual + cantidad
            nuevo_total = int(precio) * nueva_cantidad
             # Verificar si hay suficiente cantidad de producto
            if nueva_cantidad > cantidad_disponible:
                nueva_cantidad = cantidad_disponible  # Establecer la cantidad máxima disponible
                nuevo_total = int(precio) * nueva_cantidad

        
            sql_update = "UPDATE carrito SET Precio=%s, Cantidad=%s, Total=%s WHERE Producto=%s AND Correo=%s"
            update_values = (precio, nueva_cantidad, nuevo_total, producto, correo)
            cursor.execute(sql_update, update_values)
            conn.commit()
        else:
            # Agregar un nuevo registro
            sql_insert = "INSERT INTO carrito (Producto, Precio, Cantidad, Total, Correo) VALUES (%s, %s, %s, %s, %s)"
            insert_values = (producto, precio, cantidad, total, correo)
            cursor.execute(sql_insert, insert_values)
            conn.commit()
        
    cursor.close()
    return redirect('/mostcarr')


@app.route('/generatickete', methods=['POST'])
def generatickete():
    productos = request.form.getlist('producto')
    precios = request.form.getlist('precio')
    cantidades = request.form.getlist('cantidad')
    totales = request.form.getlist('total')

    # Crear el contenido del archivo de texto
    contenido = "{:<20s}{:<10s}{:<10s}{:<10s}\n".format("Producto", "Precio", "Cantidad", "Total")
    for i in range(len(productos)):
        contenido += "{:<20s}{:<10s}{:<10s}{:<10s}\n".format(productos[i], precios[i], cantidades[i], totales[i])

    # Agregar el total a pagar al final
    suma_total = sum(float(total) for total in totales)
    contenido += "\n{:<20s}${:<10.2f}".format("Total a Pagar", suma_total)

    for i in range(len(cantidades)):
        producto = productos[i]
        cantidad = int(cantidades[i])

        consulta = "UPDATE productos SET existencia = existencia - %s WHERE Nombre = %s"
        valores = (cantidad, producto)
        conn=mysql.connect()
        cursor = conn.cursor()
        cursor.execute(consulta, valores)
        conn.commit()

    correo_buscar = session["correo"]
    consulta_eliminar = "DELETE FROM carrito WHERE correo = %s"
    valores_eliminar = (correo_buscar,)
    conn=mysql.connect()
    cursor = conn.cursor()
    cursor.execute(consulta_eliminar, valores_eliminar)
    conn.commit()

    # Guardar el archivo en el servidor
    archivo_nombre = "ticket.txt"
    archivo_ruta = os.path.join(app.root_path, "archivos", archivo_nombre)
    with open(archivo_ruta, "w") as archivo:
        archivo.write(contenido)

   
   
    # Leer el contenido del archivo
    with open(archivo_ruta, "r") as archivo:
        contenido_archivo = archivo.read()
        
        
    correoticket = session["correo"]
    usuarioticket = session["usuario"]
    consulta_insertar = "INSERT INTO ticket (archivo, usuario, caducidad, estado,correo) VALUES (%s, %s, %s, %s, %s)"
    valores_insertar = (contenido_archivo, usuarioticket, "2023-12-31", "Activo",correoticket)
     # Guardar el archivo en una tabla de MySQL
    conn=mysql.connect()
    cursor = conn.cursor()
    cursor.execute(consulta_insertar, valores_insertar)
    conn.commit()


    # Crear la respuesta con el archivo de texto
    response = make_response(contenido)
    response.headers["Content-Disposition"] = "attachment; filename=ticket.txt"
    response.headers["Content-type"] = "text/plain"

    return response

@app.route('/mostrar_ticket/<int:id>')
def mostrar_ticket(id):
    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente":
        return redirect('/')
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT archivo FROM ticket WHERE id = %s", (id,))
    resultado = cursor.fetchone()
    
    contenido = resultado[0] if resultado else None
    
    return render_template('sitio/tabla.html', contenido=contenido)

#Agregar 1.
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

#Agregar 2.
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

#Agregar 3.
@app.route("/agregar3")
def agre3():
    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente":
        return redirect('/')
    sql="SELECT * FROM `trabajador`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    productos=cursor.fetchall()
    conn.commit()
    return render_template('admin/mtrabajador.html',productos=productos)

#Ruta clientes.
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

#Ruta tickets.
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

#Ruta trabajadores.
@app.route("/trabajadores")
def trabajadores():

    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente":
        return redirect('/')
        
    sql="SELECT * FROM `trabajador`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    productos=cursor.fetchall()
    conn.commit()
    return render_template('admin/mtrabajador.html',productos=productos)

#Eliminar productos.
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


#Eliminar cliente.
@app.route('/destroyClient/<int:id>')
def destroyClient(id):
    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente" or session["rango"]=="empleado":
        return redirect('/admin')
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id=%s",(id))
    productos=cursor.fetchall()
    conn.commit()
    return redirect('/cliente')

#Eliminar empleado.
@app.route('/destroyemple/<int:id>')
def destroyemple(id):
    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente" or session["rango"]=="empleado":
        return redirect('/admin')
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM trabajador WHERE id=%s",(id))
    productos=cursor.fetchall()
    conn.commit()
    return redirect('/trabajadores')

#Eliminar ticket.
@app.route('/destroyticket/<int:id>')
def destroyticket(id):
    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente" or session["rango"]=="empleado":
        return redirect('/admin')
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM ticket WHERE id=%s",(id))
    productos=cursor.fetchall()
    conn.commit()
    return redirect('/ticket')


#Editar productos.
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

#Funcion editar clientes.
@app.route('/edidc/<int:id>')
def edidc(id):
    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente" or session["rango"]=="empleado":
        return redirect('/admin')
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id=%s",(id))
    productos=cursor.fetchall()
    conn.commit()
    return render_template('invet/edidc.html',productos=productos)

#Editar trabajador
@app.route('/edide/<int:id>')
def edide(id):
    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente" or session["rango"]=="empleado":
        return redirect('/admin')
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM trabajador WHERE id=%s",(id))
    productos=cursor.fetchall()
    conn.commit()
    return render_template('invet/edide.html',productos=productos)

#Editar Ticket
@app.route('/edidti/<int:id>')
def edidti(id):
    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente":
        return redirect('/admin')
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM ticket WHERE id=%s",(id))
    productos=cursor.fetchall()
    conn.commit()
    return render_template('invet/edidti.html',productos=productos)


#Accion 1.
@app.route("/act", methods=['POST'])
def act():
    if not 'login' in session:
        return redirect('/')
    
    if session["rango"]=="cliente" or session["rango"]=="empleado":
        return redirect('/')
    
    id = request.form['Codigo']
    _nom = request.form['Nombre']
    _prev = request.form['preciodecompra']
    _prec = request.form['preciodeventa']
    _exi = request.form['existencia']
    _rest = request.form['restriccion']
    _img = request.files['imagen']
    
    conn = mysql.connect()
    cursor = conn.cursor()
    
    if _img.filename != '':
        _img.save(f"reTIEN\{_img.filename}")
        sql = "UPDATE productos SET `Nombre`=%s, `preciodecompra`=%s, `preciodeventa`=%s, `existencia`=%s, `restriccion`=%s, `imagen`=%s WHERE codigo=%s ;"
        datos = (_nom, _prev, _prec, _exi, _rest, _img.filename, id)
    else:
        sql = "UPDATE productos SET `Nombre`=%s, `preciodecompra`=%s, `preciodeventa`=%s, `existencia`=%s, `restriccion`=%s WHERE codigo=%s ;"
        datos = (_nom, _prev, _prec, _exi, _rest, id)
    
    cursor.execute(sql, datos)
    conn.commit()
    
    return redirect('/agregar')

#Accion 2.
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

#Editar empleado.
@app.route("/act4", methods=['POST'])
def act4():
    if not 'login' in session:
        return redirect('/')
    
    if session["rango"]=="cliente" or session["rango"]=="empleado":
        return redirect('/')
    id=request.form['id']
    _nom=request.form['nombre']
    _prev=request.form['horario']
    _sala=request.form['salario']
    _prec=request.form['usuario']
    _exi=request.form['correo']
    _rest=request.form['contra']
    #_img=request.files['imagen']

    #if _img.filename != '':
    #    _img.save(f"reTIEN\{_img.filename}")
    sql="UPDATE trabajador SET `nombre`=%s, `horario`=%s, `salario`=%s, `usuario`=%s, `correo`=%s, `contra`=%s WHERE id=%s ;"
    datos=(_nom,_prev,_sala,_prec,_exi,_rest,id)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/trabajadores')

#Editar ticket.
@app.route("/act5", methods=['POST'])
def act5():
    if not 'login' in session:
        return redirect('/')
    if session["rango"]=="cliente":
        return redirect('/')
    id=request.form['id']
    _prev=request.form['usuario']
    _sala=request.form['caducidad']
    _prec=request.form['estado']
    _exi=request.form['correo']
    #_img=request.files['imagen']

    #if _img.filename != '':
    #    _img.save(f"reTIEN\{_img.filename}")
    sql="UPDATE ticket SET `estado`=%s WHERE id=%s ;"
    datos=(_prec,id)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/ticket')

# Ruta de inicio de seccion correcto como admin
@app.route("/Loginadmin")
def Loginadmin():
    if 'login' in session and session.get('rango') == 'admin' or 'login' in session and session.get('rango') == 'empleado':
        return redirect('/admin')
    if 'login' in session and session.get('rango') == 'cliente':
        return redirect('/mostrar')
    return render_template('admin/loginadmin.html')

#Inicio de sesión.  
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



