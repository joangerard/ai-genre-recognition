from django.contrib import admin
# Import the model we defined in models.py.
from to_do_list.models import ToDo

# Register the ToDo model class to the admin site.
admin.site.register(ToDo)