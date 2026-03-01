import socket
import logging

# Configuración de logging en consola
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | MATH | %(message)s"
)

HOST = "0.0.0.0"
PORT = 5002  # Puerto exclusivo para operaciones matemáticas

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

logging.info("Servidor MATH activo y esperando operaciones")

while True:

    # Espera conexión del middleware
    conn, addr = server.accept()
    logging.info(f"Conexión recibida desde {addr}")

    # Recibe la operación matemática como texto
    operacion = conn.recv(1024).decode()
    logging.info(f"Operación recibida: {operacion}")

    try:
        # eval() ejecuta la operación matemática recibida
        resultado = eval(operacion)

        respuesta = f"Resultado: {resultado}"
        logging.info(f"Resultado calculado correctamente: {resultado}")

    except Exception as e:
        # Si ocurre un error (ej: operación inválida)
        respuesta = "Error en la operación"
        logging.error(f"Error al procesar operación: {e}")

    # Enviamos el resultado al middleware
    conn.send(respuesta.encode())

    # Cerramos conexión
    conn.close()
