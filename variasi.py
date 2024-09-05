from flask import Flask, request, render_template_string
import mysql.connector
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    plot_url = None
    if request.method == 'POST':
        selected_id = request.form['parameter']
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        # Mapping of text input to ID
        id_mapping = {
            'volt': 1,
            'current': 2,
            'power': 3,
            'freq': 4,
            'pf': 5,
            'all': 'all'
        }
        
        reverse_id_mapping = {v: k for k, v in id_mapping.items()}
        
        selected_id = id_mapping[selected_id]

        # Koneksi ke database MySQL
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='pm5350'
        )

        cursor = connection.cursor()

        if selected_id == 'all':
            query = f"""
            SELECT id, time, value FROM pm 
            WHERE time BETWEEN '{start_time}' AND '{end_time}'
            """
        else:
            query = f"""
            SELECT time, value FROM pm 
            WHERE id = {selected_id} AND time BETWEEN '{start_time}' AND '{end_time}'
            """

        cursor.execute(query)
        results = cursor.fetchall()

        # Memisahkan data menjadi daftar: waktu dan nilai
        times = {}
        values = {}
        if selected_id == 'all':
            for row in results:
                id, time, value = row
                if id not in times:
                    times[id] = []
                    values[id] = []
                times[id].append(time)
                values[id].append(value)
        else:
            times[selected_id] = [row[0] for row in results]
            values[selected_id] = [row[1] for row in results]

        # Menutup koneksi ke database
        cursor.close()
        connection.close()

        # Membuat plot
        plt.figure(figsize=(10, 5))
        if selected_id == 'all':
            for id, time_list in times.items():
                label = reverse_id_mapping[id].capitalize()
                plt.plot(time_list, values[id], marker='o', linestyle='-', label=label)
        else:
            label = reverse_id_mapping[selected_id].capitalize()
            plt.plot(times[selected_id], values[selected_id], marker='o', linestyle='-', label=label)
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title(f'Trend of Values over Time for {request.form["parameter"].capitalize()}')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save plot to a PNG in memory
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        plt.close()

    return render_template_string('''
        <!doctype html>
        <title> PT INDOCEMENT Select Parameter and Time Range</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
        <div class="container">
            <h1 class="text-center">PT INDOCEMENT TUNGGAL
PRAKARSA Tbk. Plant Cirebon </h1>
            <h2 class="text-center">Select a Parameter and Time Range</h2>
            <form method="post" class="form-horizontal">
                <div class="form-group">
                    <label for="parameter" class="col-sm-2 control-label">Parameter:</label>
                    <div class="col-sm-10">
                        <select id="parameter" name="parameter" required class="form-control">
                            <option value="volt">Volt</option>
                            <option value="current">Current</option>
                            <option value="power">Power</option>
                            <option value="freq">Frequency</option>
                            <option value="pf">Power Factor</option>
                            <option value="all">All</option>
                        </select>
                    </div>
                </div>
                <div class="form-group">
                    <label for="start_time" class="col-sm-2 control-label">Start Time:</label>
                    <div class="col-sm-10">
                        <input type="datetime-local" id="start_time" name="start_time" required class="form-control">
                    </div>
                </div>
                <div class="form-group">
                    <label for="end_time" class="col-sm-2 control-label">End Time:</label>
                    <div class="col-sm-10">
                        <input type="datetime-local" id="end_time" name="end_time" required class="form-control">
                    </div>
                </div>
                <div class="form-group">
                    <div class="col-sm-offset-2 col-sm-10">
                        <input type="submit" value="Submit" class="btn btn-primary">
                    </div>
                </div>
            </form>
            {% if plot_url %}
                <h2>Plot:</h2>
                <img src="data:image/png;base64,{{ plot_url }}">
            {% endif %}
        </div>
    ''', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
