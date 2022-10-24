from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('employee/<str:pk>', views.employee_info, name='employee'),
    path('create-project/', views.create_project, name='create-project'),
    path('delete-project/<str:pk>', views.delete_project, name='delete-project'),
    path('update-project/<str:pk>', views.update_project, name='update-project'),
    path('create-task/<str:pk>', views.create_task, name='create-task'),
    path('update-task/<str:pk>', views.update_task, name='update-task'),
    path('delete-task/<str:pk>', views.delete_task, name='delete-task'),

    path('', views.home, name='home'),
    path('project/<str:pk>/', views.project, name='project'),
    path('myprojects/', views.ProjectsByUserListView.as_view(), name='my-projects'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="base/password_reset_form.html"),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="base/password_reset_done.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="base/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="base/password_reset_complete.html"),
         name='password_reset_complete'),
]
