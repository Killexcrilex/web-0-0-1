function    Carrito() {
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
}