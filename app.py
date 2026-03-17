from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Configuración del archivo de datos
COURSES_FILE = 'courses.json'

# ============================================================
# FUNCIONES DE PERSISTENCIA (MANEJO DEL ARCHIVO JSON)
# ============================================================

def load_courses():
    """
    Carga los cursos desde el archivo JSON. 
    Si el archivo no existe o está corrupto, devuelve una lista vacía.
    """
    if not os.path.exists(COURSES_FILE):
        # Si el archivo no existe, lo creamos vacío
        save_courses([])
        return []
    
    try:
        with open(COURSES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        # Manejo de errores de lectura o formato JSON
        print(f"Error al leer {COURSES_FILE}: {e}")
        return []

def save_courses(courses):
    """
    Guarda la lista de cursos en el archivo JSON con formato legible (indent).
    """
    try:
        with open(COURSES_FILE, 'w', encoding='utf-8') as f:
            json.dump(courses, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error al escribir en {COURSES_FILE}: {e}")
        raise  # Re-lanzamos el error para que Flask lo capture si es necesario

# ============================================================
# ENDPOINTS DE LA API REST
# ============================================================

# 1. POST /api/courses - Crear un nuevo curso
@app.route('/api/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    
    # Validar que se enviaron datos
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    # Campos requeridos según los requisitos
    required_fields = ['name', 'description', 'target_date', 'status']
    
    # Comprobar si falta algún campo
    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            return jsonify({"error": f"El campo '{field}' es requerido"}), 400
            
    # Validar valores permitidos para 'status'
    valid_statuses = ["No Comenzado", "En Progreso", "Completado"]
    if data['status'] not in valid_statuses:
        return jsonify({
            "error": f"Estado inválido. Debe ser uno de: {', '.join(valid_statuses)}"
        }), 400

    courses = load_courses()
    
    # Generar ID automáticamente (empezando desde 1)
    new_id = 1
    if courses:
        # Buscamos el ID más alto y sumamos 1
        new_id = max(course['id'] for course in courses) + 1
        
    # Crear el objeto del curso
    new_course = {
        "id": new_id,
        "name": data['name'],
        "description": data['description'],
        "target_date": data['target_date'],
        "status": data['status'],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    courses.append(new_course)
    save_courses(courses)
    
    return jsonify(new_course), 201

# 2. GET /api/courses - Obtener todos los cursos
@app.route('/api/courses', methods=['GET'])
def get_courses():
    courses = load_courses()
    return jsonify(courses), 200

# 3. GET /api/courses/<id> - Obtener un curso específico
@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    courses = load_courses()
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if course is None:
        return jsonify({"error": "Curso no encontrado"}), 404
        
    return jsonify(course), 200

# 4. PUT /api/courses/<id> - Actualizar un curso
@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
        
    courses = load_courses()
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if course is None:
        return jsonify({"error": "Curso no encontrado"}), 404
        
    # Validar 'status' si se intenta actualizar
    if 'status' in data:
        valid_statuses = ["No Comenzado", "En Progreso", "Completado"]
        if data['status'] not in valid_statuses:
            return jsonify({
                "error": f"Estado inválido. Debe ser uno de: {', '.join(valid_statuses)}"
            }), 400

    # Actualizar campos (solo si están presentes en la petición)
    fields_to_update = ['name', 'description', 'target_date', 'status']
    for field in fields_to_update:
        if field in data:
            course[field] = data[field]
            
    save_courses(courses)
    return jsonify(course), 200

# 5. DELETE /api/courses/<id> - Eliminar un curso
@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    courses = load_courses()
    course_to_delete = next((c for c in courses if c['id'] == course_id), None)
    
    if course_to_delete is None:
        return jsonify({"error": "Curso no encontrado"}), 404
        
    # Crear una nueva lista excluyendo el ID seleccionado
    updated_courses = [c for c in courses if c['id'] != course_id]
    save_courses(updated_courses)
    
    return jsonify({"message": f"Curso con ID {course_id} eliminado correctamente"}), 200

# 6. GET /api/courses/stats - Obtener estadísticas de los cursos
@app.route('/api/courses/stats', methods=['GET'])
def get_stats():
    courses = load_courses()
    
    # Contar cursos por cada estado
    stats = {
        "total_courses": len(courses),
        "by_status": {
            "No Comenzado": len([c for c in courses if c['status'] == "No Comenzado"]),
            "En Progreso": len([c for c in courses if c['status'] == "En Progreso"]),
            "Completado": len([c for c in courses if c['status'] == "Completado"])
        }
    }
    
    return jsonify(stats), 200

# ============================================================
# MANEJO DE ERRORES GLOBALES
# ============================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ruta o recurso no encontrado"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Ocurrió un error interno en el servidor"}), 500

# ============================================================
# INICIO DE LA APLICACIÓN
# ============================================================

if __name__ == '__main__':
    # Asegurarse de que el archivo JSON existe antes de arrancar
    if not os.path.exists(COURSES_FILE):
        save_courses([])

    # Mensajes de inicio personalizados
    print(f"- CodeCraftHub API is starting...")
    print(f"- Data will be stored in: `{os.path.abspath(COURSES_FILE)}`")
    print(f"- API will be available at: `http://localhost:5000`")
    
    app.run(debug=True, port=5000)
