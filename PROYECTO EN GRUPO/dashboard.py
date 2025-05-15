from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from config import get_pubnub_config
import signal
import sys
import time
from datetime import datetime
import os
import json
from collections import defaultdict

class EmergencyDashboard:
    def __init__(self, channel="emergencias"):
        self.channel = channel
        self.pubnub = PubNub(get_pubnub_config())
        
        # Estadísticas
        self.emergencias = {}
        self.emergencias_por_tipo = defaultdict(int)
        self.emergencias_por_ciudad = defaultdict(int)
        self.emergencias_por_gravedad = defaultdict(int)
        self.total_emergencias = 0
        self.emergencias_atendidas = 0
        self.ultima_actualizacion = None
        
        # Registrar listener
        class DashboardListener(SubscribeCallback):
            def __init__(self, dashboard):
                self.dashboard = dashboard
                
            def message(self, pubnub, message):
                self.dashboard.procesar_mensaje(message.message, message.channel)
                
        # Registrar listener y señales
        self.listener = DashboardListener(self)
        self.pubnub.add_listener(self.listener)
        signal.signal(signal.SIGINT, self.handle_shutdown)
    
    def procesar_mensaje(self, mensaje, channel):
        """Procesa los mensajes recibidos"""
        if channel == self.channel:
            # Es una emergencia
            self.total_emergencias += 1
            self.emergencias[mensaje["id"]] = mensaje
            self.emergencias_por_tipo[mensaje["tipo"]] += 1
            self.emergencias_por_ciudad[mensaje["ubicacion"]["ciudad"]] += 1
            self.emergencias_por_gravedad[mensaje["gravedad"]] += 1
        elif channel == f"{self.channel}_respuestas":
            # Es una respuesta a emergencia
            if mensaje["emergencia_id"] in self.emergencias:
                self.emergencias[mensaje["emergencia_id"]]["atendida"] = True
                self.emergencias[mensaje["emergencia_id"]]["hospital"] = mensaje["hospital_id"]
                self.emergencias_atendidas += 1
        
        self.ultima_actualizacion = datetime.now()
        self.mostrar_dashboard()
    
    def mostrar_dashboard(self):
        """Muestra el dashboard en la consola"""
        # Limpiar terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"{'=' * 70}")
        print(f"🚨 PANEL DE CONTROL DEL SISTEMA DE EMERGENCIAS 🚨")
        print(f"{'=' * 70}")
        print(f"⏰ Última actualización: {self.ultima_actualizacion.strftime('%H:%M:%S') if self.ultima_actualizacion else 'N/A'}")
        print(f"📊 RESUMEN:")
        print(f"  - Total emergencias: {self.total_emergencias}")
        print(f"  - Emergencias atendidas: {self.emergencias_atendidas}")
        print(f"  - Pendientes: {self.total_emergencias - self.emergencias_atendidas}")
        
        # Estadísticas por tipo
        print(f"\n📋 POR TIPO DE EMERGENCIA:")
        for tipo, count in sorted(self.emergencias_por_tipo.items(), key=lambda x: x[1], reverse=True):
            porcentaje = (count / self.total_emergencias) * 100 if self.total_emergencias > 0 else 0
            print(f"  - {tipo}: {count} ({porcentaje:.1f}%)")
        
        # Estadísticas por ciudad
        print(f"\n🏙️ POR CIUDAD:")
        for ciudad, count in sorted(self.emergencias_por_ciudad.items(), key=lambda x: x[1], reverse=True):
            porcentaje = (count / self.total_emergencias) * 100 if self.total_emergencias > 0 else 0
            print(f"  - {ciudad}: {count} ({porcentaje:.1f}%)")
        
        # Estadísticas por gravedad
        print(f"\n⚠️ POR GRAVEDAD:")
        for gravedad, count in sorted(self.emergencias_por_gravedad.items(), key=lambda x: x[1], reverse=True):
            porcentaje = (count / self.total_emergencias) * 100 if self.total_emergencias > 0 else 0
            print(f"  - {gravedad}: {count} ({porcentaje:.1f}%)")
        
        # Últimas 5 emergencias
        print(f"\n🆕 ÚLTIMAS EMERGENCIAS:")
        ultimas = sorted(self.emergencias.values(), key=lambda x: x["timestamp"], reverse=True)[:5]
        for e in ultimas:
            timestamp = datetime.fromtimestamp(e["timestamp"]).strftime("%H:%M:%S")
            estado = "✅ Atendida" if e.get("atendida", False) else "⏳ Pendiente"
            hospital = f" por {e.get('hospital', 'N/A')}" if e.get("atendida", False) else ""
            print(f"  - [{timestamp}] {e['tipo']} en {e['ubicacion']['ciudad']} ({e['gravedad']}) - {estado}{hospital}")
    
    def iniciar(self):
        """Inicia el dashboard"""
        print("🚀 Iniciando Panel de Control...")
        
        # Suscribirse a canales
        self.pubnub.subscribe().channels([self.channel, f"{self.channel}_respuestas"]).execute()
        
        try:
            # Mantener el programa en ejecución
            while True:
                time.sleep(1)
        except Exception as e:
            print(f"❌ Error: {e}")
            self.detener()
    
    def detener(self):
        """Detiene el dashboard"""
        print("\n🛑 Cerrando Panel de Control...")
        self.pubnub.unsubscribe().channels([self.channel, f"{self.channel}_respuestas"]).execute()
        self.pubnub.remove_listener(self.listener)
    
    def handle_shutdown(self, signum, frame):
        self.detener()
        sys.exit(0)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Panel de Control del Sistema de Emergencias')
    parser.add_argument('--channel', type=str, default='emergencias', help='Canal principal de emergencias')
    
    args = parser.parse_args()
    
    dashboard = EmergencyDashboard(channel=args.channel)
    dashboard.iniciar()