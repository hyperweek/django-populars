from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Popularity(models.Model):
    popularity = models.FloatField(default=0.0)
    content_type = models.ForeignKey(ContentType)
    object_pk = models.PositiveIntegerField('object Id')
    content_object = generic.GenericForeignKey('content_type', 'object_pk')

    class Meta:
        ordering = ('-popularity',)
        unique_together = ('content_type', 'object_pk')

    def set_popularity(self, pub_date, last_viewed_date, now, hits, comments=0, favorites=0, likes=0):
        activ_period = (last_viewed_date - pub_date).days
        inactiv_period = (now - last_viewed_date).days

        self.popularity = (hits + comments * settings.COMMENT_WEIGHT + favorites * settings.FAV_WEIGHT + likes * settings.LIKE_WEIGHT) / float(activ_period + pow(inactiv_period, settings.AGING_DEGREE) + 1)
