# Fast Cars - Car Rental System

A car rental web application built with **Flask** and **MySQL**.

### Backend Demo
Watch the demo video showcasing the backend and admin features:

[Backend Demo Video](https://drive.google.com/file/d/1GWAbL3QXgwUEc_bBxWdVz1ZBydbKsxK-/view?usp=sharing)

### Frontend Demo
Watch the demo video showcasing the frontend UI features:

[Frontend Demo Video](https://drive.google.com/file/d/108AxfP9NSyPwILwmEF0oGHVoWCeEIesN/view?usp=sharing)

## Features

- User registration, login, and account management
- User dashboard to update account, view bookings and their details
- Car listings and booking system
- Admin dashboard to manage cars, users, and bookings
- Testimonials from users
- Contact form

### Hardcoded Admin Login:
  **Email:** `admin@admin.com` | **Password:** `admin`

## Other UI Features
  - `app.html` serves as the base template for frontend layout (e.g. footer, navbar).
  - Most templates inherit from `app.html` using Jinja templating.
  - `index.html` is a standalone page and does not extend `app.html`.
  - **Dynamic Navigation Button**: The top-right button switches between "Login" and "Logout" based on the user's session state. If logged in as admin, it becomes "Admin Dashboard."
  - **Conditional Links**: "Book Now" button appears only when appropriate, with auto-redirection after login.
  - **Pre-filled Booking Form**: Automatically fills in car details if a user comes from a car listing page.
  - **Admin-Only Features**: Admin users can manage cars, bookings, and see stats such as total users, bookings, and testimonials.
  - **Responsive Design**: Fully mobile-friendly.
  - **Flash Messages**: Success and error feedback displayed to users.
  - **Smooth Transitions**: Elegant page transitions and user actions.
  - **Simple Database Structure**: Well-defined tables for managing data.

## Requirements

- Python 3
- Flask
- MySQL
- pip
- XAMPP (or any MySQL server)

## Setup Instructions

1. **Clone repository:**
   ```bash
   git clone https://github.com/sabbakar/fast-cars-rental-app.git
   cd fast-cars-rental-app
   ```

2. **Create virtual environment:(Linux)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
    For **Windows**:

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ``` 

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up database:**
   - Create database (inside MySQL shell):
     ```sql
     CREATE DATABASE fast_cars;
     ```
   - Import schema:
     - Inside MySQL shell (if `schema.sql` is accessible):
       ```sql
       source schema.sql;
       ```
     - **Or from terminal** (not inside MySQL shell):
       ```bash
       mysql -u username -p fast_cars < schema.sql
       ```
       
5. **Configure `main.py` database settings to appropriate username and password**

6. **Run the app:**
   ```bash
   python3 main.py
   ```

   Visit: `http://localhost:5001`

## File Structure

```
fast-cars/
├── images/
├── static/
├── templates/
├── main.py
├── requirements.txt
├── schema.sql
└── README.md
```

## Acknowledgements

- Flask
- MySQL
- XAMPP
- Bootstrap

## Contact Me

Feel free to reach out if you have any questions, suggestions, or feedback.

- Email: sadeeqsas14@gmail.com
- [Twitter](https://twitter.com/sadiq__abubakar)
