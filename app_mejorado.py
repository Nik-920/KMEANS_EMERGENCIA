from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Configuración global
DATASET_PATH = r"C:\db\Nik Denilson\Universidad\IntiligenciaArtificial\ProyectoCasani\templates\Data\EtlData.xlsx"


# ============================================================
# FUNCIONES AUXILIARES MEJORADAS
# ============================================================

def convertir_a_coordenadas_ciclicas(df):
    """
    Convierte variables temporales a coordenadas cíclicas.
    Esto respeta que 23:59 y 00:01 están cerca.
    """
    # Convertir FECHA_LLAMADA
    if df['FECHA_LLAMADA'].dtype == 'object':
        df['FECHA_LLAMADA'] = pd.to_datetime(df['FECHA_LLAMADA'], format='%Y%m%d', errors='coerce')
    elif not pd.api.types.is_datetime64_any_dtype(df['FECHA_LLAMADA']):
        df['FECHA_LLAMADA'] = pd.to_datetime(df['FECHA_LLAMADA'], errors='coerce')

    # Procesar HORAINICIO_LLAMADA
    df['HORAINICIO_TEMP'] = pd.to_datetime(
        '2022-01-01 ' + df['HORAINICIO_LLAMADA'].astype(str),
        format='%Y-%m-%d %H:%M:%S',
        errors='coerce'
    )

    df['SEGUNDOS'] = (
        df['HORAINICIO_TEMP'].dt.hour * 3600 +
        df['HORAINICIO_TEMP'].dt.minute * 60 +
        df['HORAINICIO_TEMP'].dt.second
    )

    # ✅ MEJORA 1: Coordenadas cíclicas para HORA
    df['HORA_SIN'] = np.sin(2 * np.pi * df['SEGUNDOS'] / 86400)
    df['HORA_COS'] = np.cos(2 * np.pi * df['SEGUNDOS'] / 86400)

    # ✅ MEJORA 2: Coordenadas cíclicas para DÍA DE LA SEMANA
    dia_map = {
        'LUNES': 0, 'MARTES': 1, 'MIERCOLES': 2, 'MIÉRCOLES': 2,
        'JUEVES': 3, 'VIERNES': 4, 'SABADO': 5, 'SÁBADO': 5, 'DOMINGO': 6
    }
    df['DIA_NUM'] = df['DIANOMBRE'].str.upper().str.strip().map(dia_map)
    df['DIA_SIN'] = np.sin(2 * np.pi * df['DIA_NUM'] / 7)
    df['DIA_COS'] = np.cos(2 * np.pi * df['DIA_NUM'] / 7)

    # ✅ MEJORA 3: One-hot encoding para TURNO (categórico, no ordinal)
    turno_dummies = pd.get_dummies(df['TURNO'], prefix='TURNO', drop_first=True)
    df = pd.concat([df, turno_dummies], axis=1)

    print(f"✓ Variables cíclicas creadas correctamente")
    print(f"  - HORA_SIN/COS: {df['HORA_SIN'].notna().sum()} registros")
    print(f"  - DIA_SIN/COS: {df['DIA_SIN'].notna().sum()} registros")
    print(f"  - Dummies de TURNO: {turno_dummies.shape[1]} columnas")

    return df


def determinar_clusters_optimos(X_scaled, max_clusters=10):
    """
    Determina automáticamente el número óptimo de clusters
    usando el método del codo y coeficiente de Silhouette.
    ⚡ OPTIMIZADO: Reduce iteraciones para datasets grandes
    """
    print("\n🔍 Determinando número óptimo de clusters...")

    # ⚡ OPTIMIZACIÓN: Para datasets grandes, reducir n_init
    n_samples = X_scaled.shape[0]
    if n_samples > 20000:
        n_init = 5  # Menos iteraciones
        print(f"  ⚡ Dataset grande: usando n_init={n_init} para velocidad")
    elif n_samples > 10000:
        n_init = 10
    else:
        n_init = 20

    inertias = []
    silhouette_scores = []
    davies_bouldin_scores = []

    K_range = range(2, max_clusters + 1)

    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=n_init, max_iter=200)
        labels = kmeans.fit_predict(X_scaled)

        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X_scaled, labels))
        davies_bouldin_scores.append(davies_bouldin_score(X_scaled, labels))

        print(f"  k={k}: Silhouette={silhouette_scores[-1]:.3f}, DB={davies_bouldin_scores[-1]:.3f}")

    # Encontrar el óptimo
    optimal_k = silhouette_scores.index(max(silhouette_scores)) + 2

    print(f"\n✓ Número óptimo de clusters: {optimal_k}")
    print(f"  - Silhouette Score: {max(silhouette_scores):.3f}")
    print(f"  - Davies-Bouldin: {davies_bouldin_scores[optimal_k-2]:.3f}")

    # Generar gráfico de evaluación
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))

    # Método del codo
    ax1.plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
    ax1.set_title('Método del Codo', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Número de Clusters (k)', fontsize=12)
    ax1.set_ylabel('Inercia (Within-Cluster Sum of Squares)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.axvline(optimal_k, color='red', linestyle='--', label=f'Óptimo: k={optimal_k}')
    ax1.legend()

    # Silhouette Score
    ax2.plot(K_range, silhouette_scores, 'go-', linewidth=2, markersize=8)
    ax2.set_title('Coeficiente de Silhouette', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Número de Clusters (k)', fontsize=12)
    ax2.set_ylabel('Silhouette Score (mayor es mejor)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.axvline(optimal_k, color='red', linestyle='--', label=f'Óptimo: k={optimal_k}')
    ax2.legend()

    # Davies-Bouldin Index
    ax3.plot(K_range, davies_bouldin_scores, 'ro-', linewidth=2, markersize=8)
    ax3.set_title('Davies-Bouldin Index', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Número de Clusters (k)', fontsize=12)
    ax3.set_ylabel('DB Index (menor es mejor)', fontsize=12)
    ax3.grid(True, alpha=0.3)
    ax3.axvline(optimal_k, color='red', linestyle='--', label=f'Óptimo: k={optimal_k}')
    ax3.legend()

    plt.tight_layout()

    # Guardar gráfico
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=120, bbox_inches='tight')
    buffer.seek(0)
    grafico_metricas = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return optimal_k, grafico_metricas


def validar_clusters(X_scaled, labels):
    """
    Valida la calidad del clustering con múltiples métricas
    """
    silhouette = silhouette_score(X_scaled, labels)
    davies_bouldin = davies_bouldin_score(X_scaled, labels)
    calinski_harabasz = calinski_harabasz_score(X_scaled, labels)

    print("\n📊 MÉTRICAS DE VALIDACIÓN:")
    print(f"  ✓ Silhouette Score: {silhouette:.4f} (rango: -1 a 1, óptimo: cercano a 1)")
    print(f"  ✓ Davies-Bouldin Index: {davies_bouldin:.4f} (menor es mejor)")
    print(f"  ✓ Calinski-Harabasz Score: {calinski_harabasz:.2f} (mayor es mejor)")

    # Interpretación
    if silhouette > 0.5:
        calidad = "EXCELENTE ✅"
    elif silhouette > 0.3:
        calidad = "BUENA ✓"
    elif silhouette > 0.2:
        calidad = "ACEPTABLE ⚠️"
    else:
        calidad = "POBRE ❌"

    print(f"\n  🎯 Calidad del clustering: {calidad}")

    return {
        'silhouette': silhouette,
        'davies_bouldin': davies_bouldin,
        'calinski_harabasz': calinski_harabasz,
        'calidad': calidad
    }


# ============================================================
# CLUSTERING TEMPORAL MEJORADO
# ============================================================

def cargar_y_procesar_datos_mejorado():
    """Carga y preprocesa el dataset con mejoras"""
    try:
        df = pd.read_excel(DATASET_PATH, engine='openpyxl')
        print(f"✓ Dataset cargado: {len(df)} registros")

        # Aplicar transformaciones cíclicas
        df = convertir_a_coordenadas_ciclicas(df)

        # Eliminar nulos
        turno_cols = [col for col in df.columns if col.startswith('TURNO_')]
        columnas_requeridas = ['HORA_SIN', 'HORA_COS', 'DIA_SIN', 'DIA_COS'] + turno_cols

        df_antes = len(df)
        df_clean = df.dropna(subset=columnas_requeridas).copy()

        print(f"\n📊 LIMPIEZA:")
        print(f"  - Original: {df_antes} registros")
        print(f"  - Eliminados: {df_antes - len(df_clean)}")
        print(f"  - Válidos: {len(df_clean)}")

        if len(df_clean) == 0:
            raise Exception("No hay datos válidos después de la limpieza")

        return df_clean

    except Exception as e:
        raise Exception(f"Error al cargar datos: {str(e)}")


def ejecutar_clustering_temporal_mejorado(df):
    """
    Ejecuta clustering temporal con todas las mejoras
    """
    print("\n🚀 INICIANDO CLUSTERING TEMPORAL MEJORADO...")

    # Seleccionar características
    turno_cols = [col for col in df.columns if col.startswith('TURNO_')]
    feature_cols = ['HORA_SIN', 'HORA_COS', 'DIA_SIN', 'DIA_COS'] + turno_cols

    X = df[feature_cols].values
    X_scaled = StandardScaler().fit_transform(X)

    # Determinar número óptimo de clusters
    n_clusters, grafico_metricas = determinar_clusters_optimos(X_scaled, max_clusters=8)

    # Ejecutar clustering con el óptimo
    print(f"\n🔄 Ejecutando K-means con k={n_clusters}...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=50, max_iter=500)
    df['CLUSTER'] = kmeans.fit_predict(X_scaled)

    # Validar calidad
    metricas = validar_clusters(X_scaled, df['CLUSTER'])

    print(f"✓ Clustering completado: {n_clusters} clusters identificados")

    return df, kmeans, metricas, grafico_metricas


# ============================================================
# CLUSTERING GEOGRÁFICO MEJORADO
# ============================================================

def ejecutar_clustering_geografico_mejorado(df):
    """
    ✅ MEJORA 6: Clustering geográfico con one-hot encoding y pesos
    ⚡ OPTIMIZADO: Usa KMeans para datasets grandes (>10k registros)
    """
    print("\n🗺️ CLUSTERING GEOGRÁFICO MEJORADO...")

    # One-hot encoding para variables categóricas
    zona_dummies = pd.get_dummies(df['ZONA'], prefix='ZONA')
    sector_dummies = pd.get_dummies(df['SECTOR'], prefix='SECTOR')
    subsector_dummies = pd.get_dummies(df['SUBSECTOR'], prefix='SUBSECTOR')
    tipo_dummies = pd.get_dummies(df['TIPOCASO'], prefix='TIPO')

    print(f"✓ Encoding aplicado:")
    print(f"  - ZONA: {zona_dummies.shape[1]} categorías")
    print(f"  - SECTOR: {sector_dummies.shape[1]} categorías")
    print(f"  - SUBSECTOR: {subsector_dummies.shape[1]} categorías")
    print(f"  - TIPOCASO: {tipo_dummies.shape[1]} categorías")

    # ✅ Aplicar pesos según importancia jerárquica
    df_encoded = pd.concat([
        zona_dummies * 3.0,      # Mayor peso
        sector_dummies * 2.0,    # Peso medio
        subsector_dummies * 1.0, # Menor peso
        tipo_dummies * 2.5       # Alto peso (crítico)
    ], axis=1)

    # Normalizar
    X_scaled = StandardScaler().fit_transform(df_encoded)

    print(f"✓ Dataset preparado: {X_scaled.shape[0]} registros x {X_scaled.shape[1]} features")

    # ⚡ OPTIMIZACIÓN: Usar KMeans para datasets grandes
    # AgglomerativeClustering tiene complejidad O(n³) - muy lento para >10k registros
    # KMeans tiene complejidad O(n*k*i) - mucho más rápido

    if len(df) > 10000:
        print(f"⚡ Dataset grande detectado ({len(df)} registros)")
        print(f"  → Usando K-means (más rápido que jerárquico)")
        use_kmeans = True
    else:
        print(f"✓ Dataset pequeño ({len(df)} registros)")
        print(f"  → Usando clustering jerárquico")
        use_kmeans = False

    # Determinar número óptimo (con max_clusters reducido para velocidad)
    n_clusters, grafico_metricas = determinar_clusters_optimos(X_scaled, max_clusters=8)

    # Ejecutar clustering
    if use_kmeans:
        print(f"\n🔄 Ejecutando K-means con k={n_clusters}...")
        clustering = KMeans(n_clusters=n_clusters, random_state=42, n_init=20, max_iter=300)
        df['CLUSTER_GEO'] = clustering.fit_predict(X_scaled)
    else:
        print(f"\n🔄 Ejecutando Clustering Jerárquico con k={n_clusters}...")
        clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
        df['CLUSTER_GEO'] = clustering.fit_predict(X_scaled)

    # Validar
    metricas = validar_clusters(X_scaled, df['CLUSTER_GEO'])

    print(f"✓ Clustering geográfico completado")

    return df, clustering, metricas, grafico_metricas


# ============================================================
# MODELO PREDICTIVO DE ASIGNACIÓN DE RECURSOS
# ============================================================

def preparar_datos_predictivos(df):
    """
    ✅ MEJORA 7: Preparar datos para modelo predictivo
    """
    print("\n🤖 PREPARANDO MODELO PREDICTIVO DE ASIGNACIÓN...")

    # Crear coordenadas cíclicas
    df = convertir_a_coordenadas_ciclicas(df)

    # Codificar variables geográficas
    zona_dummies = pd.get_dummies(df['ZONA'], prefix='ZONA', drop_first=True)
    sector_dummies = pd.get_dummies(df['SECTOR'], prefix='SECTOR', drop_first=True)

    # Features para el modelo
    feature_cols = ['HORA_SIN', 'HORA_COS', 'DIA_SIN', 'DIA_COS'] + \
                   list(zona_dummies.columns) + list(sector_dummies.columns)

    df_features = pd.concat([df[['HORA_SIN', 'HORA_COS', 'DIA_SIN', 'DIA_COS']],
                             zona_dummies, sector_dummies], axis=1)

    # Target: UNIDAD a asignar
    df_features['TARGET'] = df['UNIDAD']

    # Filtrar unidades con suficientes datos (mínimo 50 casos)
    unidad_counts = df['UNIDAD'].value_counts()
    unidades_validas = unidad_counts[unidad_counts >= 50].index

    df_features = df_features[df_features['TARGET'].isin(unidades_validas)]

    print(f"✓ Dataset predictivo preparado:")
    print(f"  - Registros: {len(df_features)}")
    print(f"  - Features: {len(feature_cols)}")
    print(f"  - Unidades objetivo: {len(unidades_validas)}")

    return df_features, feature_cols


def entrenar_modelo_asignacion(df):
    """
    ✅ MEJORA 8: Modelo predictivo con Random Forest
    """
    df_model, feature_cols = preparar_datos_predictivos(df)

    X = df_model[feature_cols]
    y = df_model['TARGET']

    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    print(f"\n🔄 Entrenando Random Forest...")
    print(f"  - Train: {len(X_train)} registros")
    print(f"  - Test: {len(X_test)} registros")

    # Random Forest
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=20,
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'  # Manejo de desbalance
    )

    rf.fit(X_train, y_train)

    # Evaluar
    train_score = rf.score(X_train, y_train)
    test_score = rf.score(X_test, y_test)

    # Cross-validation
    cv_scores = cross_val_score(rf, X, y, cv=5, n_jobs=-1)

    print(f"\n📊 RESULTADOS DEL MODELO:")
    print(f"  ✓ Accuracy Train: {train_score:.2%}")
    print(f"  ✓ Accuracy Test: {test_score:.2%}")
    print(f"  ✓ CV Score (mean): {cv_scores.mean():.2%} (±{cv_scores.std():.2%})")

    # Importancia de características
    importancias = pd.DataFrame({
        'feature': feature_cols,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False).head(10)

    print(f"\n📈 TOP 10 VARIABLES MÁS IMPORTANTES:")
    for idx, row in importancias.iterrows():
        print(f"  {row['feature']}: {row['importance']:.4f}")

    return rf, test_score, importancias


# ============================================================
# RUTAS FLASK MEJORADAS
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analisis')
def analisis():
    """
    ✅ Endpoint TEMPORAL con todas las mejoras implementadas
    """
    try:
        print("\n" + "="*60)
        print("🚀 ANÁLISIS CLUSTERING TEMPORAL MEJORADO - INICIANDO")
        print("="*60)

        # 1. Cargar datos
        df = cargar_y_procesar_datos_mejorado()

        # 2. Clustering temporal
        df, kmeans, metricas, grafico_metricas = ejecutar_clustering_temporal_mejorado(df)

        # 3. Generar visualización
        imagen_base64 = generar_grafico(df)

        # 4. Analizar clusters
        estadisticas = analizar_clusters(df)

        # 5. Guardar resultados
        output_path = 'static/resultados_clustering_temporal.csv'
        df.to_csv(output_path, index=False, sep=';', encoding='utf-8-sig')

        print(f"\n✅ ANÁLISIS TEMPORAL COMPLETADO")
        print("="*60)

        return render_template('analisis.html',
                             imagen=imagen_base64,
                             estadisticas=estadisticas,
                             total_registros=len(df),
                             n_clusters=len(df['CLUSTER'].unique()),
                             fecha_actual=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return render_template('error.html', error=str(e))


@app.route('/analisis-geografico')
def analisis_geografico():
    """
    ✅ Endpoint GEOGRÁFICO con mejoras implementadas
    """
    try:
        print("\n" + "="*60)
        print("🗺️ ANÁLISIS CLUSTERING GEOGRÁFICO MEJORADO - INICIANDO")
        print("="*60)

        # 1. Cargar datos
        df = pd.read_excel(DATASET_PATH, engine='openpyxl')
        print(f"✓ Dataset cargado: {len(df)} registros")

        # 2. Clustering geográfico mejorado
        df, clustering, metricas, grafico_metricas = ejecutar_clustering_geografico_mejorado(df)

        # 3. Generar visualización geográfica
        imagen_base64 = generar_grafico_geografico(df)

        # 4. Analizar clusters geográficos
        estadisticas = analizar_clusters_geografico(df)

        # 5. Guardar resultados
        output_path = 'static/resultados_clustering_geografico.csv'
        df.to_csv(output_path, index=False, sep=';', encoding='utf-8-sig')

        print(f"\n✅ ANÁLISIS GEOGRÁFICO COMPLETADO")
        print("="*60)

        return render_template('analisis_geografico.html',
                             imagen=imagen_base64,
                             estadisticas=estadisticas,
                             total_registros=len(df),
                             n_clusters=len(df['CLUSTER_GEO'].unique()),
                             fecha_actual=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return render_template('error.html', error=str(e))


@app.route('/analisis-recursos')
def analisis_recursos():
    """
    ✅ Endpoint RECURSOS con modelo predictivo
    """
    try:
        print("\n" + "="*60)
        print("🚗 ANÁLISIS DE RECURSOS CON MODELO PREDICTIVO - INICIANDO")
        print("="*60)

        # 1. Cargar datos
        df = pd.read_excel(DATASET_PATH, engine='openpyxl')
        print(f"✓ Dataset cargado: {len(df)} registros")

        # 2. Entrenar modelo predictivo
        modelo, accuracy, importancias = entrenar_modelo_asignacion(df)

        # 3. Preparar datos para clustering de recursos (para visualización)
        df_recursos = preparar_datos_recursos_clustering(df)

        # 4. Generar visualización
        imagen_base64 = generar_grafico_recursos(df_recursos)

        # 5. Analizar clusters de recursos
        estadisticas = analizar_clusters_recursos(df_recursos)

        # 6. Guardar resultados
        output_path = 'static/resultados_clustering_recursos.csv'
        df_recursos.to_csv(output_path, index=False, sep=';', encoding='utf-8-sig')

        print(f"\n✅ ANÁLISIS DE RECURSOS COMPLETADO")
        print("="*60)

        return render_template('analisis_recursos.html',
                             imagen=imagen_base64,
                             estadisticas=estadisticas,
                             total_registros=len(df_recursos),
                             n_clusters=len(df_recursos['CLUSTER_REC'].unique()),
                             modelo_accuracy=f"{accuracy:.2%}",
                             fecha_actual=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return render_template('error.html', error=str(e))


@app.route('/modelo-predictivo')
def modelo_predictivo():
    """
    Endpoint para modelo predictivo de asignación
    """
    try:
        print("\n🤖 ENTRENANDO MODELO PREDICTIVO...")

        df = pd.read_excel(DATASET_PATH, engine='openpyxl')
        modelo, accuracy, importancias = entrenar_modelo_asignacion(df)

        return jsonify({
            'success': True,
            'accuracy': f"{accuracy:.2%}",
            'top_features': importancias.to_dict('records'),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================
# FUNCIONES AUXILIARES EXISTENTES (reutilizar del código original)
# ============================================================

def generar_grafico(df):
    """Reutilizar función existente"""
    import numpy as np

    fig, ax = plt.subplots(figsize=(16, 10))

    horas = df['SEGUNDOS'] / 3600
    np.random.seed(42)
    dia_con_jitter = df['DIA_NUM'] + np.random.uniform(-0.35, 0.35, size=len(df))

    scatter = ax.scatter(
        horas, dia_con_jitter, c=df['CLUSTER'],
        cmap='viridis', alpha=0.5, s=50,
        edgecolors='white', linewidth=0.3
    )

    ax.set_xlabel('Hora del día (0 – 23)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Día de la semana', fontsize=14, fontweight='bold')
    ax.set_title('Clustering Temporal MEJORADO - K-means con validación',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(range(0, 24))
    ax.set_yticks(range(0, 7))
    ax.set_yticklabels(['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])
    ax.set_ylim(-0.5, 6.5)
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.8)
    ax.set_facecolor('#f8f9fa')

    cbar = plt.colorbar(scatter, ax=ax, label='Cluster ID')

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return image_base64


def analizar_clusters(df):
    """Analiza clusters temporales"""
    resultados = []

    for cluster_id in sorted(df['CLUSTER'].unique()):
        cluster_data = df[df['CLUSTER'] == cluster_id]

        hora_promedio = cluster_data['SEGUNDOS'].mean() / 3600
        total_llamadas = len(cluster_data)

        top_casos = cluster_data['TIPOCASO'].value_counts().head(3).to_dict()

        dia_frecuente = cluster_data['DIANOMBRE'].mode().values[0] if len(
            cluster_data['DIANOMBRE'].mode()) > 0 else 'N/A'

        turno_frecuente = cluster_data['TURNO'].mode().values[0] if len(
            cluster_data['TURNO'].mode()) > 0 else 'N/A'

        resultados.append({
            'cluster_id': int(cluster_id),
            'total_llamadas': int(total_llamadas),
            'hora_promedio': f"{hora_promedio:.2f}h",
            'dia_frecuente': dia_frecuente,
            'turno_frecuente': turno_frecuente,
            'top_casos': top_casos
        })

    return resultados


def generar_grafico_geografico(df):
    """Genera gráfico de dispersión para clustering geográfico"""
    import numpy as np

    fig, ax = plt.subplots(figsize=(18, 10))

    # Mapear zonas y subsectores a números
    zona_map = {zona: i for i, zona in enumerate(sorted(df['ZONA'].dropna().unique()))}
    subsector_map = {sub: i for i, sub in enumerate(sorted(df['SUBSECTOR'].dropna().unique()))}

    df['ZONA_NUM'] = df['ZONA'].map(zona_map)
    df['SUBSECTOR_NUM'] = df['SUBSECTOR'].map(subsector_map)

    # Agregar jitter
    np.random.seed(42)
    zona_con_jitter = df['ZONA_NUM'] + np.random.uniform(-0.35, 0.35, size=len(df))
    subsector_con_jitter = df['SUBSECTOR_NUM'] + np.random.uniform(-0.35, 0.35, size=len(df))

    scatter = ax.scatter(
        zona_con_jitter, subsector_con_jitter,
        c=df['CLUSTER_GEO'], cmap='viridis',
        alpha=0.4, s=50, edgecolors='white', linewidth=0.3
    )

    ax.set_xlabel('Zona Geográfica', fontsize=14, fontweight='bold')
    ax.set_ylabel('Subsector', fontsize=14, fontweight='bold')
    ax.set_title('Clustering Geográfico MEJORADO - Agglomerative Clustering',
                 fontsize=16, fontweight='bold', pad=20)

    # Etiquetas
    zonas_unicas = sorted(df['ZONA'].dropna().unique())
    subsectores_unicos = sorted(df['SUBSECTOR'].dropna().unique())

    ax.set_xticks(range(len(zonas_unicas)))
    ax.set_xticklabels(zonas_unicas, rotation=45, ha='right', fontsize=10)
    ax.set_yticks(range(len(subsectores_unicos)))
    ax.set_yticklabels(subsectores_unicos, fontsize=9)

    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.8)
    ax.set_facecolor('#f8f9fa')

    cbar = plt.colorbar(scatter, ax=ax, label='Cluster Geográfico', pad=0.02)

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return image_base64


def analizar_clusters_geografico(df):
    """Genera estadísticas por cluster geográfico"""
    resultados = []

    for cluster_id in sorted(df['CLUSTER_GEO'].unique()):
        cluster_data = df[df['CLUSTER_GEO'] == cluster_id]

        total_llamadas = len(cluster_data)

        zona_frecuente = cluster_data['ZONA'].mode().values[0] if len(
            cluster_data['ZONA'].mode()) > 0 else 'N/A'
        sector_frecuente = cluster_data['SECTOR'].mode().values[0] if len(
            cluster_data['SECTOR'].mode()) > 0 else 'N/A'
        subsector_frecuente = cluster_data['SUBSECTOR'].mode().values[0] if len(
            cluster_data['SUBSECTOR'].mode()) > 0 else 'N/A'

        top_casos = cluster_data['TIPOCASO'].value_counts().head(3).to_dict()

        zonas_unicas = cluster_data['ZONA'].nunique()
        densidad = total_llamadas / zonas_unicas if zonas_unicas > 0 else 0

        resultados.append({
            'cluster_id': int(cluster_id),
            'total_llamadas': int(total_llamadas),
            'zona_frecuente': zona_frecuente,
            'sector_frecuente': sector_frecuente,
            'subsector_frecuente': subsector_frecuente,
            'densidad': f"{densidad:.1f}",
            'top_casos': top_casos
        })

    return resultados


def preparar_datos_recursos_clustering(df):
    """Prepara datos para clustering de recursos"""
    # Codificar variables
    unidad_map = {u: i for i, u in enumerate(sorted(df['UNIDAD'].dropna().unique()))}
    tipo_map = {t: i for i, t in enumerate(sorted(df['TIPOCASO'].dropna().unique()))}
    turno_map = {'AMANECIDA': 0, 'MAÑANA': 1, 'MANANA': 1, 'TARDE': 2, 'NOCHE': 3}

    df['UNIDAD_NUM'] = df['UNIDAD'].map(unidad_map)
    df['TIPOCASO_NUM'] = df['TIPOCASO'].map(tipo_map)
    df['TURNO_NUM'] = df['TURNO'].str.upper().str.strip().map(turno_map)

    df_clean = df.dropna(subset=['UNIDAD_NUM', 'TIPOCASO_NUM', 'TURNO_NUM']).copy()

    # Clustering
    X = df_clean[['UNIDAD_NUM', 'TIPOCASO_NUM', 'TURNO_NUM']].values
    X_scaled = StandardScaler().fit_transform(X)

    n_clusters = 6
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=20)
    df_clean['CLUSTER_REC'] = kmeans.fit_predict(X_scaled)

    print(f"✓ Clustering de recursos: {n_clusters} clusters identificados")

    return df_clean


def generar_grafico_recursos(df):
    """Genera gráfico para clustering de recursos"""
    import numpy as np

    fig, ax = plt.subplots(figsize=(16, 10))

    np.random.seed(42)
    unidad_jitter = df['UNIDAD_NUM'] + np.random.uniform(-0.35, 0.35, size=len(df))
    tipo_jitter = df['TIPOCASO_NUM'] + np.random.uniform(-0.35, 0.35, size=len(df))

    turno_sizes = df['TURNO_NUM'].map({0: 40, 1: 60, 2: 80, 3: 50})

    scatter = ax.scatter(
        unidad_jitter, tipo_jitter,
        c=df['CLUSTER_REC'], s=turno_sizes,
        cmap='viridis', alpha=0.5,
        edgecolors='white', linewidth=0.3
    )

    ax.set_xlabel('Unidad/Vehículo', fontsize=14, fontweight='bold')
    ax.set_ylabel('Tipo de Caso', fontsize=14, fontweight='bold')
    ax.set_title('Clustering de Recursos + Modelo Predictivo\n(Tamaño = turno)',
                 fontsize=16, fontweight='bold', pad=20)

    # Etiquetas
    unidades_unicas = sorted(df['UNIDAD'].dropna().unique())
    tipos_unicos = sorted(df['TIPOCASO'].dropna().unique())

    max_labels = 15
    if len(unidades_unicas) > max_labels:
        step = len(unidades_unicas) // max_labels
        ax.set_xticks(range(0, len(unidades_unicas), step))
        ax.set_xticklabels([unidades_unicas[i] for i in range(0, len(unidades_unicas), step)],
                           rotation=45, ha='right', fontsize=8)
    else:
        ax.set_xticks(range(len(unidades_unicas)))
        ax.set_xticklabels(unidades_unicas, rotation=45, ha='right', fontsize=8)

    if len(tipos_unicos) > max_labels:
        step = len(tipos_unicos) // max_labels
        ax.set_yticks(range(0, len(tipos_unicos), step))
        ax.set_yticklabels([tipos_unicos[i] for i in range(0, len(tipos_unicos), step)], fontsize=8)
    else:
        ax.set_yticks(range(len(tipos_unicos)))
        ax.set_yticklabels(tipos_unicos, fontsize=9)

    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.8)
    ax.set_facecolor('#f8f9fa')

    cbar = plt.colorbar(scatter, ax=ax, label='Cluster de Recursos', pad=0.02)

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return image_base64


def analizar_clusters_recursos(df):
    """Genera estadísticas por cluster de recursos"""
    resultados = []

    for cluster_id in sorted(df['CLUSTER_REC'].unique()):
        cluster_data = df[df['CLUSTER_REC'] == cluster_id]

        total_llamadas = len(cluster_data)

        unidad_frecuente = cluster_data['UNIDAD'].mode().values[0] if len(
            cluster_data['UNIDAD'].mode()) > 0 else 'N/A'
        tipo_frecuente = cluster_data['TIPOCASO'].mode().values[0] if len(
            cluster_data['TIPOCASO'].mode()) > 0 else 'N/A'
        turno_frecuente = cluster_data['TURNO'].mode().values[0] if len(
            cluster_data['TURNO'].mode()) > 0 else 'N/A'

        top_unidades = cluster_data['UNIDAD'].value_counts().head(3).to_dict()

        unidades_unicas = cluster_data['UNIDAD'].nunique()
        eficiencia = total_llamadas / unidades_unicas if unidades_unicas > 0 else 0

        turnos_dist = cluster_data['TURNO'].value_counts().to_dict()

        resultados.append({
            'cluster_id': int(cluster_id),
            'total_llamadas': int(total_llamadas),
            'unidad_frecuente': unidad_frecuente,
            'tipo_frecuente': tipo_frecuente,
            'turno_frecuente': turno_frecuente,
            'eficiencia': f"{eficiencia:.1f}",
            'top_unidades': top_unidades,
            'turnos_dist': turnos_dist
        })

    return resultados


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌐 SERVIDOR FLASK MEJORADO")
    print("="*60)
    print("📍 URL: http://127.0.0.1:5000")
    print("📚 Endpoints disponibles:")
    print("   - /analisis-mejorado  (Clustering con todas las mejoras)")
    print("   - /modelo-predictivo  (API de modelo predictivo)")
    print("="*60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)

