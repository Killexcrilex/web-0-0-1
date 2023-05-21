/*function    Carrito() {
    // Obtener la fecha y hora actual
    var fecha = new Date();
    
    // Generar un número de ticket aleatorio
    var numeroTicket = Math.floor(Math.random() * 1000) + 1;
    
    // Crear el contenido del ticket
    var contenidoTicket = "-------- Ticket --------\n";
    contenidoTicket += "Fecha: " + fecha.toLocaleDateString() + "\n";
    contenidoTicket += "Hora: " + fecha.toLocaleTimeString() + "\n";
    contenidoTicket += "Número de Ticket: " + numeroTicket + "\n";
    contenidoTicket += "------------------------";
    
    // Mostrar el contenido del ticket en la consola
    console.log(contenidoTicket);
    
    // Aquí puedes agregar código adicional para imprimir el ticket o realizar otras acciones con él
}*/

function incrementarValor(input) {
    var valor = parseInt(input.value);
    if (!isNaN(valor)) {
      valor++;
      input.value = valor;
    }
  }


  function decrementarValor(input) {
    var valor = parseInt(input.value);
    if (!isNaN(valor) && valor > 0) {
      valor--;
      input.value = valor;
    }
  }
  

  function agregarAlCarrito(nombreProducto, precioProducto, cantidadSeleccionada) {
    var total = parseFloat(precioProducto) * parseInt(cantidadSeleccionada);

    var carrito = {
        producto: nombreProducto,
        precio: precioProducto,
        cantidad: cantidadSeleccionada,
        total: total
    };

    // Aquí puedes realizar la lógica para enviar el objeto "carrito" al servidor y realizar la inserción en la tabla "carrito".
    // Puedes utilizar una solicitud AJAX o cualquier otra forma de comunicación con el servidor para realizar la inserción en la base de datos.

    console.log(carrito); // Muestra el objeto carrito en la consola para fines de demostración
}


function generarTicket() {
  $.ajax({
    url: '/guardar-ticket', // Ruta del servidor que genera el ticket
    type: 'GET',
    success: function(response) {
      console.log('Ticket generado correctamente');
      // Aquí puedes realizar cualquier otra acción después de generar el ticket
    },
    error: function(error) {
      console.error('Error al generar el ticket:', error);
    }
  });
}