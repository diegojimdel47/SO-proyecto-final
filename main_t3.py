import os
import sys
import shlex
import platform
import subprocess
from pathlib import Path

# =========================================
# CONFIGURACIÓN: registra aquí tus programas
# =========================================
PROGRAMAS = {
    "1": {"name": "Listar procesos",    "type": "py",   "path": "listar_procesos.py",   "args": []},
    "2": {"name": "Cliente-socket (T2)", "type": "py",   "path": "cliente_t2.py",         "args": []},
    "3": {"name": "Middleware (Tarea 3)", "type": "py",   "path": "cliente_t3.py",         "args": []}, # Tu nueva parte
    "4": {"name": "Seguridad SSH",      "type": "sh",   "path": "seguridad_ssh.sh",     "args": []},
    "5": {"name": "Migrar servidores",  "type": "bin",  "path": "migrar_servidores",    "args": []},
    "6": {"name": "Salir",              "type": None,   "path": None,                  "args": []},
}

BASE_DIR = Path(__file__).parent.resolve()

def limpiar_pantalla():
    os.system("cls" if platform.system().lower().startswith("win") else "clear")

def mostrar_menu():
    print("=" * 55)
    print("      MENÚ PRINCIPAL - Orquestador Multilenguaje")
    print("=" * 55)
    # Ordenar por el número de opción
    for k in sorted(PROGRAMAS.keys(), key=lambda x: int(x)):
        print(f"{k}. {PROGRAMAS[k]['name']}")
    print("=" * 55)

def asegurar_ejecutable(ruta: Path):
    if platform.system().lower().startswith("win"): return
    try:
        if ruta.exists() and ruta.is_file():
            ruta.chmod(ruta.stat().st_mode | 0o100)
    except Exception: pass

def construir_comando(tipo: str, ruta: Path, args: list[str]) -> list[str] | str:
    if tipo == "py":   return [sys.executable, str(ruta), *args]
    if tipo == "sh":   return ["bash", str(ruta), *args]
    if tipo == "node": return ["node", str(ruta), *args]
    if tipo == "jar":  return ["java", "-jar", str(ruta), *args]
    if tipo == "bin":  return [str(ruta), *args]
    return [str(ruta), *args]

def ejecutar_programa(config: dict):
    tipo = config["type"]
    if not tipo: return

    ruta_path = Path(config["path"])
    if not ruta_path.is_absolute():
        ruta_path = (BASE_DIR / ruta_path).resolve()

    if not ruta_path.exists():
        print(f"❌ Error: No se encontró el archivo: {ruta_path}")
        return

    if tipo in ("sh", "bin"): asegurar_ejecutable(ruta_path)

    comando = construir_comando(tipo, ruta_path, config.get("args", []))
    
    print(f"\n🚀 Ejecutando: {config['name']}")
    print("-" * 55)

    try:
        # Esto ejecuta el programa en la misma terminal o abre su interfaz
        subprocess.run(comando)
    except Exception as e:
        print(f"❌ Error al ejecutar: {e}")

def main():
    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "6":
            print("Saliendo...")
            break

        if opcion in PROGRAMAS:
            ejecutar_programa(PROGRAMAS[opcion])
            input("\nPresiona ENTER para volver al menú...")
        else:
            print("Opción inválida.")
            input("ENTER para continuar...")

if __name__ == "__main__":
    main()
