import pandas as pd
import os

# 📁 Función para cargar los CSVs
def load_data(folder='encuestas'):
    data = {}
    for file in os.listdir(folder):
        if file.endswith('.csv'):
            path = os.path.join(folder, file)
            df = pd.read_csv(path, encoding='utf-8')
            data[file.replace('.csv', '')] = df
    return data

# 📌 Diccionarios de conversión a valores numéricos
importance_map = {"Nada importante": 0, "Poco importante": 1, "Importante": 2, "Muy importante": 3, "Extremadamente importante": 4}
difficulty_map = {"Fácil de deducir": 1, "Moderadamente deducible": 2, "Difícil de deducir": 3}
applicable_map = {"Iniciales": 1, "Ambos": 1.5, "Avanzados": 2}

# 📌 Cargar los datos desde la carpeta 'encuestas'
data = load_data('encuestas')

# 📌 Crear DataFrame consolidado
all_data = pd.concat(data.values(), ignore_index=True)

# 📌 Filtrar solo filas con consejos (eliminar secciones)
all_data = all_data[all_data['#'].astype(str).str.isdigit()].copy()

# 📌 Convertir categorías a valores numéricos
all_data['Importancia Valor'] = all_data['Importancia'].map(importance_map)
all_data['Dificultad Valor'] = all_data['Dificultad de Deducción'].map(difficulty_map)
all_data['Aplicable Valor'] = all_data['Aplicable a'].map(applicable_map)

# 📌 Contar votos por categoría
importance_counts = all_data.groupby(['#', 'Importancia']).size().unstack(fill_value=0)
difficulty_counts = all_data.groupby(['#', 'Dificultad de Deducción']).size().unstack(fill_value=0)
applicable_counts = all_data.groupby(['#', 'Aplicable a']).size().unstack(fill_value=0)

# 📌 Calcular promedios por consejo
all_data['Promedio Importancia'] = all_data.groupby('#')['Importancia Valor'].transform('mean')
all_data['Promedio Dificultad'] = all_data.groupby('#')['Dificultad Valor'].transform('mean')
all_data['Promedio Aplicable'] = all_data.groupby('#')['Aplicable Valor'].transform('mean')

# 📌 Unir conteos a la data principal
all_data = all_data.drop_duplicates(subset=['#']).set_index('#')
all_data = all_data.join(importance_counts, rsuffix='_imp').join(difficulty_counts, rsuffix='_diff').join(applicable_counts, rsuffix='_app')

# 📌 Eliminar las columnas originales
cols_to_drop = ["Aplicable a", "Importancia", "Dificultad de Deducción", "Comentarios"]
all_data = all_data.drop(columns=cols_to_drop, errors='ignore')

# 📌 Guardar el DataFrame procesado en un archivo CSV (opcional)
all_data.to_csv("datos_procesados.csv", encoding="utf-8")

# ✅ El DataFrame "all_data" ahora contiene:
# - El conteo de votos por categoría
# - Los valores numéricos de Importancia, Dificultad y Aplicabilidad
# - Los promedios calculados para cada consejo
