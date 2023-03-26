from . import app
from balance.models import *


@app.route('/')
def inicio():

    return 'Arrancamos flask'
