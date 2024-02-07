from django.urls import path, include

urlpatterns = [
    path("tasks/", include('clouderp_tasks.urls')),
]
