import random
import time
import uuid
from enum import Enum
from dataclasses import dataclass

class TipoEmergencia(Enum):
    INFARTO = "Infarto"
    ACCIDENTE = "Accidente"
    INCENDIO = "Incendio"
    DERRUMBE = "Derrumbe"
    PARO_RESPIRATORIO = "Paro respiratorio"
    INUNDACION = "Inundación"
    INTOXICACION = "Intoxicación"

class Ciudad(Enum):
    MADRID = "Madrid"
    BARCELONA = "Barcelona"
    VALENCIA = "Valencia"
    SEVILLA = "Sevilla"
    ZARAGOZA = "Zaragoza"
    MALAGA = "Málaga"

class NivelGravedad(Enum):
    ALTA = "Alta"
    MEDIA = "Media"
    BAJA = "Baja"
    CRITICA = "Crítica"

@dataclass
class Ubicacion:
    ciudad: str
    direccion: str = ""
    coordenadas: tuple = None
    
    @staticmethod
    def generar():
        ciudad = random.choice(list(Ciudad)).value
        calles = ["Gran Vía", "Avenida Central", "Calle Mayor", "Plaza Principal", "Paseo Marítimo"]
        numeros = list(range(1, 100))
        direccion = f"{random.choice(calles)}, {random.choice(numeros)}"
        return Ubicacion(ciudad=ciudad, direccion=direccion)

class Urgencia:
    @staticmethod
    def generar():
        tipo = random.choice(list(TipoEmergencia)).value
        gravedad = random.choice(list(NivelGravedad)).value
        ubicacion = Ubicacion.generar()
        
        # Determinar recursos necesarios según tipo y gravedad
        recursos_necesarios = Urgencia._calcular_recursos(tipo, gravedad)
        
        return {
            "id": str(uuid.uuid4()),
            "tipo": tipo,
            "ubicacion": {
                "ciudad": ubicacion.ciudad,
                "direccion": ubicacion.direccion
            },
            "gravedad": gravedad,
            "recursos_necesarios": recursos_necesarios,
            "timestamp": time.time(),
            "atendida": False
        }
    
    @staticmethod
    def _calcular_recursos(tipo, gravedad):
        recursos = {
            "ambulancias": 1,
            "medicos": 1,
            "bomberos": 0,
            "policia": 0
        }
        
        # Aumentar recursos según tipo
        if tipo == TipoEmergencia.INFARTO.value or tipo == TipoEmergencia.PARO_RESPIRATORIO.value:
            recursos["medicos"] += 1
        elif tipo == TipoEmergencia.ACCIDENTE.value:
            recursos["ambulancias"] += 1
            recursos["policia"] = 1
        elif tipo == TipoEmergencia.INCENDIO.value:
            recursos["bomberos"] = 2
            recursos["ambulancias"] = 1
        elif tipo == TipoEmergencia.DERRUMBE.value:
            recursos["bomberos"] = 3
            recursos["ambulancias"] = 2
            recursos["policia"] = 2
        
        # Multiplicar según gravedad
        if gravedad == NivelGravedad.ALTA.value:
            recursos = {k: v * 1.5 for k, v in recursos.items()}
        elif gravedad == NivelGravedad.CRITICA.value:
            recursos = {k: v * 2 for k, v in recursos.items()}
        
        # Convertir a enteros
        recursos = {k: int(v) for k, v in recursos.items()}
        
        return recursos