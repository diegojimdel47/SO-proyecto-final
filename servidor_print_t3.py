# Importamos la librería socket para crear conexiones de red
import socket

# Importamos logging para mostrar eventos en consola
import logging

# Configuración del logging para que imprima en consola
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | PRINT | %(message)s"
)

# HOST = 0.0.0.0 significa que el servidor aceptará conexiones
# desde cualquier dirección IP disponible en la red
HOST = "0.0.0.0"

# Puerto específico para el servicio de impresión
PORT = 5001

# Creamos el socket usando:
# AF_INET → IPv4
# SOCK_STREAM → Protocolo TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asociamos el socket al host y puerto definidos
server.bind((HOST, PORT))

# El servidor puede aceptar hasta 5 conexiones en espera
server.listen(5)

logging.info("Servidor PRINT activo y esperando conexiones")

# Bucle infinito para mantener el servidor siempre activo
while True:

    # Espera hasta que un cliente se conecte
    conn, addr = server.accept()

    # Mostramos qué cliente se conectó
    logging.info(f"Conexión recibida desde {addr}")

    # Recibimos los datos enviados (máximo 1024 bytes)
    data = conn.recv(1024).decode()

    logging.info(f"Solicitud de impresión recibida: {data}")

    # Generamos una respuesta simulando la impresión
    respuesta = f"Impresión realizada: {data}"

    # Enviamos la respuesta al middleware
    conn.send(respuesta.encode())

    logging.info("Respuesta enviada al middleware")

    # Cerramos la conexión actual
    conn.close()
