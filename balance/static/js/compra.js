const formulario = document.querySelector('#form-comprar');
const obtenido = document.querySelector('#obtenido');
const unitario = document.querySelector('#unitario');
const invertir = document.querySelector('#invertir');
const invertido = document.querySelector('#invertido');
const calcular = document.querySelector('#calcular')
const mensajeError = document.querySelector('#mensaje-fondos');
const mensajeInv = document.querySelector('#error-invertir');
const origen = document.querySelector('#origen');
const destino = document.querySelector('#destino');

// Este código establece el menú desplegable de destino para que no tenga ninguna opción seleccionada

origen.selectedIndex = -1;
destino.selectedIndex = -1;
// Este código establece el menú desplegable de destino para que tenga una opción por defecto
const defaultOptionOrigen = new Option('--elija una opción--', '');
origen.options.add(defaultOptionOrigen, 0);
const defaultOptionDestino = new Option('--elija una opción--', '');
destino.options.add(defaultOptionDestino, 0);

origen.addEventListener('change', () => {
    const selected = origen.value;
    Array.from(destino.options).forEach((option) => {
        if (option.value === selected) {
            option.disabled = true;
        } else {
            option.disabled = false;
        }
    });
    defaultOptionOrigen.disabled = true; // deshabilita la opción por defecto
    defaultOptionDestino.disabled = true; // deshabilita la opción por defecto
});

invertido.addEventListener('input', () => {
    if (invertido.value > 0) {
        calcular.disabled = false;
    } else {
        calcular.disabled = true;

    }
});


calcular.addEventListener('click', async (event) => {
    event.preventDefault();
    console.log("estoy dentro");

    const response = await fetch('/api/v1/consultar-cambio', {
        method: 'POST',
        body: new FormData(formulario),
    });

    const { obtenido: obtenidoValor, unitario: valorUnitario, tienes_fondos, resultado } = await response.json();

    obtenido.value = obtenidoValor.toFixed(5);
    document.getElementById("crypto-destino").textContent = document.getElementById("destino").value;
    unitario.value = (valorUnitario).toFixed(5);
    document.getElementById("crypto-origen").textContent = document.getElementById("origen").value;

    if (resultado == "") {
        document.getElementById("error-invertir").innerHTML = "Debes introducir un valor positivo";
    }

    if (!tienes_fondos) {
        document.getElementById("mensaje-fondos").innerHTML = "No tienes fondos suficientes para realizar la operación.";
        document.getElementById("invertir").disabled = true;
    } else {
        document.getElementById("mensaje-fondos").innerHTML = "Puedes realizar la operación.";
        document.getElementById("invertir").disabled = false;
    }
});


invertir.addEventListener('click', () => {
    const formData = new FormData(formulario);
    const fechaHora = new Date();
    const data = {
        fecha: fechaHora.toLocaleDateString(),
        hora: fechaHora.toLocaleTimeString(),
        origen: formData.get('origen'),
        destino: formData.get('destino'),
        invertido: formData.get('invertido'),
        obtenido: obtenido.value,
        unitario: unitario.value,
    };

    fetch('/api/v1/guardar-cambio', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error al almacenar los valores');
            }
        })
        .then(json => {
            console.log(json);
            if (json.success) {
                alert('Valores almacenados correctamente');
                window.location.href = '/comprar';
            } else {
                throw new Error('Error al almacenar los valores');
            }
        })
        .catch(error => {
            console.error(error);
            alert('Error al almacenar los valores');
        });
});
