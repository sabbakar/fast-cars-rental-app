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

2. **Set up virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

Create MySQL database

Import schema.sql into your MySQL server.

Update main.py with your MySQL credentials (DB name, user, password).
