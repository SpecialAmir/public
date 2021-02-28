from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignupView.as_view(),name='signup'),
    path('',views.IndexView.as_view(),name='home'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('signup/<uuid:token>/', views.SignupView2.as_view(), name='signup2'),
    


]