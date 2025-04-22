"""
'fast car' rental web app with CRUD functionalities using MySQL.
"""
from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import os

app = Flask(__name__)

# db configurations

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = '[your username]'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'fast_cars'
app.secret_key = '423433242'

mysql = MySQL(app)

# Convert 12-hour format to 24-hour format
def convert_to_24h(time_str):
    return datetime.strptime(time_str, "%I:%M%p").strftime("%H:%M:%S")


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users where email=%s", (field.data,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            raise ValidationError('Email Already Taken')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        name = request.form['name']
        comments = request.form['comments']
        profession = request.form['profession']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO reviews (name, comments, profession) VALUES (%s, %s, %s)",
                    (name, comments, profession))
        mysql.connection.commit()
        flash("Comments Received!")
        return redirect(url_for('testimonial'))


@app.route('/testimonial')
def testimonial():

    cur = mysql.connection.cursor()
    cur.execute("SELECT name, comments, profession FROM reviews")
    reviews = cur.fetchall()
    cur.close()
    return render_template('testimonial.html', reviews=reviews)

@app.route('/review')
def review():
    if 'user_id' not in session:
        return redirect(url_for('login', next=request.path))
    return render_template('review.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # store data into database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)", (name, email, hashed_password))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Hardcoded admin login
        if email == "admin@admin.com" and password == "admin":
            session['user_id'] = email  # Ensure session['user_id'] matches the check
            session['admin'] = True  # Optional: Separate flag for admin
            return redirect(url_for('admin_dashboard'))

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and password.encode('utf-8'):
            session['user_id'] = user[0]
            next_page = request.args.get('next') #or request.args.get('next')
            print("Next page:", next_page)  # Debugging
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash("Login failed. Please check your email and password")
            return redirect(url_for('login'))

    return render_template('login.html', form=form)



@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users where id=%s", (user_id,))
        user = cursor.fetchone()
        # cursor.close()

        # Fetch user's bookings
        cursor.execute(
            "SELECT id, car_name, pickup_location, dropoff_location, pickup_date, pickup_time, dropoff_date, dropoff_time, status, created_at FROM bookings WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,))
        bookings = cursor.fetchall()

        cursor.close()
        if user:
            # return render_template('dashboard.html', user=user)
            return render_template('dashboard.html', user=user, bookings=bookings)
    return redirect(url_for('login'))

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')



@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # flash("Message sent Successfully!")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contact (name, email, phone, subject, message) VALUES (%s, %s, %s, %s, %s)",
                    (name, email, phone, subject, message))
        mysql.connection.commit()
        flash("Message Sent Successfully!")
        return redirect(url_for('contact'))

    return render_template('contact.html')



@app.route('/cars')
def cars():
    return render_template('cars.html')



@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/book-now')
# def book_now():
#     if not session.get('user_id'):
#         return redirect(url_for('login', next=request.url))
#     return render_template('booking.html')



@app.route('/book-now', methods=['GET', 'POST'])
def book_now():
   # if not session.get('user_id'):
   #     return redirect(url_for('login', next=request.url))
    if 'user_id' not in session:
        return redirect(url_for('login', next=request.url))  # Preserve 'next'
    # return render_template('booking.html')

    if request.method == 'POST':
        car_name = request.form['car_name']
        pickup_location = request.form['pickup_location']
        dropoff_location = request.form['dropoff_location']
        pickup_date = request.form['pickup_date']
        # pickup_time = request.form['pickup_time']
        pickup_time = convert_to_24h(request.form['pickup_time'])
        dropoff_date = request.form['dropoff_date']
        # dropoff_time = request.form['dropoff_time']
        dropoff_time = convert_to_24h(request.form['dropoff_time'])
        additional_info = request.form.get('additional_info', '')

        # Validate required fields
        # if not car_name or not pickup_location or not dropoff_location:
        #     flash("All fields are required!")
        #     return redirect(url_for('book_now'))  # Reload form with error message
       # Save booking details to the database here
        cursor = mysql.connection.cursor()
        cursor.execute("""
                INSERT INTO bookings (user_id, car_name, pickup_location, dropoff_location, 
                                      pickup_date, pickup_time, dropoff_date, dropoff_time, additional_info) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (session.get('user_id'), car_name, pickup_location, dropoff_location,
                  pickup_date, pickup_time, dropoff_date, dropoff_time, additional_info))
        mysql.connection.commit()
        cursor.close()

        flash("Booking successful!")
        return redirect(url_for('dashboard', success=1))
       # return redirect(url_for('success'))  # Redirect to success page
        # return "Success"
    # return render_template('booking.html')
    return render_template('booking.html', car=request.args.get('car', ''))
@app.route('/feature')
def feature():
    return render_template('feature.html')

@app.route('/service')
def service():
    return render_template('service.html')

# USER ACCOUNT UPDATE
@app.route('/my-account')
def my_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name, email FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    return render_template('my_account.html', user=user)

@app.route('/update-profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    name = request.form['name']
    email = request.form['email']

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, user_id))
    mysql.connection.commit()
    cursor.close()

    flash("Profile updated successfully!")
    return redirect(url_for('dashboard'))


@app.route('/update-password', methods=['POST'])
def update_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT password FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if not user or not bcrypt.checkpw(current_password.encode('utf-8'), user[0].encode('utf-8')):
        flash("Current password is incorrect.")
        return redirect(url_for('my_account'))

    if new_password != confirm_password:
        flash("New passwords do not match.")
        return redirect(url_for('my_account'))

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("UPDATE users SET password=%s WHERE id=%s", (hashed_password, user_id))
    mysql.connection.commit()
    cursor.close()

    flash("Password updated successfully!")
    return redirect(url_for('dashboard'))

# ADMIN ROUTE:
@app.route('/admin-dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['user_id'] != 'admin@admin.com':
        flash("Login As Admin")
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM contact")
    total_queries = cursor.fetchone()[0]

    cursor.execute("SELECT name, email FROM users")
    # users = cursor.fetchall()
    users = [{'name': row[0], 'email': row[1]} for row in cursor.fetchall()]

    # cursor.execute("SELECT id, user_id, car_name, pickup_date, dropoff_date, status FROM bookings")
    # bookings = cursor.fetchall()

    cursor.execute("""
        SELECT b.id, u.name AS user_name, b.car_name, b.pickup_date, b.dropoff_date, b.status 
        FROM bookings b 
        JOIN users u ON b.user_id = u.id
    """)
    bookings = cursor.fetchall()

    cursor.execute("SELECT name, comments FROM reviews")
    testimonials = [{'name': row[0], 'comments': row[1]} for row in cursor.fetchall()]

    cursor.close()

    return render_template('admin_dashboard.html', total_users=total_users, total_bookings=total_bookings,
                           total_queries=total_queries, users=users, testimonials=testimonials,  bookings=bookings)

@app.route('/update-booking/<int:booking_id>/<status>')
def update_booking(booking_id, status):
    if 'admin' not in session:
        flash("Unauthorized access!")
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE bookings SET status = %s WHERE id = %s", (status, booking_id))
    mysql.connection.commit()
    cursor.close()

    flash(f"Booking {status} successfully!")
    return redirect(url_for('admin_dashboard'))

@app.route('/manage-cars')
def manage_cars():
    if 'user_id' not in session or session['user_id'] != 'admin@admin.com':
        flash("Unauthorized access!")
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, name, image FROM cars")  # Ensure only needed columns are selected
    cars = cursor.fetchall()
    cursor.close()

    cars_list = [{'id': car[0], 'name': car[1], 'image': car[2]} for car in cars]  # Convert tuple to dict

    return render_template('manage_cars.html', cars=cars_list)


@app.route('/add-car', methods=['POST'])
def add_car():
    if 'admin' not in session:
        flash("Unauthorized access!")
        return redirect(url_for('login'))

    car_name = request.form['car_name']
    car_image = request.files['car_image']

    if car_image:
        image_filename = secure_filename(car_image.filename)
        car_image.save(os.path.join('static/car_images', image_filename))

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO cars (name, image) VALUES (%s, %s)", (car_name, image_filename))
        mysql.connection.commit()
        cursor.close()

        flash("Car added successfully!")

    return redirect(url_for('manage_cars'))

@app.route('/delete-car/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM cars WHERE id = %s", (car_id,))
    mysql.connection.commit()
    cursor.close()

    flash("Car deleted successfully!")
    return redirect(url_for('manage_cars'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('_flashes', None)  # Clear previous flash messages
    flash("You have been logged out successfully.")
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=5001)
