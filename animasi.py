import mysql.connector
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

# Fungsi untuk mengambil data dari database
def get_data():
    conn = mysql.connector.connect( 
        host='127.0.0.1',
        user='root',
        password='',
        database='pm5350'
    )
    cursor = conn.cursor()
    query = "SELECT time, pm_code, value FROM pm"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# Fungsi untuk memperbarui grafik
def update(frame):
    # Ambil data dari database
    data = get_data()
    
    # Pisahkan data menjadi list masing-masing kolom
    times = [datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S') for row in data]
    pm_code = [row[1] for row in data]
    values = [row[2] for row in data]
    
    # Bersihkan plot
    ax.clear()
    
    # Buat plot baru
    unique_pm_code = set(pm_code)
    for code in unique_pm_code:
        code_times = [times[i] for i in range(len(times)) if pm_code[i] == code]
        code_values = [values[i] for i in range(len(values)) if pm_code[i] == code]
        ax.plot(code_times, code_values, label=f'PM Code {code}')
    
    # Setel judul dan label
    ax.set_title('Graph of PM Values Over Time')
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

# Buat figure dan axis untuk plot
fig, ax = plt.subplots(figsize=(10, 6))

# Buat animasi
ani = animation.FuncAnimation(fig, update, interval=5000) # Update setiap 5 detik

# Tampilkan grafik
plt.show()
