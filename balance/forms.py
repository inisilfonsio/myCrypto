from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, IntegerField, RadioField, StringField, SubmitField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired


class MovimientoForm(FlaskForm):
    id = IntegerField(default=0, widget=HiddenInput())
    fecha = DateField('Fecha', validators=[DataRequired(
        message="Debes introducir una fecha")])
    concepto = StringField('Concepto', validators=[
                           DataRequired(message="Debes especificar un concepto")])
    tipo = RadioField(
        choices=[('I', 'Ingreso'), ('G', 'Gasto')], validators=[DataRequired()])
    cantidad = FloatField('Cantidad', validators=[DataRequired(
        message="La cantidad debe tener un valor")])

    submit = SubmitField('Guardar')


# TODO actualizarlo
'''
Este código define un formulario de entrada para ingresar información sobre movimientos,
y utiliza la biblioteca WTForms para validar los datos ingresados por el usuario.
'''
