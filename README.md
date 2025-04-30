# **Student Results Management System**

## **Description**  
This project is a web-based **Student Results Management System** designed to manage students, their results, and provide an interface for both admins and students. Admins can add, view, and manage student information and their academic results, while students can check their results through a secure interface. The application includes a login system for administrators and a results-checking functionality for students. It is built using Django and SQLite for a lightweight and efficient setup.

---

## **Features**  

- **Admin Dashboard** – Secure interface for administrators to manage students and results.
- **Add & Manage Students** – Admins can add, update, and delete student records.
- **Add & Manage Results** – Admins can add and update students' academic results.
- **Secure Login System** – Admins must log in to access the admin dashboard.
- **Student Results Checking** – Students can check their academic results securely by providing their student ID.

---

## **Tech Stack**  

- **Backend:** Django (Python)  
- **Database:** SQLite3 (for development)  


---


### **1. Set Up a Virtual Environment**  
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **2. Clone the Repository**  
```bash
git clone https://github.com/Osama-elgebaly/Students_Evaluation_System
cd Students_Evaluation_System

```

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
