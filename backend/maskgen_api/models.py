from django.db import models

class Instrument(models.TextChoices):
    IMACS_F4 = 'IMACS f/4'
    IMACS_F2 = 'IMACS f/2'

class Status(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    FINALIZED = 'finalized', 'Finalized (sent to be cut)'
    COMPLETED = 'completed', 'Completed (mask has been cut successfully)'
# Models
# add more info later 
class Filter(models.Model):
    name = models.CharField(max_length=50)
 
    def __str__(self):
        return self.name


class Disperser(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class InstrumentConfig(models.Model):
    instrument = models.CharField(max_length=20, choices=Instrument.choices)
    version = models.CharField(max_length=50)
    available_filters = models.ManyToManyField(Filter, blank=True)
    available_dispersers = models.ManyToManyField(Disperser, blank=True)

    def __str__(self):
        return f"{self.instrument} v{self.version}"

class Mask(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    status = models.CharField(
        max_length=100,
        choices=Status.choices,
        default=Status.DRAFT
    )
    features = models.JSONField() # slits and holes
    objects_list = models.ManyToManyField('Object', blank=True, related_name='objs_on_mask') # guide and alignment stars
    excluded_obj_list = models.ManyToManyField('Object', blank=True, related_name='objs_not_on_mask') # objs left out of the mask
    instrument_config = models.ForeignKey('InstrumentConfig', on_delete=models.SET_NULL, null=True)
    instrument_setup = models.JSONField()

    def __str__(self):
        return f"Mask {self.name}"  
    
      
class Object(models.Model):
    TYPE_CHOICES = [
        ('GUIDE', 'Guider'),
        ('ALIGN', 'Alignment'),
        ('TARGET', 'Target'),
    ]

    name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    right_ascension = models.FloatField()
    declination = models.FloatField()
    priority = models.IntegerField(default=0.0)
    aux = models.JSONField(null=True) # a_len, b_len

    def __str__(self):
        return f"{self.type} Object {self.name}"

# object list: user_id, name, id, objects
class ObjectList(models.Model):
    user_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    objects_list = models.ManyToManyField('Object', blank=True)
    class Meta:
        unique_together = ("name", "user_id") 