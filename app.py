from flask import Flask, render_template, redirect, url_for,flash, session
from flask_bootstrap import Bootstrap
from forms import RegistrarseForm, InicioSesionForm, AgregarClienteForm, AgregarProductoForm, ConsultarForm, ConsultarEdadForm, ConsultarFechaForm
import csv


app = Flask(__name__)
bootstrap = Bootstrap(app)


app.config['SECRET_KEY'] = 'un secreto'


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    """ Muestra formulario de ingreso al sitio, valida las variables del formulario, abre el archivo y lee los registros, si los registros coinciden (usuario y contraseña) muestra mensaje y el usuario entra en sesion (username) en caso contario muestra mensaje de aviso al usuario y permite nuevamente el ingreso de los datos al formulario de ingreso hasta que estos sean correctos.
    """
    
    formulario = InicioSesionForm()
    if formulario.validate_on_submit():
        with open('usuarios.csv') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    flash('Bienvenido al sitio-Web de Tierra Inc.')
                    session['username'] = formulario.usuario.data
                    return render_template('ingresado.html')
                registro = next(archivo_csv, None)
            else:
                flash('Revisá nombre de usuario y contraseña')
                return redirect(url_for('ingresar'))
    return render_template('ingresar.html', formulario=formulario)



@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    """ Muestra formulario de registro al sitio, valida las variables del formulario, abre el archivo y lee los registros, si los registros coinciden (usuario) muestra mensaje de aviso al usuario ya existente y presenta nuevamente el formulario. Tambien verifica que las contraseñas sean iguales. Si el usuario es nuevo lo guarda en el archivo de usuarios y muestra mensaje de registro correcto y le permite iniciar sesion. 
    """
    
    formulario = RegistrarseForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios.csv', 'r') as archivo:
                csv_reader = csv.reader(archivo)
                for row in csv_reader:
                    if row [0] == formulario.usuario.data: # and row [1] == formulario.password.data:
                        flash('Usuario ya existe')
                        return redirect(url_for('registrarse'))
            with open('usuarios.csv', 'a', newline='') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('El Usuario  y la Contraseña se registraron correctamente !!! --> Iniciar Sesión !!!')
            return redirect(url_for('ingresar'))
        else:
            flash('Las contraseñas ingreasadas no son iguales')
    return render_template('registrarse.html', form=formulario)



@app.route('/lista_de_clientes')
def lista_de_clientes():
    """ Abre y lee el archivo de clientes y lo renderiza en el template html, mostrarando al usuario la lista de clientes y cantidad.
    """
    
    if 'username' in session:
        with open("clientes.csv", encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            clientes_data = []
            for row in csv_reader:
                clientes_data.append (row)
        return render_template('lista_de_clientes.html', clientes_data = clientes_data, cantidad = len(clientes_data)) 
    else:
        return redirect(url_for('index')) 


    
@app.route('/agregar_cliente', methods=['GET', 'POST'])
def agregar_cliente():
    """ Permite ingresar clientes registrandolos en el archivo clientes.csv por medio del formulario, validando los registros (nombre, edad, direccion, pais, documento, fecha, correo y trabajo), informando al usuario de carga correcta y su posterior visualización. Si el usuario no esta en sesion lo redirecciona al index.
    """
    
    if 'username' in session:
        formulario = AgregarClienteForm()
        if formulario.validate_on_submit():
            with open('clientes.csv', 'a', newline='') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.nombre.data, formulario.edad.data, 
                            formulario.direccion.data, formulario.pais.data,
                            formulario.documento.data, formulario.fecha.data,
                            formulario.correo.data, formulario.trabajo.data]
                archivo_csv.writerow(registro)
            flash('Cliente cargado correctamente')
            return redirect(url_for('lista_de_clientes'))
        return render_template('agregar_cliente.html', nuevo_cliente=formulario)
    else:
        return redirect(url_for('index'))



@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    """ Permite ingresar productos registrandolos en el archivo productos.csv por medio del formulario, validando los registros (codigo, descripcion, precio y stock), informando al usuario de carga correcta y su posterior visualización. Si el usuario no esta en sesion lo redirecciona al index.
    """
    
    if 'username' in session:
        formulario = AgregarProductoForm()
        if formulario.validate_on_submit():
            with open('productos.csv', 'a', newline='') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.codigo.data, formulario.descripcion.data, 
                            formulario.precio.data, formulario.stock.data]
                archivo_csv.writerow(registro)
            flash('Producto cargado correctamente')
            return redirect(url_for('lista_de_productos'))
        return render_template('agregar_producto.html', nuevo_producto=formulario)
    else:
        return redirect(url_for('index'))



@app.route('/lista_de_productos')
def lista_de_productos():
    """ Muestra al usuario la lista y la cantidad total de productos ingresados, registrandos en el archivo productos.csv, renderizando la vista por medio del template 'lista_de_productos.html
    """
    
    if 'username' in session:
        with open("productos.csv", encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            productos_data = []
            for row in csv_reader:
                productos_data.append (row)
        return render_template('lista_de_productos.html', productos_data = productos_data, cantidad_productos = len(productos_data)) 
    else:
        return redirect(url_for('index'))


@app.route('/consultas_pais', methods=['GET', 'POST'])
def consultas_pais():
    """ Permite al usuario realizar consultas por pais por medio del formulario, buscando en el archivo clientes, iterando cada cliente por pais (columna 3 del archivo), si el filtro coicide con el pais buscado lo guarda en resultado y lo renderiza en el template html. Si no encuentra (resultado == []) muestra mensaje al usuario.
    """
    
    if 'username' in session:
	    formulario = ConsultarForm()
	    filtro = formulario.consulta_pais.data
	    resultado = []
	    if formulario.validate_on_submit():
		    with open('clientes.csv', newline='', encoding='utf-8') as planillaClientes:
			    planilla_csv = csv.reader(planillaClientes)
			    encabezado_csv = next(planilla_csv)
			    cliente = next(planilla_csv, None)
			    while cliente:			
				    if filtro in cliente[3]:
					    resultado.append(cliente)
				    cliente = next(planilla_csv, None)
			    if resultado == []:
				    flash('No hay resultados para tu búsqueda')
			    else:
				    return render_template('consultas_resultado.html', encabezado_csv=encabezado_csv, resultado=resultado, cantidad=len(resultado))
	    return render_template('consultas.html', form=formulario, resultado=resultado)
    else:
	    return render_template('sin_permiso.html')



@app.route('/consultas_edad', methods=['GET', 'POST'])
def consultas_edad():
    """
    Permite al usuario realizar consultas por edad por medio del formulario, buscando en el archivo clientes, iterando cada cliente por edad (columna 1 del archivo), si el filtro coicide con la edad buscada la guarda en resultado y lo renderiza en el template html. Si no encuentra (resultado == []) muestra mensaje al usuario.
    """
    
    if 'username' in session:
	    formulario = ConsultarEdadForm()
	    filtro = formulario.consulta_edad.data
	    resultado = []
	    if formulario.validate_on_submit():
		    with open('clientes.csv', newline='', encoding='utf-8') as planillaClientes:
			    planilla_csv = csv.reader(planillaClientes)
			    encabezado_csv = next(planilla_csv)
			    cliente = next(planilla_csv, None)
			    while cliente:			
				    if filtro in cliente[1]:
					    resultado.append(cliente)
				    cliente = next(planilla_csv, None)
			    if resultado == []:
				    flash('No hay resultados para tu búsqueda')
			    else:
				    return render_template('consultas_resultado.html', encabezado_csv=encabezado_csv, resultado=resultado, cantidad=len(resultado))
	    return render_template('consultas.html', form=formulario, resultado=resultado)
    else:
	    return render_template('sin_permiso.html')



@app.route('/consultas_fecha', methods=['GET', 'POST'])
def consultas_fecha():
    """ Permite al usuario realizar consultas por fecha por medio del formulario, buscando en el archivo clientes, iterando cada cliente por fecha (columna 5 del archivo), si el filtro coicide con la fecha buscada la guarda en resultado y lo renderiza en el template html. Si no encuentra (resultado == []) muestra mensaje al usuario.
    """
    
    if 'username' in session:
	    formulario = ConsultarFechaForm()
	    filtro = formulario.consulta_fecha.data
	    resultado = []
	    if formulario.validate_on_submit():
		    with open('clientes.csv', newline='', encoding='utf-8') as planillaClientes:
			    planilla_csv = csv.reader(planillaClientes)
			    encabezado_csv = next(planilla_csv)
			    cliente = next(planilla_csv, None)
			    while cliente:			
				    if filtro in cliente[5]:
					    resultado.append(cliente)
				    cliente = next(planilla_csv, None)
			    if resultado == []:
				    flash('No hay resultados para tu búsqueda')
			    else:
				    return render_template('consultas_resultado.html', encabezado_csv=encabezado_csv, resultado=resultado, cantidad=len(resultado))
	    return render_template('consultas.html', form=formulario, resultado=resultado)
    else:
	    return render_template('sin_permiso.html')



@app.route('/salir', methods=['GET'])
def salir():
    if 'username' in session:
        session.pop('username')
        return render_template('salir.html')
    else:
        return redirect(url_for('index'))




@app.route('/sobre')
def sobre():
    return render_template('sobre.html')



@app.errorhandler(404)
def no_encontrado(error):
    return render_template('404.html'), 404



@app.errorhandler(500)
def error_interno(error):
    return render_template('500.html'), 500



if __name__ == '__main__':
    app.run(debug=True)
