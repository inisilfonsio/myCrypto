const formulario = document.querySelector('#form-comprar');
const obtenido = document.querySelector('#obtenido');
const unitario = document.querySelector('#unitario');
const invertir = document.querySelector('#invertir');
const calcular = document.querySelector('#calcular')


calcular.addEventListener('click', async (event) => {
    event.preventDefault();
    console.log("estoy dentro");

    const response = await fetch('/api/v1/consultar-cambio', {
        method: 'POST',
        body: new FormData(formulario),
    });

    const { obtenido: obtenidoValor, unitario: valorUnitario } = await response.json();

    obtenido.value = obtenidoValor.toFixed(5);
    document.getElementById("crypto-destino").textContent = document.getElementById("destino").value;
    unitario.value = (valorUnitario).toFixed(5);
    document.getElementById("crypto-origen").textContent = document.getElementById("origen").value;

    invertir.disabled = false;
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
            } else {
                throw new Error('Error al almacenar los valores');
            }
        })
        .catch(error => {
            console.error(error);
            alert('Error al almacenar los valores');
        });
});
