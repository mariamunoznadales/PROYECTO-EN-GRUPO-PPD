from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from config import get_pubnub_config
import json
import signal
import sys
import time
from datetime import datetime
import os

class BaseHospital:
    def __init__(self, hospital_id, channel="emergencias", filtros=None):
        self.hospital_id = hospital_id
        self.channel = channel
        self.filtros = filtros or {}
        self.emergencias_recibidas = 0
        self.emergencias_atendidas = 0
        self.pubnub = PubNub(get_pubnub_config())
        
        # Registrar manejador para cierre ordenado
        signal.signal(signal.SIGINT, self.handle_shutdown)
        
        # Crear listener personalizado
        class HospitalListener(SubscribeCallback):
            def __init__(self, hospital):
                self.hospital = hospital
                
            def message(self, pubnub, message):
                self.hospital.procesar_emergencia(message.message)
                
        # Registrar listener
        self.listener = HospitalListener(self)
        self.pubnub.add_listener(self.listener)
    
    def procesar_emergencia(self, emergencia):
        self.emergencias_recibidas += 1
        
        # Verificar si cumple con los filtros
        if self.filtrar_emergencia(emergencia):
            timestamp = datetime.fromtimestamp(emergencia['timestamp']).strftime('%H:%M:%S')
            
            # Limpiar terminal en sistemas compatibles
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"\n{'=' * 50}")
            print(f"🏥 [{self.hospital_id.upper()}] ALERTA DE EMERGENCIA #{self.emergencias_recibidas}")
            print(f"{'=' * 50}")
            print(f"🆔 ID: {emergencia['id']}")
            print(f"⏰ Hora: {timestamp}")
            print(f"🚨 Tipo: {emergencia['tipo']}")
            print(f"📍 Ubicación: {emergencia['ubicacion']['ciudad']}, {emergencia['ubicacion']['direccion']}")
            print(f"⚠️ Gravedad: {emergencia['gravedad']}")
            print(f"🚑 Recursos necesarios:")
            for recurso, cantidad in emergencia['recursos_necesarios'].items():
                if cantidad > 0:
                    print(f"  - {recurso.capitalize()}: {cantidad}")
            
            self.atender_emergencia(emergencia)
    
    def filtrar_emergencia(self, emergencia):
        """Verifica si la emergencia cumple con los filtros configurados"""
        for clave, valor in self.filtros.items():
            if clave == "ubicacion":
                if emergencia["ubicacion"]["ciudad"] not in valor:
                    return False
            elif clave in emergencia and emergencia[clave] not in valor:
                return False
        return True
    
    def atender_emergencia(self, emergencia):
        """Procesa la atención de una emergencia"""
        self.emergencias_atendidas += 1
        print(f"\n✅ Emergencia siendo atendida por {self.hospital_id}")
        print(f"📊 Estadísticas:")
        print(f"  - Total recibidas: {self.emergencias_recibidas}")
        print(f"  - Total atendidas: {self.emergencias_atendidas}")
        
        # Publicar respuesta (opcional)
        respuesta = {
            "hospital_id": self.hospital_id,
            "emergencia_id": emergencia["id"],
            "mensaje": f"Emergencia atendida por {self.hospital_id}",
            "timestamp": time.time()
        }
        
        self.pubnub.publish().channel(f"{self.channel}_respuestas").message(respuesta).sync()
    
    def iniciar(self):
        """Inicia la escucha de emergencias"""
        print(f"🏥 Hospital {self.hospital_id} iniciando...")
        print(f"📡 Escuchando en canal: {self.channel}")
        if self.filtros:
            print(f"🔍 Filtros activos: {self.filtros}")
        
        self.pubnub.subscribe().channels(self.channel).execute()
        
        try:
            # Mantener el programa en ejecución
            while True:
                time.sleep(1)
        except Exception as e:
            print(f"❌ Error: {e}")
            self.detener()
    
    def detener(self):
        """Detiene la escucha de emergencias"""
        print(f"\n🛑 Hospital {self.hospital_id} cerrando...")
        print(f"📊 Resumen final:")
        print(f"  - Emergencias recibidas: {self.emergencias_recibidas}")
        print(f"  - Emergencias atendidas: {self.emergencias_atendidas}")
        
        self.pubnub.unsubscribe().channels(self.channel).execute()
        self.pubnub.remove_listener(self.listener)
    
    def handle_shutdown(self, signum, frame):
        self.detener()
        sys.exit(0)