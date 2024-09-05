import mysql.connector
import matplotlib.pyplot as plt

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
query = "SELECT time, pm_code, value FROM pm"

# Eksekusi query
cursor.execute(query)

# Ambil semua hasil
results = cursor.fetchall()

# Tutup cursor dan koneksi
cursor.close()
conn.close()

# Pisahkan data yang diambil menjadi list masing-masing kolom
times = [row[0] for row in results]
pm_code = [row[1] for row in results]
values = [row[2] for row in results]

# Membuat grafik
plt.figure(figsize=(10, 6))

# Jika Anda ingin membuat plot untuk setiap pm_code secara terpisah
unique_pm_code = set(pm_code)
for code in unique_pm_code:
    code_times = [times[i] for i in range(len(times)) if pm_code[i] == code]
    code_values = [values[i] for i in range(len(values)) if pm_code[i] == code]
    plt.plot(code_times, code_values, label=f'PM Code {code}')

plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Graph of PM Values Over Time')
plt.legend()
plt.xticks(rotation=45)  # Rotate x-axis labels if needed
plt.tight_layout()  # Adjust layout to prevent clipping of labels

# Menampilkan grafik
plt.show()

