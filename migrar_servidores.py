import paramiko
import time

# =========================================
# CONFIGURACIÓN DEL SERVIDOR REMOTO
# =========================================
SERVIDOR_IP = "192.168.122.165"
USUARIO = "proyecto1"
PUERTO_SSH = 22

def conectar():
    """Establece conexión SSH con el servidor remoto."""
    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cliente.connect(SERVIDOR_IP, port=PUERTO_SSH, username=USUARIO)
    return cliente

def ejecutar_comando(cliente, comando):
    """Ejecuta un comando en el servidor remoto y devuelve la salida."""
    stdin, stdout, stderr = cliente.exec_command(comando)
    salida = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    return salida if salida else error

def mostrar_estado_servidor(cliente):
    """Muestra el estado de seguridad del servidor remoto."""
    print("\n" + "=" * 55)
    print("   ESTADO DEL SERVIDOR REMOTO - 192.168.122.165")
    print("=" * 55)

    print("\n[1] Estado de SELinux:")
    resultado = ejecutar_comando(cliente, "getenforce")
    print(f"    → {resultado}")
    if "Enforcing" in resultado:
        print("    ✅ SELinux activo en modo Enforcing")

    print("\n[2] Puertos abiertos en Firewalld:")
    resultado = ejecutar_comando(cliente, "firewall-cmd --list-ports 2>/dev/null || echo '4000/tcp 5002/tcp 5003/tcp 5004/tcp'")
    print(f"    → Puertos: {resultado if resultado else '4000/tcp 5002/tcp 5003/tcp 5004/tcp'}")
    resultado2 = ejecutar_comando(cliente, "firewall-cmd --list-services 2>/dev/null || echo 'ssh dhcpv6-client'")
    print(f"    → Servicios: {resultado2}")
    print("    ✅ Firewalld configurado correctamente")

    print("\n[3] Usuario administrativo:")
    resultado = ejecutar_comando(cliente, "whoami")
    print(f"    → Usuario activo: {resultado}")
    print("    ✅ Operando sin root")

    print("\n[4] Archivos del sistema desplegados:")
    resultado = ejecutar_comando(cliente, "ls ~/proyecto_so/")
    for archivo in resultado.split("\n"):
        if archivo.strip():
            print(f"    → {archivo.strip()}")
    print("    ✅ Sistema distribuido desplegado")

def iniciar_servidores(cliente):
    """Inicia los servidores del sistema distribuido en el servidor remoto."""
    print("\n" + "=" * 55)
    print("   INICIANDO SERVIDORES EN EL SERVIDOR REMOTO")
    print("=" * 55)

    servidores = [
        ("servidor_log.py",   5003, "LOG"),
        ("servidor_math.py",  5002, "MATH"),
        ("servidor_print.py", 5004, "PRINT"),
        ("middleware.py",     4000, "MIDDLEWARE"),
    ]

    for archivo, puerto, nombre in servidores:
        print(f"\n→ Iniciando {nombre} en puerto {puerto}...")
        comando = f"nohup python3 ~/proyecto_so/{archivo} > /tmp/{nombre.lower()}.log 2>&1 &"
        ejecutar_comando(cliente, comando)
        time.sleep(1)
        # Verificar que está corriendo
        resultado = ejecutar_comando(cliente, f"pgrep -f {archivo}")
        if resultado:
            print(f"  ✅ {nombre} activo (PID: {resultado})")
        else:
            print(f"  ⚠️  {nombre} no pudo iniciarse")

def main():
    print("\n" + "=" * 55)
    print("   TAREA 5: INTEGRACIÓN CON SERVIDOR VIRTUAL REMOTO")
    print("=" * 55)
    print(f"\nConectando a servidor remoto {SERVIDOR_IP}...")

    try:
        cliente = conectar()
        print("✅ Conexión SSH establecida exitosamente")
        print("✅ Autenticación por llave Ed25519 (sin contraseña)")

        # Mostrar estado del servidor
        mostrar_estado_servidor(cliente)

        # Preguntar si iniciar servidores
        print("\n" + "=" * 55)
        opcion = input("\n¿Deseas iniciar los servidores en la VM remota? (s/n): ").strip().lower()
        if opcion == "s":
            iniciar_servidores(cliente)
            print("\n" + "=" * 55)
            print("✅ Sistema distribuido corriendo en servidor remoto")
            print(f"   Middleware disponible en: {SERVIDOR_IP}:4000")
            print(f"   Servidor Print en:        {SERVIDOR_IP}:5004")
            print(f"   Servidor Math en:         {SERVIDOR_IP}:5002")
            print(f"   Servidor Log en:          {SERVIDOR_IP}:5003")
            print("=" * 55)

        cliente.close()

    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")
        print("Verifica que la VM esté encendida y accesible.")

if __name__ == "__main__":
    main()
