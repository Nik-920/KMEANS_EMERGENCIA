import pandas as pd
from matplotlib.figure import Figure
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def main():
    # 1) Cargar datos
    path = r"C:\db\Nik Denilson\Universidad\IntiligenciaArtificial\ProyectoCasani\templates\Data\EtlData.xlsx"
    df = pd.read_csv(path, sep=";", encoding="latin1")
    
    # 2) Preprocesar FECHA_LLAMADA y extraer día de la semana
    df['FECHA_LLAMADA'] = pd.to_datetime(df['FECHA_LLAMADA'], format='%Y%m%d', errors='coerce')
    df['DIA_SEMANA_NUM'] = df['FECHA_LLAMADA'].dt.dayofweek  # 0=Lunes, 6=Domingo
    
    # 3) Convertir HORAINICIO_LLAMADA a segundos desde medianoche
    df['HORAINICIO_LLAMADA'] = pd.to_datetime(
        df['HORAINICIO_LLAMADA'], format='%H%M%S', errors='coerce'
    )
    
    df['SEGUNDOS'] = (
        df['HORAINICIO_LLAMADA'].dt.hour * 3600 +
        df['HORAINICIO_LLAMADA'].dt.minute * 60 +
        df['HORAINICIO_LLAMADA'].dt.second
    )
    
    # 4) Codificar DIANOMBRE (variable categórica)
    # Mapeo manual de días a números
    dia_map = {
        'LUNES': 0, 'MARTES': 1, 'MIERCOLES': 2, 
        'JUEVES': 3, 'VIERNES': 4, 'SABADO': 5, 'DOMINGO': 6
    }
    df['DIA_NUM'] = df['DIANOMBRE'].str.upper().map(dia_map)
    
    # 5) Codificar TURNO (variable categórica)
    turno_map = {
        'AMANECIDA': 0,  # 00:00 - 07:59
        'MAÑANA': 1,     # 08:00 - 13:59
        'TARDE': 2,      # 14:00 - 19:59
        'NOCHE': 3       # 20:00 - 23:59
    }
    df['TURNO_NUM'] = df['TURNO'].str.upper().map(turno_map)
    
    # 6) Eliminar nulos
    df = df.dropna(subset=['SEGUNDOS', 'DIA_NUM', 'TURNO_NUM'])
    
    # 7) Preparar matriz para K-means
    X = df[['SEGUNDOS', 'DIA_NUM', 'TURNO_NUM']].values
    X_scaled = StandardScaler().fit_transform(X)
    
    # 8) Ejecutar K-means con 4 clusters (turnos optimizados)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['CLUSTER'] = kmeans.fit_predict(X_scaled)
    
    # 9) Análisis de resultados por cluster
    print("\n=== ANÁLISIS DE TURNOS POR CLUSTER ===\n")
    for cluster_id in sorted(df['CLUSTER'].unique()):
        cluster_data = df[df['CLUSTER'] == cluster_id]
        
        print(f"--- CLUSTER {cluster_id} ---")
        print(f"Total llamadas: {len(cluster_data)}")
        print(f"Hora promedio: {cluster_data['SEGUNDOS'].mean() / 3600:.2f}h")
        print(f"Días más frecuentes: {cluster_data['DIANOMBRE'].mode().values}")
        print(f"Turnos más frecuentes: {cluster_data['TURNO'].mode().values}")
        print(f"Tipos de caso principales:")
        print(cluster_data['TIPOCASO'].value_counts().head(3))
        print()
    
    # 10) Preparar figura de visualización
    fig = Figure(figsize=(12, 8))
    ax = fig.subplots()
    
    # Convertir segundos a horas para mejor visualización
    horas = df['SEGUNDOS'] / 3600
    
    scatter = ax.scatter(
        horas, 
        df['DIA_NUM'], 
        c=df['CLUSTER'], 
        cmap='viridis', 
        alpha=0.6,
        s=50
    )
    
    # Etiquetas y estilo
    ax.set_xlabel('Hora del día (0 – 23)', fontsize=12)
    ax.set_ylabel('Día de la semana', fontsize=12)
    ax.set_title('Clustering Temporal K-means - Llamadas de Emergencia Ventanilla', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(range(0, 24))
    ax.set_yticks(range(0, 7))
    ax.set_yticklabels(['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'])
    ax.grid(True, alpha=0.3)
    
    # Barra de color
    fig.colorbar(scatter, ax=ax, label='Cluster ID')
    
    # 11) Guardar resultados
    df.to_csv('resultados_clustering_temporal.csv', index=False, sep=';')
    
    return fig, df

if __name__ == '__main__':
    fig, df_resultados = main()
    # Si usas matplotlib backend, puedes hacer fig.savefig()
