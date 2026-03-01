import socket
import logging

# Configuración de logging para el cliente
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | CLIENTE | %(message)s"
)

# IP del middleware (debe ser la IP real del equipo que lo ejecuta)
MIDDLEWARE_IP = "127.0.0.1"
PORT = 4000

while True:

    # Solicita al usuario que escriba una petición
    mensaje = input("Petición (print/math/log:mensaje) o 'salir': ")

    if mensaje.lower() == "salir":
        logging.info("Cliente finalizó ejecución")
        break

    # Crear socket para conectarse al middleware
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectarse al middleware
    cliente.connect((MIDDLEWARE_IP, PORT))

    logging.info(f"Enviando petición: {mensaje}")

    # Enviar mensaje al middleware
    cliente.send(mensaje.encode())

    # Recibir respuesta
    respuesta = cliente.recv(1024).decode()

    logging.info(f"Respuesta recibida: {respuesta}")

    print("Respuesta:", respuesta)

    # Cerrar conexión
    cliente.close()
