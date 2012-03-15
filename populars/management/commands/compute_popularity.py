import datetime
from django.core.management.base import NoArgsCommand
from django.contrib.contenttypes.models import ContentType

from populars.models import Popularity

class Command(NoArgsCommand):
    """
    This management command should be setup as a cron job and run daily.
    Updates the popularity of an object.

    Example:

        python manage.py compute_popularity
    """
    help = 'Recomputes the popularity of all objects'

    def handle(self, **options):
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
            print '\nUpdate started at: '+str(now)
            
            #Computing popularity
            update_popularity(counter_queryset, now)

            print "The operation took %s" % get_time_from_seconds((datetime.datetime.now()-now).seconds)
        

def update_popularity(counter_queryset, now):

    for counter_object in counter_queryset:
        if counter_object.content_object:
            popularity, created = Popularity.objects.get_or_create(content_type=counter_object.content_type, object_pk=counter_object.object_pk)

            created_at = counter_object.content_object.created_at
            modified_at = counter_object.content_object.modified_at
            hits = counter_object.content_object.hits
            comments = counter_object.content_object.comments if hasattr(counter_object.content_object, 'comments') else 0
            favorites = counter_object.content_object.favorites if hasattr(counter_object.content_object, 'favorites') else 0
            likes = counter_object.content_object.likes if hasattr(counter_object.content_object, 'likes') else 0

            # Updating Popularity objects
            Popularity.objects.update_popularity(popularity, popularity.get_popularity(created_at, modified_at, now, hits, comments, favorites, likes))


def get_time_from_seconds(seconds):
    hrs = int(seconds/3600)
    mins = int(seconds % 3600)/60
    secs = seconds-mins*60-hrs*3600
    return "%dh:%dm:%ds"%(hrs, mins, secs)