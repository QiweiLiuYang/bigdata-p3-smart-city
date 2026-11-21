import random
from datetime import datetime, timedelta, timezone
from influxdb_client_3 import InfluxDBClient3, Point
import os

TOKEN = os.environ.get("INFLUX_TOKEN", "sin-auth")  # con --without-auth vale cualquier valor
cliente = InfluxDBClient3(host="http://localhost:8181", database="smartcity", token=TOKEN)
SENSORES_TEMP_HUM = ["temp-001", "temp-002", "temp-003"]
SENSORES_CO2 = ["co2-001", "co2-002"]
SENSORES_CALIDAD_AGUA = ["agua-001", "agua-002"]

def simular_lectura_temp_hum(sensor_id: str, instante: datetime) -> Point:
    return (
        Point("temperatura_humedad")
        .tag("sensor_id", sensor_id)
        .field("temperatura", round(random.uniform(18, 32), 1))
        .field("humedad", round(random.uniform(30, 70), 1))
        .time(instante)
    )


def simular_lectura_co2(sensor_id: str, instante: datetime) -> Point:
    return (
        Point("co2")
        .tag("sensor_id", sensor_id)
        .field("co2_ppm", round(random.uniform(400, 1200), 1))
        .time(instante)
    )


def simular_lectura_calidad_agua(sensor_id: str, instante: datetime) -> Point:
    return (
        Point("calidad_agua")
        .tag("sensor_id", sensor_id)
        .field("ph", round(random.uniform(6.5, 8.5), 1))
        .field("temperatura", round(random.uniform(10, 25), 1))
        .field("cloro", round(random.uniform(0.2, 1.5), 1))
        .time(instante)
    )

if __name__ == "__main__":
    ahora = datetime.now(timezone.utc)
    puntos = [
        simular_lectura_temp_hum(sensor, ahora - timedelta(minutes=i))
        for sensor in SENSORES_TEMP_HUM
        for i in range(60)  # última hora, una lectura por minuto
    ]
    puntos += [
        simular_lectura_co2(sensor, ahora - timedelta(minutes=i))
        for sensor in SENSORES_CO2
        for i in range(60)
    ]
    puntos += [
        simular_lectura_calidad_agua(sensor, ahora - timedelta(minutes=i))
        for sensor in SENSORES_CALIDAD_AGUA
        for i in range(60)
    ]
    cliente.write(record=puntos)  # escritura en lote
    print(f"Simulación completada: {len(puntos)} puntos.")