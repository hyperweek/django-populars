import datetime
from django.core.management.base import NoArgsCommand

from populars.models import Popularity


class Command(NoArgsCommand):
    help = "Can be run as a cronjob or directly to update popularity on all objects tracked via django-hitcount or django-popularity."

    def handle_noargs(self, **options):
        from django.conf import settings

        counter_queryset = None
        if 'hitcount' in settings.INSTALLED_APPS:
            from hitcount.models import HitCount
            counter_queryset = HitCount.objects.all()

        elif 'popularity' in settings.INSTALLED_APPS:
            from popularity.models import ViewTracker
            counter_queryset = ViewTracker.objects.all()
        else:
            print 'Hitcount or Popularity not installed !'

        if counter_queryset:
            now = datetime.datetime.now()
            print "\nUpdate started at: %s" % str(now)

            #Computing popularity
            nbr_objs = update_popularity(counter_queryset, now)
            print "%d objects updated" % nbr_objs

            time_elapsed = get_time_from_seconds((datetime.datetime.now() - now).seconds)
            print "The operation took %s" % time_elapsed
        else:
            print "0 objects updated"


def update_popularity(counter_queryset, now):

    for counter_object in counter_queryset:
        if counter_object.content_object:
            obj, created = Popularity.objects.get_or_create(content_type=counter_object.content_type, object_pk=counter_object.object_pk)

            created_at = counter_object.content_object.created_at
            modified_at = counter_object.content_object.modified_at
            hits = counter_object.content_object.hits
            comments = getattr(counter_object.content_object, 'comments', 0)
            favorites = getattr(counter_object.content_object, 'favorites', 0)
            likes = getattr(counter_object.content_object, 'likes', 0)

            # Updating Popularity objects
            popularity = obj.get_popularity(created_at, modified_at, now,
                hits, comments, favorites, likes)
            Popularity.objects.update_popularity(obj, popularity)
    return counter_queryset.count()


def get_time_from_seconds(seconds):
    hrs = int(seconds / 3600)
    mins = int(seconds % 3600) / 60
    secs = seconds - mins * 60 - hrs * 3600
    return "%dh:%dm:%ds" % (hrs, mins, secs)
