from django.db import models


class EventLink(models.Model):
    title = models.CharField(max_length=100)
    google_calendar_link = models.URLField()
    icalendar = models.FileField(upload_to='calendars/')

    def __str__(self):
        return self.title
