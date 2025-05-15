from base_hospital import BaseHospital
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sistema receptor de emergencias - Hospital A')
    parser.add_argument('--channel', type=str, default='emergencias', help='Canal de suscripción')
    parser.add_argument('--filtro-ciudad', type=str, action='append', help='Filtrar por ciudad')
    parser.add_argument('--filtro-tipo', type=str, action='append', help='Filtrar por tipo de emergencia')
    parser.add_argument('--filtro-gravedad', type=str, action='append', help='Filtrar por nivel de gravedad')
    
    args = parser.parse_args()
    
    # Configurar filtros
    filtros = {}
    if args.filtro_ciudad:
        filtros["ubicacion"] = args.filtro_ciudad
    if args.filtro_tipo:
        filtros["tipo"] = args.filtro_tipo
    if args.filtro_gravedad:
        filtros["gravedad"] = args.filtro_gravedad
    
    # Iniciar hospital
    hospital = BaseHospital(
        hospital_id="Hospital A", 
        channel=args.channel,
        filtros=filtros
    )
    hospital.iniciar()