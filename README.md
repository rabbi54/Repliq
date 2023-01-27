# Repliq Asset Management 

This application is build using django framework. The goal of this project is to build a platform for several companies to manage asset (like phones, laptops, tablets and other gears) allocation to their employees.


## Components:
---
1. custom_user
2. asset

### Custom_user
1. This component provides **Views and API views** for user authentication, login.
2. Employee, Company Model
3. Some test cases


### Asset
1. This component provides **views and api views** for all the features. 
    * List of assets
    * List of employee
    * List of Loans
    * Assign Loans to employee
    * Return Loans
2. This componet contains all the related models like (Brand, Asset, AssetLoanSession)
3. Some test cases


To run the project, clone the repository to your local machine or in the cloud:

1. Create a virtual environment
2. Install required modules using pip
3. Log in with credentials 

**You can both use postman and template to test the application**

> As I provided database with the project. No need to set up for database. And you also get credentials of existing users.

**Company owner credentials**
> email : admin@acompany.com
> password : 123456

**Super admin credentials**
> email : admin@admin.com
> password : 123456



You can register as a new user but need to give access for company-admin from django-admin
You can add employee from already existing users.


## Quick Start
```
git clone https://github.com/rabbi54/Repliq.git
cd Repliq
python -m venv venv
pip install -r requirements.txt
python manage.py runserver
```


## Operations
Assuming you are running the application in local machine to port 8000

### Adding a new company
1. Log in to the admin panel http://127.0.0.1:8000/admin/ using the credentials provided of Super admin
2. Add new company

### Adding company admin to company
1. Register a new user for admin of that company http://127.0.0.1:8000/auth/user-register/
2. Add employee account for that new user **tick is_company_admin**.
3. Now that employee is admin of that company
4. User can log in to the system http://127.0.0.1:8000/auth/user-login

### Adding new employee to the company
1. Register new user from http://127.0.0.1:8000/auth/user-register/
2. New admin can select them as employee of the company http://127.0.0.1:8000/auth/add-employee/

### Adding new asset
1. Use the form provided here http://127.0.0.1:8000/

### Assign asset to employee
1. Use the form provided here http://127.0.0.1:8000/assign-asset/

### Show all the loans
1. Use this url http://127.0.0.1:8000/show-loans/

### Return an asset
1. Click the button named "Return Now" here http://127.0.0.1:8000/show-loans/
