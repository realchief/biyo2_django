from django.db import models


class Display(models.Model):
    name = models.CharField(max_length=128)
    background_color = models.CharField(max_length=7)

    def __unicode__(self):
        return u'Display # %s' % self.id


class Page(models.Model):
    name = models.CharField(max_length=128)
    display = models.ForeignKey(Display, related_name='pages')


ELEMENT_TYPES = (
    (1, 'IMAGE'),
    (2, 'CATEGORY'),
    (3, 'PRODUCT'),
    (4, 'TWITTER'),
    (5, 'INSTAGRAM'),
    (6, 'FACEBOOK'),
    (7, 'FOURSQUARE'),
    (8, 'YELP'),
    (9, 'IMAGES'),
    (10, 'WEATHER'),
)


class Element(models.Model):
    type = models.IntegerField(choices=ELEMENT_TYPES)
    value = models.CharField(max_length=128)
    archived = models.BooleanField(default=False)

    def __unicode__(self):
        return u'element #%s' % self.id


class Box(models.Model):
    element = models.OneToOneField(Element, null=True, blank=True)
    display = models.ForeignKey(Display, related_name='boxes')
    row = models.IntegerField()
    col = models.IntegerField()
    size_x = models.IntegerField()
    size_y = models.IntegerField()
    background_color = models.CharField(max_length=7)
    archived = models.BooleanField(default=False)

    def __unicode__(self):
        return u'Box #%s' % self.id


class Picture(models.Model):
    """This is a small demo using just two fields. The slug field is really not
    necessary, but makes the code simpler. ImageField depends on PIL or
    pillow (where Pillow is easily installable in a virtualenv. If you have
    problems installing pillow, use a more generic FileField instead.

    """
    file = models.ImageField(upload_to="pictures")
    slug = models.SlugField(max_length=50, blank=True)
    box = models.ForeignKey(Box, blank=True, null=True, related_name='box_images')

    def __unicode__(self):
        return u'%s' % self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new',)

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.file.delete(False)
        super(Picture, self).delete(*args, **kwargs)
