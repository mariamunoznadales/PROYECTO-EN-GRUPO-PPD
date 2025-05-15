from pubnub.pnconfiguration import PNConfiguration
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()

def get_pubnub_config():
    pnconfig = PNConfiguration()
    # Obtener claves de variables de entorno
    pnconfig.subscribe_key = os.environ.get('PUBNUB_SUBSCRIBE_KEY', 'sub-c-a2df94ac-367c-4af8-bc59-17fd53873061')
    pnconfig.publish_key = os.environ.get('PUBNUB_PUBLISH_KEY', 'pub-c-d9c60cc2-2dc9-40ef-99d1-bcd402be43d3')
    pnconfig.uuid = os.environ.get('PUBNUB_UUID', 'sistema-alerta')
    pnconfig.region = "eu"
    pnconfig.ssl = True
    return pnconfig