# Importamos socket para manejar conexiones de red
import socket

# Importamos logging para mostrar información en consola
import logging

# Configuración del sistema de logging
# level=logging.INFO → mostrará mensajes informativos y errores
# format → define cómo se verá cada mensaje en consola
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | LOG | %(message)s"
)

# HOST 0.0.0.0 permite que el servidor acepte conexiones
# desde cualquier IP dentro de la red
HOST = "0.0.0.0"

# Puerto exclusivo para el servicio de logging
PORT = 5003

# Creamos el socket TCP usando IPv4
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asociamos el socket al host y puerto definidos
server.bind((HOST, PORT))

# Permitimos hasta 5 conexiones en espera
server.listen(5)

logging.info("Servidor LOG activo y esperando mensajes")

# Bucle infinito para mantener el servidor activo constantemente
while True:

    # Espera a que el middleware se conecte
    conn, addr = server.accept()

    # Mostramos desde qué dirección IP se conectaron
    logging.info(f"Conexión recibida desde {addr}")

    # Recibimos el mensaje enviado por el middleware
    mensaje = conn.recv(1024).decode()

    # Mostramos el mensaje recibido en consola
    # Este servidor actúa como sistema de registro en tiempo real
    logging.info(f"Evento registrado: {mensaje}")

    # Confirmamos al middleware que el mensaje fue registrado
    respuesta = "Mensaje registrado correctamente en consola"

    # Enviamos la confirmación
    conn.send(respuesta.encode())

    # Cerramos la conexión actual
    conn.close()
