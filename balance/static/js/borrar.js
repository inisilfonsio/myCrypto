// Cuando se carga la página, se llama a la función cargarMovimientos para mostrar los movimientos
window.onload = function () {
    cargarMovimientos();
}

// Función que llama a la API para obtener los movimientos del usuario y los muestra en la tabla
function cargarMovimientos() {

    // Se hace la petición a la API
    fetch('/api/v1/movimientos')
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            // Se comprueba si se ha recibido una respuesta correcta
            if (data.status === 'success') {
                // Se vacía la tabla
                var tableBody = document.getElementById('movimientos-body');
                tableBody.innerHTML = '';

                // Se recorren los movimientos y se van agregando a la tabla
                data.movs.forEach(function (movimiento) {
                    var row = document.createElement('tr');

                    var fecha = document.createElement('td');
                    fecha.innerHTML = movimiento.fecha ? movimiento.fecha : '---';
                    row.appendChild(fecha);

                    var hora = document.createElement('td');
                    hora.innerHTML = movimiento.hora;
                    row.appendChild(hora);

                    var origen = document.createElement('td');
                    origen.innerHTML = movimiento.origen;
                    row.appendChild(origen);

                    var invertido = document.createElement('td');
                    invertido.innerHTML = movimiento.invertido;
                    invertido.className = 'numero';
                    row.appendChild(invertido);

                    var destino = document.createElement('td');
                    destino.innerHTML = movimiento.destino;
                    row.appendChild(destino);

                    var obtenido = document.createElement('td');
                    obtenido.innerHTML = movimiento.obtenido;
                    obtenido.className = 'numero';
                    row.appendChild(obtenido);

                    var unitario = document.createElement('td');
                    unitario.innerHTML = movimiento.unitario;
                    unitario.className = 'numero';
                    row.appendChild(unitario);

                    tableBody.appendChild(row);

                    // Si el movimiento tiene errores, se agregan debajo
                    if (movimiento.has_errors) {
                        var errorRow = document.createElement('tr');
                        var emptyCell = document.createElement('td');
                        emptyCell.colSpan = 4;

                        var errorList = document.createElement('ul');
                        movimiento.errores.forEach(function (error) {
                            var errorItem = document.createElement('li');
                            errorItem.innerHTML = error;
                            errorList.appendChild(errorItem);
                        });

                        emptyCell.appendChild(errorList);
                        errorRow.appendChild(emptyCell);
                        tableBody.appendChild(errorRow);
                    }
                });

                // Se oculta el mensaje "No hay movimientos para mostrar" si hay movimientos
                var listaVacia = document.querySelector('.lista-vacia');
                if (data.movs.length > 0) {
                    listaVacia.style.display = 'none';
                } else {
                    listaVacia.style.display = 'table-row';
                }

            }
            // Si ha habido un error, se muestra en consola
            else {
                console.log(data.message);
            }
        })
        // Si ha habido un error en la petición, se muestra en consola
        .catch(function (error) {
            console.log(error);
        });
}

// Cuando se hace clic en el botón "Cargar", se llama a la función cargarMovimientos para mostrar los movimientos actualizados
var cargarMovimientosButton = document.getElementById('cargar-movimientos');
cargarMovimientosButton.addEventListener('click', function () {
    cargarMovimientos();
});
