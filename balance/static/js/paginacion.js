// Variables globales
let page = 1; // Página actual
const perPage = 10; // Número de resultados por página

// Función para cargar los movimientos
function cargarMovimientos() {
    // Realizar la petición a la API para obtener los resultados de la página actual
    fetch(`/api/v1/movimientos?p=${page}&r=${perPage}`)
        .then(response => response.json())
        .then(data => {

            // Comprobar si la petición ha sido exitosa
            if (data.status === 'success') {
                // Mostrar los resultados en la tabla
                const resultados = document.getElementById('resultados');
                resultados.innerHTML = '';
                for (let i = 0; i < data.results.length; i++) {
                    const m = data.results[i];
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
            <td>${m.fecha ? m.fecha : '---'}</td>
            <td>${m.hora}</td>
            <td>${m.origen}</td>
            <td class="numero">${m.invertido}</td>
            <td>${m.destino}</td>
            <td class="numero">${m.obtenido}</td>
            <td class="numero">${m.unitario}</td>
          `;
                    if (m.has_errors) {
                        const trError = document.createElement('tr');
                        const tdError = document.createElement('td');
                        tdError.colSpan = 7;
                        for (let j = 0; j < m.errores.length; j++) {
                            const pError = document.createElement('p');
                            pError.classList.add('error');
                            pError.textContent = m.errores[j];
                            tdError.appendChild(pError);
                        }
                        trError.appendChild(tdError);
                        resultados.appendChild(trError);
                    }
                    resultados.appendChild(tr);
                }

                numPages = Math.ceil(data.total / perPage);

                // Actualizar los botones de paginación
                const anterior = document.getElementById('anterior');
                const siguiente = document.getElementById('siguiente');
                if (page === 1) {
                    anterior.disabled = true;
                } else {
                    anterior.disabled = false;
                }
                if (page === numPages) {
                    siguiente.disabled = true;
                } else {
                    siguiente.disabled = false;
                }
                generarBotonesPaginacion()
            }
        })
        .catch(error => {
            // Mostrar mensaje de error
            const resultados = document.getElementById('resultados');
            resultados.innerHTML = `
            <tr>
            <td colspan='7' class="lista-vacia">${error}</td>
            </tr>
            <tr>
            <td colspan='7' class="lista-vacia"><a id='boton-regalo' class='button' href="/regalo-inicial">Recoge aquí tu regalo inicial</a></td>
            </tr>
        `;
        });
}

// Función para ir a la página anterior
function irPaginaAnterior() {
    if (page > 1) {
        page--;
        cargarMovimientos();
    }
}

// Función para ir a la página siguiente
function irPaginaSiguiente() {
    page++;
    cargarMovimientos();
}

// Event listeners de los botones de paginación
document.getElementById('anterior').addEventListener('click', irPaginaAnterior);
document.getElementById('siguiente').addEventListener('click', irPaginaSiguiente);

cargarMovimientos();

// Función para crear la numeración de paginación
function generarBotonesPaginacion() {
    const contenedorPaginacion = document.getElementById('contenedor-paginacion');
    contenedorPaginacion.innerHTML = '';

    for (let i = 1; i <= numPages; i++) {
        const botonPagina = document.createElement('button');
        botonPagina.textContent = i;
        if (i === page) {
            botonPagina.classList.add('pagina-actual');
            botonPagina.disabled = true;
        }
        botonPagina.addEventListener('click', () => {
            page = i;
            cargarMovimientos();
        });
        contenedorPaginacion.appendChild(botonPagina);
    }
}
