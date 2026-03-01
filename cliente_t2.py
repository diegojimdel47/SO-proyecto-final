# client_t2.py
import socket

HOST = '127.0.0.1'  # IP del servidor
PORT = 5001         # Puerto del servidor

print("=== Cliente TCP para Tarea 2 ===")

while True:
    mensaje = input("Escribe un mensaje (o 'salir' para terminar): ")
    if mensaje.lower() == "salir":
        print("[CLIENTE] Saliendo...")
        break

    # Crear socket y conectarse al servidor
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Enviar mensaje
    client.send(mensaje.encode())

    # Recibir respuesta
    respuesta = client.recv(1024).decode()
    print(f"[CLIENTE] Respuesta del servidor: {respuesta}")

    client.close()  # Cerrar conexión

