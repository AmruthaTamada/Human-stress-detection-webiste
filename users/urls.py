from django.urls import path
from .views import signup_view, login_view, logout_view,home_view, stress_predictor_view,main_page

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('stress_predictor/', stress_predictor_view, name='stress_predictor'),
    path('', main_page, name='main_page'),  # Default route to main page
]
