from flask import Flask,jsonify,request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'kathuria'
app.config['MYSQL_PASSWORD'] = 'Harshita@123'
app.config['MYSQL_DB'] = 'studentdb'

mysql = MySQL(app)

@app.route('/')
def hello_world():
    return '<h1>Your app is running!</h1>'

@app.route('/api/students', methods=['GET'])
def get_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student")
    results = cur.fetchall()
    cur.close()

    student_list = []
    for result in results:
        student = {
            'student_id':result[0],
            'name': result[1],
            'email': result[2],
            'phone': result[3],
            'course': result[4]
        }
        student_list.append(student)

    return jsonify(student_list)
    
    
@app.route('/api/students/<int:roll_number>', methods=['GET'])
def get_student(roll_number):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM student WHERE student_id = %s''', (roll_number,))
    result = cur.fetchone()
    cur.close()

    if result:
        student = {
            'student_id': result[0],
            'name': result[1],
            'email': result[2],
            'phone': result[3],
            'course': result[4]
        }
        return jsonify(student)
    else:
        return jsonify({'message': 'Student not found'})
@app.route('/api/students', methods=['POST'])
def add_student():
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    course = request.json['course']

    cur = mysql.connection.cursor()
    cur.execute('''INSERT INTO student (name, email, phone, course)
                   VALUES (%s, %s, %s, %s)''',
                ( name, email, phone, course))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Student added successfully'})
# Update a student by id
@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    course = request.json['course']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE student SET name=%s, email=%s, phone=%s, course=%s WHERE student_id=%s", (name, email, phone, course, id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Student updated successfully'})

# Delete a student by id
@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM student WHERE student_id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Student deleted successfully'})


   
if __name__ == '__main__':
    app.run()
