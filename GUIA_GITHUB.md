# 📤 CÓMO SUBIR TU PROYECTO A GITHUB

## 🎯 Objetivo
Subir tu proyecto a GitHub para que cualquiera pueda clonarlo y ejecutarlo con Docker.

---

## 📋 Pre-requisitos

1. ✅ Cuenta en GitHub (https://github.com)
2. ✅ Git instalado en tu PC
3. ✅ Todos los archivos Docker creados

---

## 🚀 PASO A PASO

### 1️⃣ Verificar Git

```powershell
# Verificar instalación
git --version

# Si no está instalado, descargar de:
# https://git-scm.com/download/win
```

### 2️⃣ Configurar Git (Primera vez)

```powershell
# Configurar nombre
git config --global user.name "Tu Nombre"

# Configurar email
git config --global user.email "tu@email.com"
```

### 3️⃣ Inicializar Repositorio Local

```powershell
# Navegar a tu proyecto
cd "C:\db\Nik Denilson\Universidad\IntiligenciaArtificial\ProyectoCasani"

# Inicializar Git (si no existe .git)
git init

# Ver estado
git status
```

### 4️⃣ Agregar Archivos

```powershell
# Agregar TODOS los archivos
git add .

# Verificar qué se agregó (verde = agregado, rojo = ignorado)
git status
```

### 5️⃣ Hacer Commit

```powershell
# Commit inicial
git commit -m "feat: Sistema de análisis de emergencias con Docker"

# Verificar
git log --oneline
```

### 6️⃣ Crear Repositorio en GitHub

1. Ir a: https://github.com/new
2. **Repository name:** `ProyectoCasani` o `SistemaEmergenciasVentanilla`
3. **Description:** Sistema de análisis de llamadas de emergencia con K-means
4. **Visibility:** Public (para compartir) o Private
5. ✅ **NO marcar** "Initialize with README" (ya tienes uno)
6. Click **Create repository**

### 7️⃣ Conectar con GitHub

GitHub te mostrará comandos, pero usa estos:

```powershell
# Agregar remote (cambiar TU_USUARIO por tu usuario real)
git remote add origin https://github.com/TU_USUARIO/ProyectoCasani.git

# Verificar
git remote -v

# Cambiar rama a main
git branch -M main
```

### 8️⃣ Subir Código (Push)

```powershell
# Primera vez (con -u)
git push -u origin main

# Te pedirá login de GitHub
# Username: tu_usuario
# Password: tu_token (NO tu contraseña)
```

**⚠️ IMPORTANTE:** GitHub ya no acepta contraseñas. Necesitas un **Personal Access Token**.

#### Crear Token:
1. GitHub → Settings (tu perfil)
2. Developer settings → Personal access tokens → Tokens (classic)
3. Generate new token (classic)
4. Nombre: "ProyectoCasani"
5. Expiration: 90 days
6. Scopes: Marcar **repo**
7. Generate token
8. **COPIAR EL TOKEN** (no lo volverás a ver)
9. Usar como contraseña en el push

### 9️⃣ Verificar

1. Refrescar tu repositorio en GitHub
2. Deberías ver todos los archivos
3. README.md se muestra automáticamente

---

## ✅ VERIFICACIÓN FINAL

Tu repositorio debe tener:

```
ProyectoCasani/
├── app_mejorado.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── README.md
├── DOCUMENTACION_PROYECTO.md
├── GUIA_DOCKER.md
├── static/
│   └── style.css
└── templates/
    ├── *.html
    └── Data/
        └── EtlData.xlsx
```

**⚠️ VERIFICAR:** El archivo `EtlData.xlsx` debe estar incluido (es tu dataset).

---

## 🔄 ACTUALIZAR REPOSITORIO (Cambios Futuros)

```powershell
# Ver cambios
git status

# Agregar cambios
git add .

# Commit
git commit -m "fix: corregir error en clustering geográfico"

# Subir
git push
```

---

## 👥 CÓMO OTRAS PERSONAS USARÁN TU PROYECTO

1. **Clonar:**
   ```bash
   git clone https://github.com/TU_USUARIO/ProyectoCasani.git
   cd ProyectoCasani
   ```

2. **Ejecutar con Docker:**
   ```bash
   docker-compose up --build
   ```

3. **Acceder:**
   ```
   http://localhost:5000
   ```

**¡Listo!** Sin instalar Python, Flask, Pandas, etc. manualmente.

---

## 📊 BADGES PARA TU README

Agrega estos badges al inicio de tu README.md en GitHub:

```markdown
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![GitHub](https://img.shields.io/github/stars/TU_USUARIO/ProyectoCasani?style=social)](https://github.com/TU_USUARIO/ProyectoCasani)
```

---

## 🌟 HACER PÚBLICO TU PROYECTO

### Compartir:
```
https://github.com/TU_USUARIO/ProyectoCasani
```

### En tu presentación:
> "Este proyecto está disponible públicamente en GitHub. Cualquiera puede clonarlo y ejecutarlo en su máquina con un solo comando: `docker-compose up`"

### En tu CV:
```
Sistema de Análisis de Emergencias con ML
Python | Flask | Scikit-learn | Docker
GitHub: github.com/TU_USUARIO/ProyectoCasani
```

---

## 🔐 PRIVACIDAD DEL DATASET

Si el dataset contiene información sensible:

### Opción 1: Excluir del repositorio
Editar `.gitignore`:
```
# Excluir dataset
templates/Data/*.xlsx
```

Luego:
```powershell
git rm --cached templates/Data/EtlData.xlsx
git commit -m "remove: excluir dataset sensible"
git push
```

### Opción 2: Usar dataset de ejemplo
Crear `templates/Data/example_data.xlsx` con datos ficticios.

---

## 📝 MENSAJES DE COMMIT RECOMENDADOS

Usa estos prefijos:

```bash
feat:    nueva funcionalidad
fix:     corrección de error
docs:    cambios en documentación
style:   formato, punto y coma, etc.
refactor: refactorización de código
test:    agregar tests
chore:   mantenimiento
```

**Ejemplos:**
```bash
git commit -m "feat: agregar clustering geográfico"
git commit -m "fix: corregir error 404 en rutas"
git commit -m "docs: actualizar README con Docker"
git commit -m "refactor: optimizar clustering con K-means"
```

---

## 🚨 PROBLEMAS COMUNES

### ❌ "fatal: remote origin already exists"
**Solución:**
```powershell
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/ProyectoCasani.git
```

### ❌ "Authentication failed"
**Solución:** Usar Personal Access Token, no contraseña.

### ❌ "large files detected"
**Solución:**
```powershell
# Si el dataset es muy grande (>100MB)
# Ver: https://git-lfs.github.com/
```

### ❌ "refusing to merge unrelated histories"
**Solución:**
```powershell
git pull origin main --allow-unrelated-histories
git push
```

---

## 📦 ALTERNATIVAS A GITHUB

Si no quieres usar GitHub:

1. **GitLab** - Más privacidad (gitlab.com)
2. **Bitbucket** - Integrado con Jira (bitbucket.org)
3. **Compartir ZIP** - Subir a Google Drive/OneDrive

---

## ✅ CHECKLIST FINAL

Antes de compartir:

- [ ] README.md completo
- [ ] Dockerfile funcional
- [ ] docker-compose.yml configurado
- [ ] requirements.txt actualizado
- [ ] .gitignore correcto
- [ ] Dataset incluido (o excluido si es sensible)
- [ ] Subido a GitHub
- [ ] URL pública funcional
- [ ] Probado: `git clone` + `docker-compose up`

---

## 🎓 PARA TU PRESENTACIÓN

### Slide 1: Introducción
```
Título: Sistema de Análisis de Emergencias
Subtítulo: Dockerizado para despliegue universal
GitHub: github.com/TU_USUARIO/ProyectoCasani
```

### Slide 2: Demo en Vivo
```
$ git clone https://github.com/TU_USUARIO/ProyectoCasani.git
$ cd ProyectoCasani
$ docker-compose up

→ http://localhost:5000 ✅
```

### Slide 3: Ventajas
```
✅ Funciona en cualquier máquina
✅ Sin instalación manual
✅ Reproducible
✅ Open source en GitHub
```

---

**¡Tu proyecto ya está listo para compartir con el mundo!** 🌍🚀

