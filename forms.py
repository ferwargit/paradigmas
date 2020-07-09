from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Length


class InicioSesionForm(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[Required(), Length(min=4, max=14)])
    password = PasswordField('Contraseña', validators=[Required(), Length(min=4, max=10)])
    enviar = SubmitField('Ingresar')


class RegistrarseForm(InicioSesionForm):
    password_check = PasswordField('Verificar Contraseña', validators=[Required(), Length(min=4, max=10)])
    enviar = SubmitField('Registrarse')
    

class AgregarClienteForm(FlaskForm):
    nombre = StringField('Nombre del Cliente', validators=[Required(), Length(min=4, max=28)])
    edad = StringField('Edad', validators=[Required(), Length(min=2, max=2)])
    direccion = StringField('Dirección', validators=[Required(), Length(min=4, max=14)])
    pais = StringField('País', validators=[Required(), Length(min=4, max=14)])
    documento = StringField('Documento DNI', validators=[Required(), Length(min=8, max=10)])
    fecha = StringField('Fecha Alta (YYYY-MM-DD)', validators=[Required(), Length(min=10, max=10)])
    correo = StringField('Correo Electrónico', validators=[Required(), Length(min=4, max=24)])
    trabajo = StringField('Trabajo', validators=[Required(), Length(min=4, max=14)])
    enviar = SubmitField('Agregar')
    
    
class AgregarProductoForm(FlaskForm):
    codigo = StringField('Código', validators=[Required(), Length(min=4, max=4)])
    descripcion = StringField('Descripción', validators=[Required(), Length(min=4, max=54)])
    precio = StringField('Precio', validators=[Required(), Length(min=1, max=10)])
    stock = StringField('Stock', validators=[Required(), Length(min=1, max=10)])
    enviar = SubmitField('Agregar')
    
class ConsultarForm(FlaskForm):
    consulta_pais = StringField('País', validators=[Required(), Length(min=4, max=10)])
    enviar = SubmitField('Consultar')
    

class ConsultarEdadForm(FlaskForm):
    consulta_edad = StringField('Edad', validators=[Required(), Length(min=2, max=2)])
    enviar = SubmitField('Consultar')
    

class ConsultarFechaForm(FlaskForm):
    consulta_fecha = StringField('Fecha Alta (YYYY-MM-DD)', validators=[Required(), Length(min=10, max=14)])
    enviar = SubmitField('Consultar')
    
