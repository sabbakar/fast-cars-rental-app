```markdown
# Fast Cars - Car Rental System

A car rental web application built with **Flask** and **MySQL**.

## Features

- **User Registration & Login**  
  Users can create accounts and log in to book cars.

- **Car Listings & Booking**  
  Display cars available for rent with booking functionality.

- **Admin Dashboard**  
  Admin can manage users, cars, bookings, and testimonials.

- **Testimonials**  
  Users can leave reviews for rented cars.

- **Contact Page**  
  A page for users to contact the support team.

- **Booking Page**  
  Users can view, book, and cancel their bookings.

## Requirements

- **Python 3**
- **Flask**  
  Web framework for Python.
- **MySQL**  
  Relational database for storing user and car data.
- **XAMPP** (or other MySQL setup)  
  For setting up MySQL locally.
- **pip**  
  Python package installer.

## Setup Instructions

### 1. Clone the repository
Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/yourusername/fast-cars.git
cd fast-cars
```

### 2. Set up a virtual environment
Create and activate a virtual environment for Python:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install the required dependencies
Install all the required libraries and dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Create MySQL database
Create the **MySQL database** for the application.

- Open **XAMPP** or your MySQL setup.
- Run the following SQL commands:

```sql
CREATE DATABASE fast_cars;
```

- Import the database schema by running:

```bash
source schema.sql
```

### 5. Configure MySQL credentials
In the `main.py` file, update the database connection with your MySQL credentials:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'yourusername'
app.config['MYSQL_PASSWORD'] = 'yourpassword'
app.config['MYSQL_DB'] = 'fast_cars'
```

### 6. Running the Application

After setting up everything, you can run the Flask application with:

```bash
python main.py
```

Now, open your browser and visit `http://localhost:5000` to access the car rental system.

## File Structure

```
fast-cars/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── car_list.html
│   │   ├── booking.html
│   │   ├── contact.html
│   │   └── dashboard.html
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── models/
│   │   ├── user.py
│   │   ├── car.py
│   │   └── booking.py
│   └── forms/
│       └── registration_form.py
│
├── requirements.txt
├── schema.sql
└── README.md
```

## Usage

Once the app is running, you can access the following pages:

- **Home Page**: Displays a welcome message and car rental options.
- **User Registration & Login**: Allows users to create an account and log in.
- **Car Listings**: Displays available cars for rent with their details.
- **Booking Page**: Allows users to book cars.
- **Admin Login**: Use the hardcoded email `admin@admin.com` and password `adminpassword` to log in as an admin and access the admin dashboard.
- **Admin Dashboard**: Admin can view users, bookings, and testimonials.
- **Contact Page**: For users to get in touch with support.



## Acknowledgements

- Flask for the web framework
- MySQL for the database management system
- XAMPP for setting up MySQL locally
- The Bootstrap framework for styling

