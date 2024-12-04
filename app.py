from flask import Flask, request
import sqlite3

app = Flask(__name__)

DB_NAME = "sensores_wifi.db"

# Crear base de datos si no existe
def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mediciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            humedad REAL,
            temperatura REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

setup_database()

@app.route('/endpoint', methods=['POST'])
def recibir_datos():
    try:
        humedad = request.form['humedad']
        temperatura = request.form['temperatura']
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO mediciones (humedad, temperatura) VALUES (?, ?)", (humedad, temperatura))
        conn.commit()
        conn.close()
        return "Datos almacenados correctamente.", 200
    except Exception as e:
        return str(e), 400

if __name__ == "__main__":
    setup_database()
    app.run(host='0.0.0.0', port=5000)




    
    