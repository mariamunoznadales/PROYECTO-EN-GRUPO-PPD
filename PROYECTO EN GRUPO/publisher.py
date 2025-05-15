from pubnub.pubnub import PubNub
from config import get_pubnub_config
from urgencia import Urgencia
import time
import json
import argparse
import signal
import sys

class EmergencyPublisher:
    def __init__(self, channel="emergencias", intervalo=5):
        self.pubnub = PubNub(get_pubnub_config())
        self.channel = channel
        self.intervalo = intervalo
        self.running = False
        self.total_enviadas = 0
        
        # Registrar manejador para cierre ordenado
        signal.signal(signal.SIGINT, self.handle_shutdown)
    
    def publicar_emergencia(self):
        mensaje = Urgencia.generar()
        self.total_enviadas += 1
        print(f"📤 #{self.total_enviadas} Publicando emergencia: {mensaje['tipo']} en {mensaje['ubicacion']['ciudad']}")
        
        envelope = self.pubnub.publish().channel(self.channel).message(mensaje).sync()
        if envelope.status.is_error():
            print(f"❌ Error al publicar: {envelope.status.error_data.information}")
        else:
            print(f"✅ Publicada con éxito. Timetoken: {envelope.result.timetoken}")
        
        return mensaje
    
    def iniciar(self):
        self.running = True
        print(f"🚑 Iniciando sistema de publicación en canal '{self.channel}'")
        print(f"⏱️ Intervalo de publicación: {self.intervalo} segundos")
        
        try:
            while self.running:
                self.publicar_emergencia()
                time.sleep(self.intervalo)
        except Exception as e:
            print(f"❌ Error en el publicador: {e}")
            self.detener()
    
    def detener(self):
        self.running = False
        print(f"\n🛑 Deteniendo sistema. Total de emergencias enviadas: {self.total_enviadas}")
    
    def handle_shutdown(self, signum, frame):
        self.detener()
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sistema de publicación de emergencias')
    parser.add_argument('--intervalo', type=int, default=5, help='Intervalo entre emergencias (segundos)')
    parser.add_argument('--channel', type=str, default='emergencias', help='Canal de publicación')
    
    args = parser.parse_args()
    
    publicador = EmergencyPublisher(channel=args.channel, intervalo=args.intervalo)
    publicador.iniciar()