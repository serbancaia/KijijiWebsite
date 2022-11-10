from django.urls import path
from . import views

#urls for blog
app_name = "blog"
urlpatterns = [
	path('<int:pk>/', views.BlogView.as_view(), name="blog"),
	path('<int:blog_id>/add-entry/', views.AddEntryView, name="add-entry"),
]
