import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import os

# Conexión a PostgreSQL
usuario = 'postgres'
contraseña = '1234'
host = 'localhost'
puerto = '5432'
basededatos = 'paletizado_db'

conexion = sqlalchemy.create_engine(f'postgresql+psycopg2://{usuario}:{contraseña}@{host}:{puerto}/{basededatos}')

# Cargar los datos
df_sql = pd.read_sql('SELECT * FROM palletizer_info', conexion)
df_csv = pd.read_csv('eventos_paletizador.csv')

df_csv['machine_id'] = df_csv['machine_id'].astype(str)
df_sql['machine_id'] = df_sql['machine_id'].astype(str)

df_combinado = pd.merge(df_csv, df_sql, on='machine_id', how='left')
df_combinado_filtrado = df_combinado.dropna(subset=['model'])

# Crear carpeta si no existe
if not os.path.exists('graficos'):
    os.makedirs('graficos')

colores = plt.cm.tab10.colors
logo_path = 'logo_utpl.png'


# Función para insertar el logo UTPL
def agregar_logo(fig, ax):
    if os.path.exists(logo_path):
        logo = mpimg.imread(logo_path)
        axins = inset_axes(ax, width="10%", height="10%", loc='upper left')
        axins.imshow(logo)
        axins.axis('off')


# Función para generar y guardar gráficos
def generar_grafico(datos, titulo, ylabel, xlabel, nombre_archivo):
    fig, ax = plt.subplots(figsize=(8, 4))
    barras = datos.plot(kind='bar', ax=ax, color=colores)

    for i, barra in enumerate(barras.patches):
        altura = barra.get_height()
        etiqueta = datos.index[i]
        ax.text(barra.get_x() + barra.get_width() / 2, altura / 2, str(etiqueta),
                ha='center', va='center', fontsize=6, rotation=90, color='white')

    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.tick_params(axis='x', labelbottom=False)

    agregar_logo(fig, ax)
    plt.tight_layout()

    # Guardar en carpeta graficos/
    ruta = os.path.join('graficos', nombre_archivo)
    plt.savefig(ruta, bbox_inches='tight')
    plt.close()


# Generar y guardar cada gráfico
generar_grafico(df_combinado_filtrado.groupby('model')['tiempo_segundos'].mean(),
                'Tiempo Promedio de Eventos por Modelo de Máquina', 'Tiempo (segundos)',
                'Modelo de Máquina', 'grafico1_modelo_tiempo.png')

generar_grafico(df_combinado_filtrado['model'].value_counts(),
                'Cantidad de Eventos por Modelo de Máquina', 'Número de Eventos',
                'Modelo de Máquina', 'grafico2_modelo_eventos.png')

generar_grafico(df_combinado_filtrado['operario'].value_counts(),
                'Eventos Registrados por Operario', 'Cantidad de Eventos',
                'Operario', 'grafico3_operario_eventos.png')

generar_grafico(df_combinado_filtrado.groupby('operario')['tiempo_segundos'].mean(),
                'Duración Promedio de Eventos por Operario', 'Tiempo Promedio (segundos)',
                'Operario', 'grafico4_operario_duracion.png')

generar_grafico(df_combinado_filtrado['evento'].value_counts(),
                'Eventos por Tipo de Evento', 'Cantidad',
                'Tipo de Evento', 'grafico5_eventos_tipo.png')

generar_grafico(df_combinado_filtrado.groupby('evento')['tiempo_segundos'].mean(),
                'Duración Promedio por Tipo de Evento', 'Tiempo Promedio (segundos)',
                'Tipo de Evento', 'grafico6_eventos_duracion.png')

# Exportar dataset final
df_combinado_filtrado.to_csv('dataset_final.csv', index=False)
