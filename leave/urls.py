from django.urls import path
from . import views

urlpatterns = [
    path('hostel_leave/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('rector_dashboard/', views.rector_dashboard, name='rector_dashboard'),
    path('apply_leave/', views.apply_leave, name='apply_leave'),
    path('logout/', views.logout_view, name='logout'),
    path('approve_leave/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('reject_leave/<int:leave_id>/', views.reject_leave, name='reject_leave'),
]
