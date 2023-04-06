# Please follow the steps below to run the code
Clone the Repo from Git
```sh
$ git clone https://github.com/senganal-ta/app-templates.git
$ cd app-templates
```
Create virtual enviroment using the conda env file
```sh
$ conda env create -n app-templates-venv --file requirements/discount_web_api/env.yml
```

Activate the virtual envrionment
```sh
$ conda activate app-templates-venv
```
Run the Django server
```sh
$ python src/discount_web_api/manage.py runserver
$ cd app-templates
```
# Custom Permissions in Django
Documentation on how to create custom permissions is available in [Custom Permissions](https://testdriven.io/blog/custom-permission-classes-drf/).

This app-template uses Django's built in User model and customizes it. Custom User model is available under src/discount_web_api/apps/scenario_comparision/models.py

Run migrations for the app: scenario_comparision
```sh
$ cd src/discount_web_api/
$ python manage.py makemigrations scenario_comparision
$ python manage.py migrate
```

To run the template, create few user roles and user groups using fixture.
```sh
$ python manage.py loaddata custom_permissions_initial_data_load.json
```
Once data is created, create a superuser using the following command
```sh
$ python manage.py createsuperuser
```
After creating a superuser, start the django server
```sh
$ python manage.py runserver
```
Authorize using the superuser credentials and create more users using APIs available 

