## Quick Start

To get this project up and running locally on your computer:
1. Set up the Python development environment, recommend using a Python virtual environment.
1. Assuming you have Python setup, run the following commands (Windows):
   ```
   pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic
   python manage.py test # Run the standard tests. These should all pass.
   python manage.py createsuperuser
   python manage.py runserver
   ```
1. Open a browser to `http://127.0.0.1:8000/admin/` to open the admin site
1. Create a few test objects of each type.
1. Open tab to `http://127.0.0.1:8000` to see the main site, with your new objects.