# 🚀 GUÍA RÁPIDA DE INICIO - DOCKER

## ⚡ Inicio Rápido (3 pasos)

### 1️⃣ Instalar Docker Desktop

**Windows:**
- Descargar de: https://www.docker.com/products/docker-desktop/
- Ejecutar instalador
- Reiniciar PC
- Abrir Docker Desktop

**Verificar instalación:**
```powershell
docker --version
docker-compose --version
```

---

### 2️⃣ Clonar y Ejecutar

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/ProyectoCasani.git
cd ProyectoCasani

# Construir y ejecutar (¡UN SOLO COMANDO!)
docker-compose up --build
```

**Esperar a ver:**
```
sistema-emergencias-ventanilla | * Running on http://0.0.0.0:5000
sistema-emergencias-ventanilla | * Running on all addresses (0.0.0.0)
```

---

### 3️⃣ Acceder

Abrir navegador en:
```
http://localhost:5000
```

**¡Listo! Ya está funcionando** 🎉

---

## 📋 Comandos Docker Esenciales

### Iniciar (normal):
```bash
docker-compose up
```

### Iniciar (en segundo plano):
```bash
docker-compose up -d
```

### Detener:
```bash
docker-compose down
```

### Ver logs en tiempo real:
```bash
docker-compose logs -f
```

### Reconstruir imagen:
```bash
docker-compose up --build
```

### Ver estado:
```bash
docker ps
```

---

## 🔧 Troubleshooting Docker

### ❌ Error: "docker: command not found"
**Solución:** Instalar Docker Desktop

### ❌ Error: "Cannot connect to Docker daemon"
**Solución:** Iniciar Docker Desktop

### ❌ Error: "Port 5000 is already in use"
**Solución:**
```bash
# Opción 1: Detener proceso que usa el puerto
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Opción 2: Cambiar puerto en docker-compose.yml
ports:
  - "8080:5000"  # Usar 8080 en lugar de 5000
```

### ❌ Error: "No space left on device"
**Solución:** Limpiar imágenes antiguas
```bash
docker system prune -a
```

### ❌ Error: "Timeout waiting for container"
**Solución:** Aumentar RAM de Docker Desktop
- Abrir Docker Desktop
- Settings → Resources
- Memory: Mínimo 4 GB

---

## 🎯 ¿Por qué Docker?

### ✅ Ventajas:
1. **Portabilidad:** Funciona en Windows, Mac, Linux
2. **Sin conflictos:** Entorno aislado
3. **Fácil:** Un solo comando para instalar todo
4. **Reproducible:** Siempre el mismo resultado
5. **Compartible:** Mismo entorno para todos

### 📦 Lo que Docker hace por ti:
- Instala Python 3.12
- Instala Flask, Pandas, Scikit-learn automáticamente
- Configura variables de entorno
- Expone puerto 5000
- Maneja dependencias del sistema
- Reinicia automáticamente si falla

---

## 🔄 Flujo de Trabajo Típico

```bash
# 1. Clonar proyecto
git clone [repo-url]
cd ProyectoCasani

# 2. Iniciar contenedor
docker-compose up -d

# 3. Ver logs (opcional)
docker-compose logs -f

# 4. Acceder a http://localhost:5000

# 5. Hacer cambios en el código
# Los cambios se reflejan automáticamente (hot reload)

# 6. Detener cuando termines
docker-compose down
```

---

## 📊 Estructura Docker

```
Dockerfile
  ↓
  Construye imagen con Python + dependencias
  ↓
docker-compose.yml
  ↓
  Orquesta servicios
  ↓
  Ejecuta contenedor en puerto 5000
  ↓
  Tu aplicación corriendo ✅
```

---

## 🐳 Comandos Avanzados (Opcional)

### Ejecutar comando dentro del contenedor:
```bash
docker exec -it sistema-emergencias-ventanilla python --version
```

### Acceder a terminal del contenedor:
```bash
docker exec -it sistema-emergencias-ventanilla /bin/bash
```

### Ver uso de recursos:
```bash
docker stats
```

### Copiar archivo desde contenedor:
```bash
docker cp sistema-emergencias-ventanilla:/app/static/resultados.csv ./
```

### Eliminar todo y empezar limpio:
```bash
docker-compose down --volumes --rmi all
docker-compose up --build
```

---

## 🌐 Despliegue en Producción (Opcional)

### Opción 1: Docker Hub
```bash
# Login
docker login

# Tag imagen
docker tag proyectocasani-web tu-usuario/sistema-emergencias:v2.0

# Push
docker push tu-usuario/sistema-emergencias:v2.0

# Alguien más puede usar:
docker pull tu-usuario/sistema-emergencias:v2.0
docker run -p 5000:5000 tu-usuario/sistema-emergencias:v2.0
```

### Opción 2: Render.com (Gratis)
1. Subir a GitHub
2. Conectar Render con GitHub
3. Render detecta Dockerfile automáticamente
4. ¡Listo! URL pública gratis

### Opción 3: Google Cloud Run
```bash
gcloud run deploy sistema-emergencias \
  --source . \
  --port 5000 \
  --region us-central1
```

---

## ✅ Checklist de Verificación

Antes de compartir tu proyecto, verifica:

- [ ] Docker Desktop instalado
- [ ] Proyecto clonado
- [ ] `docker-compose up` funciona
- [ ] Acceso a http://localhost:5000 correcto
- [ ] Los 3 análisis funcionan
- [ ] CSV se exportan correctamente
- [ ] No hay errores en logs
- [ ] README.md actualizado con tu usuario GitHub

---

## 🎓 Para tu Presentación

### Demostración:
```bash
# 1. Clonar en vivo (5 seg)
git clone [tu-repo]
cd ProyectoCasani

# 2. Construir y ejecutar (2 min)
docker-compose up --build

# 3. Mostrar en navegador (inmediato)
# http://localhost:5000
```

**Mensaje clave:**
> "Con un solo comando (`docker-compose up`), cualquier persona puede ejecutar este proyecto en cualquier máquina sin instalar nada manualmente."

---

## 📞 Soporte

**Problemas con Docker:**
- Documentación oficial: https://docs.docker.com/
- Docker Hub: https://hub.docker.com/

**Problemas con el proyecto:**
- Ver logs: `docker-compose logs`
- Abrir issue en GitHub
- Revisar DOCUMENTACION_PROYECTO.md

---

**¡Todo listo para compartir tu proyecto! 🚀**

