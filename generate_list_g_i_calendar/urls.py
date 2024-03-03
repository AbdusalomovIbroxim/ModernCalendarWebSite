from django.urls import path
from .views import EventLinkGenerator, download_icalendar

urlpatterns = [
    path('', EventLinkGenerator.as_view(), name='index'),
    path('save-links/', EventLinkGenerator.as_view(), name='save_links'),
    path('download-icalendar/<int:event_id>/', download_icalendar, name='download_icalendar'),
]
