from django.urls import path 

from . import views

urlpatterns = [
    path('', views.home, name='home.html'),
    path("home",views.home,name ="home"),
    path('leaves/<int:pro>/',views.leaves,name ="leaves"),
    path('application/<int:pro>/',views.application,name ="application"),
    path('application/<int:pro>/application',views.application,name ="application"),
    path('show/<int:pro>/',views.show,name ="show"),
    path('logout/<int:pro>/',views.logout,name ="logout"),
    path('status/<int:pro>/',views.status,name ="status"),
    path('status/<int:pro>/status',views.status,name ="status"),
    path('changecsehod/<int:pro>/',views.changecsehod,name ="changecsehod"),
    path('changecsehod/<int:pro>/changecsehod',views.changecsehod,name ="changecsehod"),
    path('changeeehod/<int:pro>/',views.changeeehod,name ="changeeehod"),
    path('changeeehod/<int:pro>/changeeehod',views.changeeehod,name ="changeeehod"),
    path('changemechod/<int:pro>/',views.changemechod,name ="changemechod"),
    path('changemechod/<int:pro>/changemechod',views.changemechod,name ="changemechod"),
    path('changedean/<int:pro>/',views.changedean,name ="changedean"),
    path('changedean/<int:pro>/changedean',views.changedean,name ="changedean"),
   
]