import mysql.connector

# Buat koneksi ke database MySQL
conn = mysql.connector.connect(
    host='127.0.0.1',    # Ganti dengan host database Anda
    user='root', # Ganti dengan username database Anda
    password='', # Ganti dengan password database Anda
    database='pm5350'     # Nama database Anda
)

# Membuat cursor untuk mengeksekusi query
cursor = conn.cursor()

# Query untuk mengambil data dari tabel pm
query = "SELECT time, pm_code, id, value FROM pm"

# Eksekusi query
cursor.execute(query)

# Ambil semua hasil
results = cursor.fetchall()

# Tampilkan hasil
for row in results:
    print(f"Time: {row[0]}, PM Code: {row[1]}, ID: {row[2]}, Value: {row[3]}")

# Tutup cursor dan koneksi
cursor.close()
conn.close()
