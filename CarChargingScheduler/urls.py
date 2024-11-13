"""
URL configuration for CarChargingScheduler project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from CarChargingScheduler.views import ChargingSchedule, ChargingSlotView, CarView, PauseChargingScheduleView, \
    OverrideChargingScheduleView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('car/<uuid:ae_id>', CarView.as_view(), name='charging_schedule'),
    path('car/<uuid:ae_id>/charging_schedule/', ChargingSchedule.as_view(), name='charging_schedule'),
    path('car/<uuid:ae_id>/charging_schedule/<uuid:ae_id>', ChargingSlotView.as_view(), name='charging_slots'),
    path('car/<uuid:ae_id>/charging_schedule/override', ChargingSchedule.as_view(), name='override_charging_schedule'),
    path('car/<uuid:ae_id>/charging_schedule/pause', PauseChargingScheduleView.as_view(), name='pause_charging_schedule'),
    path('car/<uuid:ae_id>/charging_schedule/<uuid:ae_id>/charging_slots', OverrideChargingScheduleView.as_view(),
         name='charging_schedule')

]