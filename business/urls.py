from django.urls import path
from . views import *


urlpatterns = [
    path('kyb/', BusinessKYBView.as_view(), name = 'business-kyb'),

]