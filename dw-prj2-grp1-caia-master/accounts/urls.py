from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
	path('signup/', views.signUpPage, name="signup"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),
	path('account/', views.accountManagementPage, name="account"),
	path('account/change-password', views.changePassword, name="change-password"),
	path('account/items', views.AccountItemListView.as_view(), name="account-item-list"), 
]
