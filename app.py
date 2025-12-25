from flask import Flask, jsonify, request, render_template
import mysql.connector
import os
import time # Impor untuk fungsi load-cpu

app = Flask(__name__)

# agar bisa diakses dari JavaScript
from flask_cors import CORS
CORS(app)

# -------------------------------
# Koneksi ke MySQL
# -------------------------------
def db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "example"),
        database=os.getenv("MYSQL_DB", "gudang")
    )

# -------------------------------
# Inisialisasi Database
# -------------------------------
def init_db():
    connection = db()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS barang (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama VARCHAR(255),
            stok INT,
            harga DECIMAL(10,2)
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()

# Panggil init_db saat start
init_db()

# -------------------------------
# PENGUJIAN CGROUPS (Tambahan)
# -------------------------------
def cpu_heavy_task(duration=5):
    """Menjalankan tugas intensif CPU selama durasi tertentu (detik)."""
    start_time = time.time()
    count = 0
    while (time.time() - start_time) < duration:
        count += 1
    return count

@app.route("/load-cpu")
def load_cpu():
    """Endpoint yang memicu tugas intensif CPU untuk pengujian cgroups."""
    start = time.time()
    result = cpu_heavy_task(duration=5) # Beban selama 5 detik
    end = time.time()
    
    response = {
        "status": "CPU Load Test Complete",
        "message": f"Time taken to run heavy loop: {end - start:.2f} seconds"
    }
    return jsonify(response)


# -------------------------------
# FRONTEND (LOAD HTML)
# -------------------------------
@app.route("/")
def index():
    return render_template("index.html")

# -------------------------------
# API CRUD BARANG (Tetap)
# -------------------------------

# Get All
@app.route("/api/barang", methods=["GET"])
def get_barang():
    connection = db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM barang")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(rows)

# Add
@app.route("/api/barang", methods=["POST"])
def add_barang():
    data = request.json
    connection = db()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO barang (nama, stok, harga) VALUES (%s, %s, %s)",
        (data["nama"], data["stok"], data["harga"])
    )
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Barang ditambahkan"})

# Update
@app.route("/api/barang/<int:id>", methods=["PUT"])
def update_barang(id):
    data = request.json
    connection = db()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE barang SET nama=%s, stok=%s, harga=%s WHERE id=%s",
        (data["nama"], data["stok"], data["harga"], id)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Barang diperbarui"})

# Delete
@app.route("/api/barang/<int:id>", methods=["DELETE"])
def delete_barang(id):
    connection = db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM barang WHERE id=%s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Barang dihapus"})

# -------------------------------
# Run Flask
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)