

Create the following properties in each model class to track::

    @property
    def created_at(self):
        return self.pub_date

    @property
    def modified_at(self):
        return HitCount.objects.get(content_type=ContentType.objects.get_for_model(self), object_pk=self.id).modified

    @property
    def hits(self):
        return HitCount.objects.get(content_type=ContentType.objects.get_for_model(self), object_pk=self.id).hits

    @property
    def comments(self):
        return self._get_num_comments()

    @property
    def favs(self):
        return self._get_num_favs()

    @property
    def likes(self):
        return 0


Put these lines in your settings::

    COMMENT_WEIGHT  = 2
    LIKE_WEIGHT     = 3
    FAV_WEIGHT      = 4

    AGING_DEGREE    = 2


Create the following signal in each model class to track::

    def photo_popularity_delete(sender, instance, *args, **kwargs):
        ctype = ContentType.objects.get_for_model(instance)
        try:
            Popularity.objects.filter(content_type=ctype, object_pk=instance.id).delete()
        except Popularity.DoesNotExist:
            pass

    signals.pre_delete.connect(photo_popularity_delete, sender=Photo, dispatch_uid="delete-photo-hitcount")
