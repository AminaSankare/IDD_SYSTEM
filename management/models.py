from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

# Create your models here.


class Citizen(models.Model):
    class Gender(models.TextChoices):
        SELECT = "", "Select Gender"
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"

    class Marital(models.TextChoices):
        SELECT = "", "Select Marital"
        SINGLE = "Single", "Single"
        MARRIED = "Married", "Married"
        DIVORCED = "Divorced", "Divorced"
        SEPARATED = "Separated", "Separated"
        WIDOWED = "Widowed", "Widowed"

    first_name = models.CharField(
        verbose_name="First Name", max_length=50, blank=False)
    last_name = models.CharField(
        verbose_name="Last Name", max_length=50, blank=False)
    gender = models.CharField(
        verbose_name="Gender", choices=Gender.choices, default=Gender.SELECT, max_length=10)
    birthdate = models.DateField(verbose_name="Birthdate", blank=False)
    birth_place = models.CharField(verbose_name="Birth place", max_length=100)
    marital_status = models.CharField(
        verbose_name="Marital Status", choices=Marital.choices, default=Marital.SELECT, max_length=20)
    nationality = models.CharField(verbose_name="Nationality", max_length=50)
    nid_number = models.CharField(
        verbose_name="National ID Number", max_length=50, unique=True, blank=False)
    createdDate = models.DateField(
        verbose_name="Created Date", auto_now_add=True)

    def image(self):
        return mark_safe('<img src="/../../media/%s" width="70" />' % (self.picture))

    image.allow_tags = True

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class CitizenAddress(models.Model):
    citizen = models.OneToOneField(
        Citizen, verbose_name="Citizen", related_name="address", on_delete=models.CASCADE)
    province = models.CharField(
        verbose_name="Province", max_length=50, blank=True)
    state = models.CharField(verbose_name="State", max_length=50, blank=True)
    city = models.CharField(verbose_name="City", max_length=50, blank=True)
    street = models.CharField(verbose_name="Street", max_length=50, blank=True)

    def __str__(self):
        return "{} {}".format(self.citizen.first_name, self.citizen.last_name)


class CitizenParent(models.Model):
    class Parent(models.TextChoices):
        SELECT = "", "Select Parent"
        FATHER = "Father", "Father"
        MOTHER = "Mother", "Mother"

    citizen = models.ForeignKey(
        Citizen, verbose_name="Citizen", related_name="parents", on_delete=models.CASCADE)
    parent = models.CharField(
        verbose_name="Parent", choices=Parent.choices, default=Parent.SELECT, max_length=10)
    first_name = models.CharField(
        verbose_name="First Name", max_length=50, blank=True)
    last_name = models.CharField(
        verbose_name="Last Name", max_length=50, blank=True)
    professionalism = models.CharField(
        verbose_name="Professionalism", max_length=50, blank=True)

    def __str__(self):
        return "{} {}".format(self.citizen.first_name, self.citizen.last_name)


class CitizenDocument(models.Model):
    class DocumentType(models.TextChoices):
        SELECT = "", "Select Document"
        PASSPORT = "Passport", "Passport"
        IDD = "Individual Descriptive Document", "Individual Descriptive Document"

    citizen = models.ForeignKey(
        Citizen, verbose_name="Citizen", related_name="documents", on_delete=models.CASCADE)
    document = models.CharField(
        verbose_name="Document", choices=DocumentType.choices, default=DocumentType.SELECT, max_length=50)
    file = models.FileField(
        verbose_name="Document",
        upload_to="citizens/documents/",
        validators=[FileExtensionValidator(['pdf'])],
        blank=True, null=True
    )
    createdDate = models.DateTimeField(
        verbose_name="Created Date", auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.citizen.first_name, self.citizen.last_name)


class Service(models.Model):
    class ServiceType(models.TextChoices):
        SELECT = "", "Select Service"
        PASSPORT_APPLICATION = "e-Passport Application", "e-Passport Application"
        IDD_APPLICATION = "Individual Descriptive Document Application", "Individual Descriptive Document Application"

    name = models.CharField(
        verbose_name="Service Name", choices=ServiceType.choices, default=ServiceType.SELECT, max_length=100, unique=True, blank=False, null=False)
    description = models.TextField(
        verbose_name="Description", blank=False, null=False)
    processingTime = models.CharField(
        verbose_name="Processing Time", max_length=50, blank=False, null=False)
    fees = models.CharField(verbose_name="Fees",
                            max_length=100, blank=False, null=False)

    def __str__(self):
        return "{}".format(self.name)


class Application(models.Model):
    class DocumentCategory(models.TextChoices):
        SELECT = "", "Select Document Category"
        NONE = "None", "None"
        ORDINARY = "Ordinary Passport", "Ordinary Passport"
        DIPLOMATIC = "Diplomatic Passport", "Diplomatic Passport"
        SERVICE = "Service Passport", "Service Passport"

    citizen = models.ForeignKey(Citizen, verbose_name="Citizen",
                                related_name="applications", on_delete=models.CASCADE)
    current_phone = PhoneNumberField(verbose_name="Phone Number", blank=True)
    email = models.EmailField(verbose_name="Email",
                              max_length=255, unique=True, blank=False)
    service = models.ForeignKey(
        Service, verbose_name="Service", on_delete=models.CASCADE)
    documentCategories = models.CharField(verbose_name="Document Category", choices=DocumentCategory.choices,
                                          default=DocumentCategory.SELECT, max_length=50, blank=True, null=True)
    picture = models.ImageField(
        verbose_name="Image",
        upload_to="application/images/",
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        blank=True, null=True
    )
    status = models.BooleanField(
        verbose_name="Status", default=False, blank=True)
    createdDate = models.DateTimeField(
        verbose_name="Created Date", auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.citizen.first_name, self.citizen.last_name)
