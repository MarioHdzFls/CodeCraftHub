# 🚀 CodeCraftHub - API de Gestión de Cursos

¡Bienvenido a **CodeCraftHub**! Este es un proyecto educativo diseñado para enseñarte cómo construir una **API REST** funcional utilizando **Python** y el micro-framework **Flask**.

La aplicación te permite gestionar una lista de cursos (Crear, Leer, Actualizar y Eliminar - CRUD) almacenando toda la información de forma persistente en un archivo local `courses.json`.

---

## 🌟 Características

- **API REST Completa:** Implementa todos los métodos estándar (`GET`, `POST`, `PUT`, `DELETE`).
- **Persistencia Automática:** Los datos se guardan en un archivo JSON, por lo que no se pierden al reiniciar el servidor.
- **Validación de Datos:** Protege la integridad de los datos validando campos requeridos y estados permitidos.
- **IDs Auto-incrementales:** Genera identificadores únicos automáticamente para cada curso.
- **Gestión de Errores:** Respuestas claras en formato JSON cuando algo sale mal (404 Not Found, 400 Bad Request).

---

## 🛠️ Requisitos Previos

Antes de empezar, asegúrate de tener instalado:
- [Python 3.8+](https://www.python.org/downloads/)
- `pip` (el gestor de paquetes de Python, que viene incluido con Python).

---

## ⚙️ Instalación (Paso a Paso)

1. **Clonar o descargar el proyecto:**
   Si tienes Git:
   ```bash
   git clone https://github.com/MarioHdzFls/CodeCraftHub.git
   cd codecraft-hub
   ```

2. **Crear un entorno virtual (Recomendado):**
   Esto mantiene las librerías del proyecto aisladas de tu sistema.
   ```bash
   # En Windows
   python -m venv venv
   .\venv\Scripts\activate

   # En macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
   *Nota: Si no tienes el archivo, simplemente ejecuta `pip install flask`.*

---

## 🚀 Cómo Ejecutar la Aplicación

Para iniciar el servidor de desarrollo, ejecuta el siguiente comando en tu terminal:

```bash
python app.py
```

Verás un mensaje indicando que el servidor está corriendo en `http://127.0.0.1:5000`. ¡Ya puedes empezar a hacer peticiones!

---

## 📚 Documentación de la API

### 1. Obtener todos los cursos
- **URL:** `/api/courses`
- **Método:** `GET`
- **Descripción:** Devuelve una lista de todos los cursos registrados.

### 2. Crear un nuevo curso
- **URL:** `/api/courses`
- **Método:** `POST`
- **Cuerpo (JSON):**
```json
{
  "name": "Python para Todos",
  "description": "Curso básico de programación",
  "target_date": "2024-12-31",
  "status": "No Comenzado"
}
```

### 3. Obtener un curso específico
- **URL:** `/api/courses/<id>`
- **Método:** `GET`
- **Ejemplo:** `/api/courses/1`

### 4. Actualizar un curso
- **URL:** `/api/courses/<id>`
- **Método:** `PUT`
- **Descripción:** Puedes actualizar uno o varios campos.
- **Cuerpo (JSON):**
```json
{
  "status": "En Progreso"
}
```

### 5. Eliminar un curso
- **URL:** `/api/courses/<id>`
- **Método:** `DELETE`

### 6. Obtener estadísticas de los cursos
- **URL:** `/api/courses/stats`
- **Método:** `GET`
- **Descripción:** Devuelve el número total de cursos y el desglose por estado (No Comenzado, En Progreso, Completado).
- **Ejemplo de respuesta:**
```json
{
  "total_courses": 5,
  "by_status": {
    "No Comenzado": 2,
    "En Progreso": 2,
    "Completado": 1
  }
}
```

---

## 🧪 Cómo realizar Pruebas

Puedes probar la API de varias formas:

1. **Terminal (cURL):**
   ```bash
   curl -X GET http://localhost:5000/api/courses
   ```
2. **Postman o Insomnia:** Herramientas visuales ideales para principiantes.
3. **Navegador:** Solo para los métodos `GET` (visita `http://localhost:5000/api/courses`).

---

## 📂 Estructura del Proyecto

```text
CodeCraftHub/
├── app.py              # Código principal de la aplicación Flask
├── courses.json        # "Base de datos" en formato JSON (se crea solo)
├── requirements.txt    # Lista de librerías necesarias
├── README.md           # Este archivo guía
└── templates/          # (Opcional) Archivos HTML para el futuro
```

---

## ❓ Solución de Problemas Comunes

- **"Address already in use":** El puerto 5000 está ocupado. Cierra cualquier otro programa que lo use o cambia el puerto en `app.run(port=5000)`.
- **"ModuleNotFoundError: No module named 'flask'":** Asegúrate de haber activado tu entorno virtual y ejecutado `pip install flask`.
- **JSON inválido en el cuerpo:** Asegúrate de usar comillas dobles `"` y no simples `'` en tus peticiones POST/PUT.

---

¡Felicidades! Estás aprendiendo a construir el motor de las aplicaciones modernas. 💻✨
