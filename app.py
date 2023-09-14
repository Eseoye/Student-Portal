
from flask import Flask, request, redirect, flash, url_for, current_app, render_template
import datetime, os, json
import psycopg2 
from whitenoise import WhiteNoise
from decouple import config 

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")
app.secret_key = config('SECRET_KEY', default='default_secret_key')

def get_db_connection():
    
    
    conn = psycopg2.connect(
        host = config('DB_HOST'),
        database = config('DB_NAME'),
        user = config('DB_USER'),
        password = config('DB_PASSWORD'),
        port = config('DB_PORT')
    )
    return conn




@app.route('/')
def home():
    
    return render_template('home.html')

@app.route('/portal')
def portal():
    
    return render_template('portal.html')

@app.route('/portalHandler', methods=['POST'])
def portalHandler():
     if request.method == 'POST':
         name= ''
         firstname = request.form.get('firstname') or None
         middlename = request.form.get('middlename') or None
         lastname = request.form.get('lastname') or None
         email = request.form.get('email') or None
         dob = request.form.get('dob') or None
         gender = request.form.get('gender') or None
         phone = request.form.get('phone') or None
         address = request.form.get('address') or None
         state = request.form.get('state') or None
         lga = request.form.get('lga') or None
         kin = request.form.get('kin') or None
         score = request.form.get('score') or None
         image = request.files.get('image') or None
         
         if firstname and middlename and lastname and email and dob and gender and phone and address and state and lga and score and image:
             name = firstname + '_' + lastname + '_' + image.filename
             filepath = os.path.join(current_app.root_path, 'static/images/' + name)
             image.save(filepath)
             conn = get_db_connection()
             cur = conn.cursor()
             cur.execute('INSERT INTO students(firstname, middlename, lastname, email, dob, gender, phone, address, state, lga, kin, score, img_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (firstname, middlename, lastname, email, dob, gender, phone, address, state, lga, kin, score, name))
             conn.commit()
             cur.close()
             
         else:
            flash('Please fill all fields', 'flash_error')
            return redirect(url_for('portal'))
         flash('Successfully added student', 'flash_success')
         return redirect(url_for('index.html'))
     return redirect(url_for('portal'))
 
 
 
 
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        students = ''
        name = request.form.get('searchName') or None
        status = request.form.get('searchStatus') or None
        gender = request.form.get('searchGender') or None
        score = request.form.get('searchScore') or None
        print('score:', score)
        
        if name or status or gender or score:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('select * from students where firstname like %s or firstname is null or middlename like %s or middlename is null or lastname like %s or lastname is null or status like %s or status is null or gender like %s or gender is null or jamb = %s or score is null order by student_id', (name, name, name, status, gender, score))
            rv = cur.fetchall()
            students = rv
        else:
            flash('Please Add a Search Term', 'flash_success')
            return redirect(url_for('index'))
        flash('Search Completed', 'flash_success')
        return render_template('index.html', students = students)
    
    return redirect(url_for('index'))

@app.route('/index.html')
def index():
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select * from students order by student_id')
    rv = cur.fetchall()
    student = rv
    
    
    return render_template('index.html', students = student)

if __name__ == "__main__":
    app.run(debug = config('DEBUG', default='False', cast=bool))
    