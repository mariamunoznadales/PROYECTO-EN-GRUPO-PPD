# Sistema de Emergencias Distribuido en Tiempo Real

Este proyecto simula una red de emergencias médicas utilizando programación distribuida y eventos en tiempo real. Permite generar emergencias aleatorias, distribuirlas a hospitales con filtros personalizados, y visualizar toda la actividad en una interfaz gráfica.

## Objetivo

Simular un sistema de emergencias en tiempo real con múltiples agentes (generador, hospitales, panel de control), todos funcionando de forma concurrente y comunicándose a través de PubNub.

---

## Estructura del proyecto
├── publisher.py # Generador de emergencias

├── urgencia.py # Lógica para crear emergencias

├── base_hospital.py # Lógica común para hospitales

├── hospital_a.py # Hospital con filtros configurables

├── hospital_b.py # Otro hospital

├── dashboard.py # Visualización por consola

├── interfaz_dashboard.py # Interfaz gráfica (Tkinter)

├── config.py # Carga claves desde .env

├── .env # Claves de PubNub (no se sube)


## Configuración

Crea un archivo .env en la raíz del proyecto:

PUBNUB_PUBLISH_KEY=tu publish key

PUBNUB_SUBSCRIBE_KEY=tu subscribe key

UUID=interfaz_dashboard


## Ejecución paso a paso

1. Abre 3 terminales o pestañas:

Terminal 1 – Interfaz gráfica

python3 interfaz_dashboard.py

Terminal 2 – Generador de emergencias

python3 publisher.py --intervalo 3 --channel emergencias

Terminal 3 – Hospitales

python3 hospital_a.py 
python3 hospital_b.py



