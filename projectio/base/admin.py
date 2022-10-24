from django.contrib import admin
from .models import Project, Client, Employee, Task, Invoice


class TaskAdminInline(admin.TabularInline):
    model = Task


class ProjectAdmin(admin.ModelAdmin):
    inlines = (TaskAdminInline,)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(Invoice)
