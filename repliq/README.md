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


Quick Start
```
git clone https://github.com/rabbi54/Repliq.git
cd Repliq
python -m venv venv
pip install -r requirements.txt
python manage.py runserver
```
