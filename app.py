from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Ruta para acceder a los gráficos
@app.route('/graficos/<filename>')
def graficos(filename):
    return send_from_directory('graficos', filename)

# Página principal
@app.route('/')
def index():
    nombres_graficos = [
        'grafico1_modelo_tiempo.png',
        'grafico2_modelo_eventos.png',
        'grafico3_operario_eventos.png',
        'grafico4_operario_duracion.png',
        'grafico5_eventos_tipo.png',
        'grafico6_eventos_duracion.png'
    ]
    return render_template('index.html', graficos=nombres_graficos)

if __name__ == '__main__':
    app.run(debug=True)
