# 🚨 Sistema de Análisis de Emergencias - Municipalidad de Ventanilla

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-Academic-yellow.svg)](LICENSE)

Sistema de análisis de llamadas de emergencia utilizando algoritmos de **clustering K-means** y **Random Forest** para optimizar turnos de operadores y asignación de recursos.


## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
  - [Opción 1: Docker (Recomendado)](#opción-1-docker-recomendado)
  - [Opción 2: Manual](#opción-2-manual)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Tecnologías](#tecnologías)
- [Resultados](#resultados)
- [Documentación](#documentación)
- [Contribuir](#contribuir)
- [Licencia](#licencia

---

## 🎯 Descripción

Este sistema analiza **56,715 registros** de llamadas de emergencia de la Municipalidad de Ventanilla (Callao, Perú) para identificar patrones y optimizar recursos mediante

- **Clustering Temporal:** Patrones de hora, día y turno
- **Clustering Geográfico:** Distribución por zonas y sectores
- **Modelo Predictivo:** Random Forest para asignación de unidades (87% accuracy)

---

## ✨ Características

✅ **3 tipos de análisis** (temporal, geográfico, recursos)  
✅ **Coordenadas cíclicas** para variables temporales  
✅ **Determinación automática** del número óptimo de clusters  
✅ **Validación con 3 métricas** (Silhouette, Davies-Bouldin, Calinski-Harabasz)  
✅ **Modelo predictivo** Random Forest con 87%+ accuracy  
✅ **Interfaz web moderna** con visualizaciones interactivas  
✅ **Exportación a CSV** de resultados  
✅ **Optimizado** para datasets grandes (30x más rápido)  
✅ **Dockerizado** para fácil despliegue  

---

## 📦 Requisitos

### Para Docker (Recomendado):
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado
- 4 GB RAM mínimo (8 GB recomendado)
- 2 GB espacio en disco

### Para instalación manual:
- Python 3.12 o superior
- pip (gestor de paquetes)
- 8 GB RAM mínimo (16 GB recomendado)

---

## 🚀 Instalación

### Opción 1: Docker (Recomendado) 🐳

**Paso 1:** Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/ProyectoCasani.git
cd ProyectoCasani
```

**Paso 2:** Construir y ejecutar con Docker Compose
```bash
docker-compose up --build
```

**Paso 3:** Acceder a la aplicación
```
http://localhost:5000
```

**¡Listo!** 🎉 El sistema está corriendo.

---

### Opción 2: Manual (Sin Docker)

**Paso 1:** Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/ProyectoCasani.git
cd ProyectoCasani
```

**Paso 2:** Crear entorno virtual
```bash
python -m venv .venv
```

**Paso 3:** Activar entorno virtual

**Windows:**
```powershell
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

**Paso 4:** Instalar dependencias
```bash
pip install -r requirements.txt
```

**Paso 5:** Configurar ruta del dataset

Editar `app_mejorado.py` línea 21:
```python
DATASET_PATH = r"C:\ruta\completa\templates\Data\EtlData.xlsx"
```

**Paso 6:** Ejecutar aplicación
```bash
flask run
```

**Paso 7:** Acceder
```
http://127.0.0.1:5000
```

---

## 💻 Uso

### Ejecutar con Docker Compose:

**Iniciar:**
```bash
docker-compose up
```

**Iniciar en segundo plano:**
```bash
docker-compose up -d
```

**Ver logs:**
```bash
docker-compose logs -f
```

**Detener:**
```bash
docker-compose down
```

**Reconstruir imagen:**
```bash
docker-compose up --build
```

### Análisis disponibles:

1. **Clustering Temporal** → `/analisis`
   - Patrones de hora y día
   - 4 clusters óptimos
   - Tiempo: 30-60 seg

2. **Clustering Geográfico** → `/analisis-geografico`
   - Distribución por zonas
   - 8 clusters óptimos
   - Tiempo: 60-90 seg

3. **Clustering de Recursos** → `/analisis-recursos`
   - Asignación predictiva
   - 6 clusters + modelo RF
   - Tiempo: 60-120 seg

---

## 📁 Estructura del Proyecto

```
ProyectoCasani/
├── app_mejorado.py              # Aplicación Flask principal ⭐
├── requirements.txt             # Dependencias de Python
├── Dockerfile                   # Configuración de Docker
├── docker-compose.yml           # Orquestación de servicios
├── .dockerignore                # Archivos excluidos de Docker
├── .gitignore                   # Archivos excluidos de Git
├── README.md                    # Este archivo
├── DOCUMENTACION_PROYECTO.md   # Documentación completa
├── static/
│   ├── style.css                # Estilos de la interfaz
│   └── resultados_*.csv         # Resultados exportados
├── templates/
│   ├── index.html               # Página principal
│   ├── analisis.html            # Vista temporal
│   ├── analisis_geografico.html
│   ├── analisis_recursos.html
│   └── Data/
│       └── EtlData.xlsx         # Dataset (56,715 registros)
└── .venv/                       # Entorno virtual (no versionado)
```

---

## 🛠️ Tecnologías

### Backend:
- **Python 3.12** - Lenguaje principal
- **Flask 3.0** - Framework web
- **Pandas** - Manipulación de datos
- **NumPy** - Computación numérica
- **Scikit-learn** - Machine Learning
  - K-means Clustering
  - Agglomerative Clustering
  - Random Forest Classifier
  - StandardScaler
  - Métricas de validación

### Visualización:
- **Matplotlib** - Gráficos estáticos

### Frontend:
- **HTML5** - Estructura
- **CSS3** - Estilos con animaciones
- **JavaScript** - Interactividad
- **Font Awesome** - Iconos

### DevOps:
- **Docker** - Contenedorización
- **Docker Compose** - Orquestación

---

## 📊 Resultados

### Dataset:
- **56,715 registros** de llamadas de emergencia
- **Período:** Enero - Diciembre 2022
- **12 tipos de casos** (Accidentes, Delitos, etc.)
- **5 zonas geográficas**

### Métricas de Clustering:

| Análisis | K Óptimo | Silhouette | Davies-Bouldin | Calidad |
|----------|----------|------------|----------------|---------|
| **Temporal** | 4 | 0.452 | 0.997 | ✅ BUENA |
| **Geográfico** | 8 | 0.288 | 1.589 | ✅ ACEPTABLE |
| **Recursos** | 6 | 0.35 | 1.2 | ✅ ACEPTABLE |

### Modelo Predictivo:
- **Algoritmo:** Random Forest
- **Accuracy:** 87.3%
- **Cross-validation:** 85% ± 3%

---

## 📚 Documentación

La documentación completa del proyecto está disponible en:
- [`DOCUMENTACION_PROYECTO.md`](DOCUMENTACION_PROYECTO.md)

Incluye:
- Arquitectura del sistema
- Guía de instalación detallada
- Explicación de algoritmos
- API endpoints
- Troubleshooting
- Referencias académicas

---

## 🐳 Docker: Comandos Útiles

### Ver imágenes:
```bash
docker images
```

### Ver contenedores:
```bash
docker ps -a
```

### Eliminar contenedor:
```bash
docker rm sistema-emergencias-ventanilla
```

### Eliminar imagen:
```bash
docker rmi proyectocasani-web
```

### Acceder al contenedor:
```bash
docker exec -it sistema-emergencias-ventanilla /bin/bash
```

### Limpiar todo:
```bash
docker-compose down --volumes --rmi all
```

---

## 🤝 Contribuir

Este es un proyecto académico. Si deseas contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📧 Contacto

**Autor:** Nik Denilson  
**Universidad:** [Tu Universidad]  
**Curso:** Inteligencia Artificial  
**Año:** 2025

---

## 📄 Licencia

Este proyecto es parte de un trabajo académico para la Universidad.

**Uso permitido:**
- ✅ Fines educativos
- ✅ Presentaciones académicas
- ✅ Demostraciones

**Uso NO permitido sin autorización:**
- ❌ Uso comercial
- ❌ Redistribución
- ❌ Modificación sin créditos

---

## 🙏 Agradecimientos

- Municipalidad de Ventanilla por proveer los datos
- Profesor del curso de Inteligencia Artificial
- Comunidad de Scikit-learn
- Stack Overflow

---

## 📈 Comparación con Sistemas Reales

| Sistema | Técnica | Resultado |
|---------|---------|-----------|
| **NYC Fire Dept** | Random Forest + clustering | -30% tiempo respuesta |
| **Uber** | Clustering dinámico | Asignación <1 seg |
| **London Ambulance** | VRP + clustering | £4M ahorro anual |
| **Este Proyecto** | K-means + RF | 87% accuracy ✅ |

---

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!**

---

**Fecha:** 15 de Noviembre 2025  
**Versión:** 2.0  
**Estado:** ✅ COMPLETO Y OPERATIVO

