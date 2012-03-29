import datetime
from django.core.management.base import NoArgsCommand, CommandError


class Command(NoArgsCommand):
    help = "Can be run as a cronjob or directly to update popularity on all objects tracked via django-hitcount or django-popularity."

    def handle_noargs(self, **options):
        from django.conf import settings
        from populars.models import Popularity

        verbosity = int(options.get('verbosity', 1))

        if 'hitcount' in settings.INSTALLED_APPS:
            from hitcount.models import HitCount
            queryset = HitCount.objects.all()
        elif 'popularity' in settings.INSTALLED_APPS:
            from popularity.models import ViewTracker
            queryset = ViewTracker.objects.all()
        else:
            raise CommandError("django-hitcount or django-popularity should be installed first.")

        for track in queryset:
            obj = track.content_object
            popular, created = Popularity.objects.get_or_create(
                content_type=track.content_type,
                object_pk=track.object_pk
            )

            created_at = obj.created_at
            modified_at = obj.modified_at
            hits = obj.hits
            comments = getattr(obj, 'comments', 0)
            favorites = getattr(obj, 'favorites', 0)
            likes = getattr(obj, 'likes', 0)

            popular.set_popularity(created_at, modified_at,
                datetime.datetime.now(), hits, comments, favorites, likes)
            popular.save()

        if verbosity:
            print "%d objects updated" % queryset.count()
