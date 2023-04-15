const peticion = new XMLHttpRequest();
console.log('estoy bien')

function enviar() {
    const usuario = document.querySelector('#usuario').value;
    const contrasena = document.querySelector('#contrasena').value;
    const fechaHora = new Date();

    console.log('pase por aqui');


    fetch('http://127.0.0:4000/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            usuario: usuario,
            contrasena: contrasena,
            fecha: fechaHora.toLocaleDateString(),
            hora: fechaHora.toLocaleTimeString()
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error(error);
        });
}