# Student Evaluation System
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Project Overview

The **Student Evaluation System** is a Django-based web application designed for students to check their results and view previous evaluations, while also providing a backend for administrators to manage student data and evaluation results. The system includes role-based access, allowing different functionality for students, admins, and superusers.

## Features

### Student Features:
- **Check Results**: Students can input their ID to view the most recent evaluation result.
- **View Previous Results**: A "Show Previous Results" button allows students to view all their past results.

### Admin Features:
- **Manage Students**: Admins can add, update, and delete student records.
- **Manage Results**: Admins can add, edit, or delete student evaluation results.
- **Dashboard**: Admins have access to a comprehensive dashboard for managing users and results.
- **Excel**: Admins Can upload Excel file contained students and results.

### Superuser Features:
- **Admin Management**: Superusers can create and delete admin accounts.

## Technologies Used

- **Backend**: Django (Python)
- **Database**: PostgreSQL (or SQLite for development)
- **Frontend**: HTML, CSS, JavaScript
- **Version Control**: Git, GitHub
- **Deployment**: Gunicorn, Nginx, PostgreSQL (production setup)

## Installation and Setup

### Requirements
- Python 3.8+
- Django 3.x+
- PostgreSQL (for production, SQLite for development)



### Steps to Set Up Locally

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Osama-elgebaly1/student-evaluation-system.git
   cd student-evaluation-system


### **3. Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4. Apply Migrations**  
```bash
python manage.py migrate
```

### **5. Run the Development Server**  
```bash
python manage.py runserver
```

Now, the project should be running at **http://127.0.0.1:8000/**.  

---
## 💬 Contact

- **Email:** osamaelgebaly122@gmail.com  
- **GitHub:** [Osama Elgebaly](https://github.com/Osama-elgebaly1)
