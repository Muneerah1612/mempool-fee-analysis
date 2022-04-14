from django.urls import path
from .views import GetTxDetails, ListFeesView, HighLowFeesView

urlpatterns =[
    path('tx/',GetTxDetails.as_view()),
    path('feeslist/',ListFeesView.as_view()),
    path('feeestimate/',HighLowFeesView.as_view()),
]