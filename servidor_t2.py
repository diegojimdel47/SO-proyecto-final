# server_t2.py
import socket

HOST = '0.0.0.0'  # Escucha desde cualquier IP
PORT = 5001       # Puerto de escucha

# Crear el socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)  # Hasta 5 clientes en espera

print(f"[SERVIDOR] Activo en {HOST}:{PORT}")

while True:
    conn, addr = server.accept()  # Espera una conexión
    print(f"[SERVIDOR] Cliente conectado desde {addr}")

    # Recibir mensaje del cliente (máx 1024 bytes)
    data = conn.recv(1024).decode()
    if data:
        print(f"[SERVIDOR] Mensaje recibido: {data}")
        # Responder al cliente
        conn.send(f"Servidor recibió: {data}".encode())

    conn.close()  # Cerrar conexión actual
    print(f"[SERVIDOR] Conexión con {addr} cerrada\n")

