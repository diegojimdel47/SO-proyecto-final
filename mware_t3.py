import socket
import logging

# Configuración del logging para mostrar eventos del middleware
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | MIDDLEWARE | %(message)s"
)

HOST = "0.0.0.0"
PORT = 4000  # Puerto donde escucha el middleware

# Diccionario que relaciona tipo de servicio con IP y puerto
# Aquí se define hacia dónde redirigir cada solicitud
SERVICIOS = {
    "print": ("127.0.0.1", 5001),  # IP y puerto del servidor Print
    "math":  ("127.0.0.1", 5002),    # IP y puerto del servidor Math
    "log":   ("127.0.0.1", 5003)     # IP y puerto del servidor Log
}

middleware = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
middleware.bind((HOST, PORT))
middleware.listen(5)

logging.info("Middleware activo y esperando clientes")

while True:

    # Espera conexión del cliente
    cliente, addr = middleware.accept()
    logging.info(f"Cliente conectado desde {addr}")

    # Recibe la petición del cliente
    peticion = cliente.recv(1024).decode()
    logging.info(f"Petición recibida: {peticion}")

    try:
        # Separar tipo de servicio y mensaje
        # Ejemplo recibido: "math:5*8"
        tipo, mensaje = peticion.split(":", 1)

        # Buscar IP y puerto del servicio solicitado
        ip, puerto = SERVICIOS[tipo]

        logging.info(f"Redirigiendo a servicio {tipo} en {ip}:{puerto}")

        # Crear socket para conectarse al servidor correspondiente
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.connect((ip, puerto))

        # Enviar mensaje al servidor específico
        servidor.send(mensaje.encode())

        # Recibir respuesta del servidor
        respuesta = servidor.recv(1024).decode()

        servidor.close()

        logging.info("Respuesta recibida del servidor correctamente")

    except Exception as e:
        respuesta = "Servicio no disponible"
        logging.error(f"Error al procesar solicitud: {e}")

    # Enviar respuesta final al cliente
    cliente.send(respuesta.encode())

    # Cerrar conexión con cliente
    cliente.close()
