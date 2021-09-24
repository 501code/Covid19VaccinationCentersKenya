from django.db import models
from django_extensions.db.models import TimeStampedModel
from djchoices import DjangoChoices, ChoiceItem
from location_field.models.plain import PlainLocationField


class County(TimeStampedModel):
    name = models.CharField(max_length=555, blank=False, null=False)
    location = PlainLocationField(based_fields=['city'], zoom=7)

    class Meta:
        verbose_name_plural = "counties"

    def __str__(self):
        return self.name


class SubCounty(TimeStampedModel):
    name = models.CharField(max_length=555, blank=False, null=False)
    county = models.ForeignKey(County, blank=False, null=False, on_delete=models.CASCADE)
    location = PlainLocationField(based_fields=['city'], zoom=7)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "sub-counties"


class VaccineCenter(TimeStampedModel):
    class Ownerships(DjangoChoices):
        PRIVATE = ChoiceItem("private", "Private")
        PUBLIC = ChoiceItem("public", "Public")
        MILLITARY = ChoiceItem("millitary", "Millitary")
        FBO = ChoiceItem("fbo", "FBO")
        NGO = ChoiceItem("ngo", "NGO")
        ARMED_FORCES = ChoiceItem("armed_forces", "Armed Forces")
    name = models.CharField(max_length=555, blank=False, null=False)
    sub_county = models.ForeignKey(SubCounty, blank=True, null=True, on_delete=models.CASCADE)
    mfl = models.CharField(max_length=255, blank=True, null=True)
    ownership = models.CharField(choices=Ownerships.choices, default=Ownerships.PUBLIC,
                                 max_length=50, blank=True, null=True)
    location = PlainLocationField(based_fields=['city'], zoom=7, blank=True, null=True)

    class Meta:
        verbose_name_plural = "vaccine centers"

    def __str__(self):
        return self.name


class VaccineCenterFeedback(TimeStampedModel):
    vaccine_center = models.ForeignKey(VaccineCenter, blank=False, null=False,
                                       on_delete=models.CASCADE)
    additional_info = models.TextField(blank=True, null=True)
    waiting_time = models.IntegerField(default=1)
    vaccine_available = models.BooleanField(default=True)
    vaccines = models.CharField(max_length=255, null=True, blank=True)
