
# Fast Cars - Car Rental System

A car rental web application built with Flask and MySQL.

## Features

- User Registration & Login  
- Car Listings & Booking  
- Admin Dashboard  
- Testimonials  
- Contact Page

## Requirements

- Python 3  
- Flask  
- MySQL  
- XAMPP (or other MySQL setup)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/fast-cars.git
   cd fast-cars
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create MySQL database**
   - Import `schema.sql` into your MySQL server.
   - Update `main.py` with your MySQL credentials (DB name, user, password).

4. **Run the app**
   ```bash
   python main.py
   ```

5. Visit `http://127.0.0.1:5000` in your browser.

## Admin Login

- Email: `admin@admin.com`  
- Password: (hardcoded or set in DB)

---


```
