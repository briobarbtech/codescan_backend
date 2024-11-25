from flask import Blueprint,jsonify, send_file
from data.csv_repository import read_csv,write_csv,convertir_a_excel
from datetime import datetime
students = Blueprint('students', __name__)



@students.route('/students')
def all_students():
    students_list = read_csv('students')
    students = []
    for row in students_list:
            students.append({
                "nombre": row[0],
                "apellido":row[1],
                "fecha_de_nacimiento":row[2],
                "id":row[3]
                })
    return jsonify(students)


@students.route('/students/<id>')
def get_student(id):
    students_list = read_csv('students')
    for student in students_list:
        if student[3] == id:
            return jsonify({
                "nombre": student[0],
                "apellido":student[1],
                "fecha_de_nacimiento":student[2],
                "id":student[3]
                })
    return "Not found"


@students.route('/students/<id>',methods=['POST'])
def push_assistence(id):
    write_csv("assistance",id)
    return "Ok"


@students.route('/students/download', methods=['GET'])
def descargar_asistencia():
    dttm = datetime.now().strftime('%Y-%m-%d %H:%M:%S').replace(':', ';')
    convertir_a_excel(dttm)
    try:
        # Ruta al archivo Excel generado
        archivo_excel = f"../excel/asistencia_estudiantes_{dttm}.xlsx"
        # Enviar el archivo como descarga
        return send_file(
            archivo_excel,
            as_attachment=True,  # Indica que debe ser descargado
            download_name=f"asistencia_estudiantes_{dttm}.xlsx",  # Nombre del archivo descargado
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        return f"Error al enviar el archivo: {e}", 500
    
    
def page_not_found(error):
    return '<h1> ERROR 404: Page not found </h1>'