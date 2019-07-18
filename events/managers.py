from django.db import models


class ActiveManager(models.Manager):
    def get_queryset(self):
        # Gets Only Active Events
        active_events = super(ActiveManager, self).get_queryset().filter(is_inactive=False)
        return active_events
