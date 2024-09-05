import mysql.connector
import matplotlib.pyplot as plt
from datetime import datetime

# Koneksi ke database MySQL
connection = mysql.connector.connect(
   host='127.0.0.1',
        user='root',
        password='',
        database='pm5350'
)

cursor = connection.cursor()

# Query untuk mengambil data dari tabel pm
query = """
SELECT time, value 
FROM pm 
WHERE id = 1
"""

cursor.execute(query)
results = cursor.fetchall()

# Memisahkan data menjadi dua daftar: waktu dan nilai
times = []
values = []

for row in results:
    # Mengambil waktu dan memformatnya untuk hanya menampilkan bulan, tanggal, jam, dan menit
    time = row[0]
    formatted_time = time.strftime('%m-%d %H:%M %S')
    times.append(formatted_time)
    values.append(row[1])

# Menutup koneksi ke database
cursor.close()
connection.close()

# Membuat plot
plt.figure(figsize=(10, 5))
plt.plot(times, values, marker='o', linestyle='-')
plt.xlabel('Time (MM-DD HH:MM SS)')
plt.ylabel('Value')
plt.title('Trend of Values over Time for ID 1')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Menampilkan plot
plt.show()