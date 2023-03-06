from ckeditor.fields import RichTextField
from django.db import models

from django.utils.translation import gettext as _

import json

from apps.common.models import BaseModel, PersonBase


class Donations(BaseModel):
    summa = models.PositiveIntegerField()
    fullname = models.CharField(verbose_name=_('Full name'), max_length=255)
    bill_number = models.IntegerField()
    payment_gateway_id = models.IntegerField()  # check number
    payed_at = models.DateTimeField()
    status_id = models.BooleanField(help_text="True for payed, False for not payed status")  # checking the status (payed or not) T/F
    description = models.TextField()  # primicheniya reason of payment

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'


class Rasxod(BaseModel):
    summa = models.PositiveIntegerField()
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.summa

    class Meta:
        verbose_name = "Rasxod"
        verbose_name_plural = "Rasxodlar"


class EventCategory(BaseModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "EventCategory"
        verbose_name_plural = "EventCategories"


class Event(BaseModel):
    title = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    location = models.CharField(max_length=50)
    poster_path = models.ImageField(upload_to="photos/event%Y/%m/%d/")
    event_category_id = models.ForeignKey(EventCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"


class NewsCategory(BaseModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Country(BaseModel):
    name = models.CharField(max_length=100)
    flag_poster_path = models.ImageField(upload_to="photos/flags%Y/%m/%d/")

    def __str__(self):
        return self.name


class Hashtag(BaseModel):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class News(BaseModel):
    title = models.CharField(max_length=255)
    poster_path = models.ImageField(upload_to="photos/news%Y/%m/%d/")
    news_category_id = models.ForeignKey(NewsCategory, on_delete=models.CASCADE)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    full_text = RichTextField()
    view_counts = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class NewsHashtagRelation(BaseModel):
    hashtagid = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
    news_id = models.ForeignKey(News, on_delete=models.CASCADE)


class MapPoint(PersonBase):
    city_name = models.CharField(max_length=100)
    country_name = models.CharField(max_length=100)
    longitude = models.DecimalField(verbose_name=_('Longitude'), max_digits=9, decimal_places=6)
    latitude = models.DecimalField(verbose_name=_('Latitude'), max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Map Point"
        verbose_name_plural = "Map Points"


class UsefulLink(BaseModel):
    logo_poster_path = models.ImageField(upload_to="photos/logo%Y/%m/%d/", blank=True)
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Useful Link"
        verbose_name_plural = "Useful Links"


class FollowUsPost(BaseModel):  # using selenium scrapper (optional)
    poster_path = models.ImageField(upload_to="photos/post%Y%m%d/")
    url = models.CharField(max_length=100)


class Chairman(PersonBase):
    avatar_original = models.ImageField(upload_to="photos/avatar%Y%m%d/", blank=True )
    avatar_compressed = models.ImageField(upload_to="photos/avatar%Y%m%d/", blank=True)
    year = models.CharField(max_length=4, blank=True)
    reception_days = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Chairman"
        verbose_name_plural = "Chairmen"


class Task(BaseModel):  # zadachi
    text = RichTextField()

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class Representative(PersonBase):
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    avatar_original = models.ImageField(upload_to="photos/avatar%Y%m%d/")
    avatar_compressed = models.ImageField(upload_to="photos/avatar%Y%m%d/")
    task = RichTextField()  # Main Task of Board section
    longitude = models.DecimalField(verbose_name=_('Longitude'), max_digits=9, decimal_places=6)
    latitude = models.DecimalField(verbose_name=_('Latitude'), max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Representative"
        verbose_name_plural = "Representatives"


class Vacancy(BaseModel):
    icon = models.ImageField(upload_to="photos/icon%Y%m%d/")
    position_title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    short_text = models.CharField(max_length=255)
    full_text = RichTextField()
    min_salary = models.PositiveIntegerField()
    max_salary = models.PositiveIntegerField()
    work_type = models.CharField(max_length=20, help_text="enter a type of work part-time(0.5) or full_time")  # also we can use choices: 0.5, full stavka
    view_counts = models.PositiveIntegerField()

    def __str__(self):
        return self.position_title

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"


class Resume(PersonBase):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    file_path = models.FileField()  # we can also use FilePath for certain reasons
    # ip=models.IPAddressField()  we can use this two fields for security reasons
    # user_agent=models.TextField()    ex: sql injections
    type_id = models.CharField(max_length=1, help_text="enter a type 1 --> for employees 2 --> for volunteers")  # (1) --> employees  2--> for volunteers

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Resume"
        verbose_name_plural = "Resumes"


class ScheduledEventCategory(BaseModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class ScheduledEvent(BaseModel):
    poster_path = models.ImageField(upload_to="photos/event%Y%m%d/")
    title = models.CharField(max_length=200)
    scheduled_time = models.DateTimeField()
    address = models.CharField(max_length=100)
    full_text = RichTextField()
    view_counts = models.PositiveIntegerField()
    scheduled_e_category_id = models.ForeignKey(ScheduledEventCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Scheduled Event"
        verbose_name_plural = "Scheduled Events"


class Feedback(PersonBase):  # obratnaya svyaz section
    text = RichTextField()

    # ip=models.IPAddressField()   for security reason (optional)
    # useragent=models.TextField()  for security reason (optional)
    # viewed=models.BooleanField() :: optional fields
    # flag=models.BooleanField()   :: for marking ex: liked or starred

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"


class Question(PersonBase):  # question form
    question = RichTextField()

    # ip=models.IPAddressField()
    # useragent=models.TextField()
    # viewed=models.BooleanField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Faq(BaseModel):
    question = RichTextField()
    answer = RichTextField()
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    hashtag = models.ManyToManyField(Hashtag)


class Service(BaseModel):  # uslugi section
    title = models.CharField(max_length=50)
    url = models.URLField()
    icon = models.ImageField(upload_to="photos/icon%Y%m%d/")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"


class Gallery(BaseModel):
    photo_original = models.ImageField(upload_to="photos/post%Y%m%d/")
    photo_compressed = models.ImageField(upload_to="photos/post%Y%m%d/")
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)


class MigrationLaw(BaseModel):  # migratsionnoe  zakonodatelstvo
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    file = models.FileField()


class Consul(PersonBase):
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Consul"
        verbose_name_plural = "Consuls"


class Volunteer(PersonBase):
    pass

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Volunteer"
        verbose_name_plural = "Volunteers"


class Book(BaseModel):
    title=models.CharField(max_length=100)
    photo = models.ImageField(upload_to="photos/book%Y%m%d/")
    author = models.CharField(max_length=50)
    published_year = models.CharField(max_length=4, blank=True)
    page_number = models.CharField(max_length=5)
    description = RichTextField()
    file = models.FileField(upload_to="files/book%Y%m%d", blank=True)

    def __str__(self):
        return self.title


class Language(BaseModel):
    name = models.CharField(max_length=5)  # ex: uz, ru, eng

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"


class LawOfCountry(BaseModel):
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    full_text = RichTextField()
    view_counts = models.PositiveIntegerField()


class University(BaseModel):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)

    def __str__(self):
        return self.name_en

    class Meta:
        verbose_name = "University"
        verbose_name_plural = "Universities"


class Faculty(BaseModel):
    name = models.CharField(max_length=100)
    univer_id = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Faculty"
        verbose_name_plural = "Faculties"


class Region(BaseModel):
    name = models.CharField(max_length=100)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"


class Intern(PersonBase):
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    birth_date = models.DateField()
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE)
    sphere = models.CharField(max_length=50, blank=True)  # sfera deyatelnosti
    intern_start_date = models.DateField()
    univer_id = models.ForeignKey(University, on_delete=models.CASCADE, blank=True)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE, blank=True)
    begin_date = models.DateField()
    finish_date = models.DateField()
    average_score = models.CharField(max_length=3, blank=True)
    work_experience = models.TextField(blank=True)
    key_skills = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to="files/resume%Y%m%d/", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Intern"
        verbose_name_plural = "Intern"


class InstagramPost(BaseModel):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="photos/instaimage%Y%m%d/")
    url_address = models.URLField(blank=True)

    def __str__(self):
        return f"Instagram Post: {self.title}"


    @property
    def get_url(self):
        with open('links.json') as f:
            data = json.load(f)

            for url in data:
                return InstagramPost.objects.create(url_address=url)


"""
    representator
    chairman
    consuls
    map_points shu to'rtalasi aslida bitta narsami?
    
    events bilan scheduled_events aslida bitta narsami?
    
    gallery uslugiga bog'langanmi?
    
    stajirovka faqat uzb uchunmi?
"""
