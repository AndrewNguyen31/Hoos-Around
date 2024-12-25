from django.contrib import admin
from .models import User, Task, Place, Picture

# Register your models here.
admin.site.register(User)
admin.site.register(Task)
admin.site.register(Place)

admin.site.register(Picture)

admin.site.site_header = "Hoos Around Admin"
admin.site.index_title = "Welcome to Hoos Around Portal"