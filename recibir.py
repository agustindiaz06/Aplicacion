import serial
import sqlite3
import matplotlib.pyplot as plt
import time

# Configuración del puerto serie
SERIAL_PORT = "/dev/ttyACM0"  # Cambiar según el puerto de tu Arduino
BAUD_RATE = 9600

# Conectar al puerto serie
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Conectado al puerto {SERIAL_PORT}")
except Exception as e:
    print(f"Error conectando al puerto serie: {e}")
    exit()

# Configuración de la base de datos SQLite
DB_NAME = "sensores.db"
TABLE_NAME = "mediciones"

# Crear la base de datos y la tabla si no existen
def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id_medicion INTEGER PRIMARY KEY AUTOINCREMENT,
            valor_sensor INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Insertar una medición en la base de datos
def insert_data(valor):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO {TABLE_NAME} (valor_sensor) VALUES (?)
    """, (valor,))
    conn.commit()
    conn.close()

# Leer datos del puerto serie y almacenarlos
def read_serial_and_store():
    while True:
        try:
            # Leer una línea del puerto serie
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(f"Datos recibidos: {line}")
                valor = float(line.split()[1])
                insert_data(valor)
        except ValueError:
            print(f"Error al convertir el valor: {line}")
        except KeyboardInterrupt:
            print("Saliendo...")
            break

# Graficar los datos de la base de datos
def plot_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"SELECT timestamp, valor_sensor FROM {TABLE_NAME}")
    data = cursor.fetchall()
    conn.close()

    if data:
        timestamps, valores = zip(*data)
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, valores, marker='o', label='Sensor')
        plt.title('Serie temporal de valores del sensor')
        plt.xlabel('Timestamp')
        plt.ylabel('Valor del Sensor')
        plt.xticks(rotation=45)
        plt.grid()
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        print("No hay datos para graficar.")

# Configurar la base de datos
setup_database()

# Leer datos y almacenarlos
print("Iniciando lectura del puerto serie. Presiona Ctrl+C para detener.")
read_serial_and_store()

# Graficar los datos
plot_data()
