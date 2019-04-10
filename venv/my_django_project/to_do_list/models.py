from django.db import models

# Create your models here.
class ToDo(models.Model):

    # Maps to to_do_things table column.
    to_do_things = models.CharField(max_length=1000)

    # Maps to create_date table column.
    create_date = models.DateTimeField(auto_now_add=True)

    # Maps to handle_date table column.
    handle_date = models.DateTimeField()

    def __str__(self):
        ''' Return this model string value. '''
        return self.to_do_things