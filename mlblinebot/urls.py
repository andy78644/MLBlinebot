from django.urls import path
from . import views
urlpatterns = [
    path('callback', views.callback),
    path('webhook', views.webhook_handler),
    
    #path('fsm/',include('fsm.')),
]
