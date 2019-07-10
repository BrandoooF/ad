from django.db import models


class EventsManager(models.Manager):
    def get_queryset(self):
        # Gets Only Active Events
        active_events = super(EventsManager, self).get_queryset().filter(is_inactive=False)
        return active_events
