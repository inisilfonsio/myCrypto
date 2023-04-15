const formulario = document.querySelector('#form-status');
const botonComprobar = document.querySelector('#btn-comprobar');
const simbolosMoneda = document.querySelectorAll('.moneda');

botonComprobar.addEventListener('click', async (event) => {
    event.preventDefault();

    const response = await fetch('/status', {
        method: 'POST',
        body: new FormData(formulario),
    });

    const { invertido, valorTotalCartera, beneficio, mensaje } = await response.json();

    document.getElementById('invertido').textContent = invertido;
    document.getElementById('valorTotalCartera').textContent = valorTotalCartera;
    document.getElementById('beneficio').textContent = beneficio;

    // Mostrar los símbolos
    simbolosMoneda.forEach((span) => {
        span.style.display = 'inline';
    });
});

