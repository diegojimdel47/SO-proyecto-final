import paramiko

# Datos de conexión
HOST = "192.168.0.26"
USER = "mrangel"
KEY_PATH = "/home/salvadormj175/.ssh/id_ed25519"

# Crear cliente SSH
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Conexión
client.connect(HOST, username=USER, key_filename=KEY_PATH)

def ejecutar(comando):
    stdin, stdout, stderr = client.exec_command(comando)
    return stdout.read().decode()

print("\n===== FIREWALL =====")
print(ejecutar("sudo /usr/bin/firewall-cmd --list-all"))

print("\n===== PUERTOS ABIERTOS =====")
print(ejecutar("ss -tuln"))

print("\n===== SERVICIOS ACTIVOS =====")
print(ejecutar("systemctl list-units --type=service --state=running"))

client.close()
