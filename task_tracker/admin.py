from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(UserManager)
# admin.site.register(AbstractUser)
admin.site.register(User)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Task)
admin.site.register(AssignTask)
