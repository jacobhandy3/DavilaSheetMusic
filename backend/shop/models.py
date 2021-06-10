from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

class Genre(models.Model):
    name = models.CharField(max_length=50,db_index=True)
    slug = models.SlugField(max_length=75,unique=True,blank=True)

    def save(self,*args,**kwargs):
        """
        Before saving a new instance of the model,
        set the slug to a slugified version of the title
        """
        self.slug = slugify(self.name)
        super(Genre,self).save(*args,**kwargs)
    
    def __str__(self) -> str:
        return "%s" % self.name
    
    class Meta:
        #specify model field to order by
        ordering = ["name"]
        #set default name of object
        def __unicode__(self):
            return u"%s" % self.name

class Instrument(models.Model):
    name = models.CharField(max_length=50,db_index=True)
    slug = models.SlugField(max_length=75,unique=True,blank=True)

    def save(self,*args,**kwargs):
        """
        Before saving a new instance of the model,
        set the slug to a slugified version of the name
        """
        self.slug = slugify(self.name)
        super(Instrument,self).save(*args,**kwargs)

    def __str__(self) -> str:
        return "%s" % self.name
    
    class Meta:
        #specify model field to order by
        ordering = ["name"]
        #set default name of object
        def __unicode__(self):
            return u"%s" % self.name

class Format(models.Model):
    name = models.CharField(max_length=50,db_index=True)
    slug = models.SlugField(max_length=75,unique=True,blank=True)

    def save(self,*args,**kwargs):
        """
        Before saving a new instance of the model,
        set the slug to a slugified version of the name
        """
        self.slug = slugify(self.name)
        super(Format,self).save(*args,**kwargs)

    def __str__(self) -> str:
        return "%s" % self.name
    
    class Meta:
        #specify model field to order by
        ordering = ["name"]
        #set default name of object
        def __unicode__(self):
            return u"%s" % self.name

# Create your models here.
class SheetMusic(models.Model):

    #3 levels of difficulty for the music piece
    levels = [(1,"Beginner"),(2,"Early Intermediate"),(3,"Intermediate"),(4,"Advanced Intermediate"),(5,"Advanced")]

    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    instrument = models.ManyToManyField(Instrument)
    format = models.ManyToManyField(Format)
    level = models.IntegerField(choices=levels,default=1)
    genre = models.ManyToManyField(Genre)
    description = models.TextField()
    cost = models.DecimalField(max_digits=6,decimal_places=2,validators=[MinValueValidator(limit_value=0,message="Cannot input cost amount lower than $0!")])
    date_added = models.DateTimeField(auto_now_add=True)
    original = models.BooleanField(default=False)
    visible = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200,unique=True,blank=True)
    fpath = models.URLField(verbose_name="file path",blank=True,null=True)
    img_path = models.URLField(verbose_name="image path",blank=True,null=True)
    
    def listLevels(self):
        """Returns the whole list of tuples containing an integer and the human readable name associated with the integer"""
        return self.levels
    def describeLevel(self):
        """Returns the human readable name of the integer assigned to level"""
        return self.levels[self.level-1][1]
    def describeOriginal(self):
        """Returns 'Original' or 'Arrangement' depending on whether visible is true or false"""
        return "Original" if self.original == True else "Arrangement"
    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse("sheetmusic-detail", args=[self.slug])

    def save(self,*args,**kwargs):
        """
        Before saving a new instance of the model,
        set the slug to a slugified version of the title
        """
        self.slug = slugify(self.title)
        super(SheetMusic,self).save(*args,**kwargs)

    def __str__(self) -> str:
        return "%s (%s)" % (self.title,self.format)
    class Meta:
        #specify model field to order by
        ordering = ["title"]
        db_table = "sheet music"
        verbose_name_plural = "Sheet Music"
        #set default name of object
        def __unicode__(self):
            return u"%s" % self.slug

class ProductResources(models.Model):
    product = models.ForeignKey(SheetMusic,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    link = models.URLField()

    def __str__(self) -> str:
        return "%s" % self.link
    class Meta:
        #specify model field to order by
        ordering = ["product","name"]
        db_table = "product resource"
        verbose_name_plural = "Product Resources"
        #set default name of object
        def __unicode__(self):
            return u"%s" % self.link