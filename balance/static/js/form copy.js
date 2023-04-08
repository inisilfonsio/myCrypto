const formulario = document.querySelector('#form-comprar');
const obtenido = document.querySelector('#obtenido');
const valorUnitario = document.querySelector('#valor-unitario');
const invertir = document.querySelector('#invertir');

formulario.addEventListener('submit', async (event) => {
    event.preventDefault();

    const response = await fetch('http://127.0.0.1:4000/comprar', {
        method: 'POST',
        body: new FormData(formulario),
    });

    const { tasa_de_cambio, valor_unitario } = await response.json();

    obtenido.value = invertido.value * tasa_de_cambio;
    valorUnitario.value = valor_unitario;
    invertir.disabled = false;
});

invertir.addEventListener('click', async () => {
    const response = await fetch('/almacenar-valores', {
        method: 'POST',
        body: new FormData(formulario),
    });

    const { success } = await response.json();

    if (success) {
        alert('Valores almacenados correctamente');
    } else {
        alert('No se pudo almacenar los valores');
    }
});
