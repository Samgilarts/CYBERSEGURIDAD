# Grupo 4: Escaneo de Puertos y Servicios (4 estudiantes)
from typing import Dict, Any
import socket
import datetime

def scan_ports_dispatcher(target, ports):
    """Orquestador para el Grupo 4"""
    print(f"  [G4] Iniciando escaneo de puertos en {target} ({ports})")
    # Aquí se reparten las tareas entre los 4 estudiantes:
    raise NotImplementedError("El escáner de puertos (Grupo 4) estará disponible en la Semana 3.")
    
def scan_ports_dispatcher(target: str, ports: str) -> Dict[str, Any]:
    """
    Realiza un escaneo de puertos TCP/UDP a un objetivo específico.

    Args:
        target (str): La dirección IP o dominio a escanear.
        ports (str): Cadena con los puertos separados por comas (ej. '80,443,22').

    Returns:
        Dict[str, Any]: Diccionario con los resultados de la auditoría,
        cumpliendo con el esquema definido en docs/schema_resultados.json.
    """
    resultado = {
        "modulo": "Scanning",
        "grupo": 4,
        "estudiante": "E1", # En este caso el orquestador o estudiante a cargo
        "target": target,
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "success",
        "data": {},
        "error_message": None
    }

    try:
        # 1. Obtenemos la IP una sola vez
        target_ip = socket.gethostbyname(target)
        # Esto va dentro del try, después de obtener target_ip

        # 2. Procesar entrada de puertos
        puertos_lista = [int(p.strip()) for p in ports.split(",") if p.strip().isdigit()]
        resultados_puertos = []
        
        # 3. Bucle de escaneo
        for puerto in puertos_lista:
            # Crear socket TCP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            
            # Intentar conexión
            result_code = sock.connect_ex((target_ip, puerto))
            
            estado = "abierto" if result_code == 0 else "cerrado"
            
            resultados_puertos.append({
                "puerto": puerto,
                "estado": estado,
                "protocolo": "TCP"
            })
            sock.close() # Cerramos el socket de este puerto

      # 4. Guardar resultados en el diccionario principal
        resultado["data"] = {
            "puertos_escaneados": puertos_lista,
            "detalles": resultados_puertos,
            "resumen": {
                "total": len(puertos_lista),
                # Aquí contamos cuántos tienen el estado "abierto"
                "abiertos": sum(1 for p in resultados_puertos if p["estado"] == "abierto")
            }
        }
        
    except Exception as e:
        # Aquí es donde capturamos el desastre y lo explicamos
        resultado["status"] = "error"
        
        # Podemos verificar si el error es de DNS (dominio no encontrado)
        if "getaddrinfo failed" in str(e) or "gaierror" in str(e):
            resultado["error_message"] = "Error: Dominio desconocido o no resuelto."
        else:
            resultado["error_message"] = f"Error en el escaneo: {str(e)}"

    return resultado
# Bloque de prueba local para el estudiante
if __name__ == "__main__":
    import json
    print("[*] Ejecutando prueba local...")
    resultado_prueba = scan_ports_dispatcher("8.8.8.8", "22, 80, 443")
    print(json.dumps(resultado_prueba, indent=4))
    
