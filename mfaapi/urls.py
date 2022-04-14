from django.urls import path
from .views import GetTxDetails

urlpatterns =[
    path('tx/',GetTxDetails.as_view()),
]