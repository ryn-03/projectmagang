        import mysql.connector
        import matplotlib.pyplot as plt

        # Fungsi untuk mendapatkan ID dari pengguna
        def get_id_from_user():
        while True:
                try:
                selected_id = int(input("Select an ID (1-5): "))
                if 1 <= selected_id <= 5:
                        return selected_id
                else:
                        print("Please select a valid ID between 1 and 5.")
                except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")

        # Mendapatkan ID dari pengguna
        selected_id = get_id_from_user()

        # Koneksi ke database MySQL
        connection = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='pm5350'
        )

        cursor = connection.cursor()

        # Query untuk mengambil data dari tabel pm
        query = f"""
        SELECT time, value FROM pm WHERE id = {selected_id}
        """

        cursor.execute(query)
        results = cursor.fetchall()

        # Memisahkan data menjadi dua daftar: waktu dan nilai
        times = [row[0] for row in results]
        values = [row[1] for row in results]

        # Menutup koneksi ke database
        cursor.close()
        connection.close()

        # Membuat plot
        plt.figure(figsize=(10, 5))
        plt.plot(times, values, marker='o', linestyle='-')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title(f'Trend of Values over Time for ID {selected_id}')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Menampilkan plot
        plt.show()
