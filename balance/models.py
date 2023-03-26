from datetime import date
import sqlite3


class DBManager:
    """
    Clase para interactuar con la base de datos SQLite
    """

    def __init__(self, ruta):
        self.ruta = ruta

    def consultaSQL(self, consulta):
        # 1. Conectar a la base de datos
        conexion = sqlite3.connect(self.ruta)

        # 2. Abrir un cursor
        cursor = conexion.cursor()

        # 3. Ejecutar la consulta SQL sobre ese cursor
        cursor.execute(consulta)

        # 4. Tratar los datos
        # 4.1 obtener los datos
        datos = cursor.fetchall()

        self.movimientos = []
        nombres_columna = []
        for columna in cursor.description:
            nombres_columna.append(columna[0])

        for dato in datos:
            indice = 0
            movimiento = {}
            for nombre in nombres_columna:
                movimiento[nombre] = dato[indice]
                indice += 1

            self.movimientos.append(movimiento)

        # 5. Cerrar la conexión
        conexion.close()

        # 6. Devolver la colección de resultados
        return self.movimientos

    def conectar(self):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()

        return conexion, cursor

    def desconectar(self, conexion):
        conexion.close()

    def consultaConParametros(self, consulta, params):
        conexion, cursor = self.conectar()

        resultado = False
        try:
            cursor.execute(consulta, params)
            conexion.commit()
            resultado = True
        except Exception as ex:
            print(ex)
            conexion.rollback()

        self.desconectar(conexion)
        return resultado

    def borrar(self, id):
        consulta = f'DELETE FROM {NOMBRE_TABLA} WHERE id=?'
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        resultado = False
        try:
            cursor.execute(consulta, (id,))
            conexion.commit()
            resultado = True
        except:
            conexion.rollback()

        conexion.close()
        return resultado

    def obtenerMovimiento(self, id):
        """
        Obtiene un movimiento a partir de su ID de la base de datos
        """
        consulta = f'SELECT {CAMPOS_TABLA} FROM {NOMBRE_TABLA} WHERE id=?'
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta, (id,))

        datos = cursor.fetchone()
        resultado = None

        if datos:
            nombres_columna = []
            for column in cursor.description:
                nombres_columna.append(column[0])

            movimiento = {}
            indice = 0
            for nombre in nombres_columna:
                movimiento[nombre] = datos[indice]
                indice += 1

            print(f'Fecha ANTES: {movimiento["fecha"]}')
            movimiento['fecha'] = date.fromisoformat(movimiento['fecha'])
            print(f'DESPUÉS:     {movimiento["fecha"]}')

            resultado = movimiento

        conexion.close()
        return resultado
