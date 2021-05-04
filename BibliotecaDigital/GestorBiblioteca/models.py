from django.db import models
from django.core.files.storage import FileSystemStorage
from django.db import models

#fp=FileSystemStorage(location='media/PORTADA_LIBRO')
#fl=FileSystemStorage(location='/media/LIBROS')
# Create your models here.


    

class Genero(models.Model):

    """
    Modelo que representa un género literario (p. ej. ciencia ficción, poesía, etc.).
    """
    nombre= models.CharField( help_text="ingres el gènero(ejp:ciencia,poecia)" ,max_length=50)
    
    
    def __unique__(self):
        return self.nombre

    def __str__(self):
        return self.nombre
    

    
class Subgenero(models.Model):

    nombre= models.CharField(help_text="especifique el area en la que se enfoca(ejp:programacion,matematicas)" ,max_length=50)
    genero=models.ForeignKey('Genero',on_delete=models.SET_NULL,null=True)

    def __unique__(self):
        return self.nombre
        
    def __str__(self):
        return self.nombre
    
    
class Tema(models.Model):
    tema= models.CharField( help_text="ingres el tema que trata (ejp:pogramacion enjava, calculo)" ,max_length=50)
    subgenero= models.ForeignKey('Subgenero', on_delete=models.SET_NULL,null=True)#relacion de mucho a muchos
    
    def display_tema(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ tema.tema for tema in self.tema.all()[:3] ])
    display_tema.short_description = 'Tema'
    
    def __unique__(self):
    	return self.tema
        
    def __str__(self):
        return self.tema
    
#from .validators import valid_extension
#import uuid
class Book (models.Model):

    """
    modelo que representa un Lbro
    """
    
    title=models.CharField(max_length=200)

    author=models.ForeignKey('Author', on_delete=models.CASCADE, null=True)
    # ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
    # 'Author' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.

    Summary=models.TextField(max_length=500 ,help_text="ingrese un breve resumen dellibro")


    bookfile=models.ForeignKey('FileBook',  on_delete=models.CASCADE, null=True)
    area=models.ForeignKey('Tema',  on_delete=models.CASCADE, null=True)
    
    create= models.DateField(auto_now=True)
    update=models.DateField(auto_now_add=True)

  

    def __unique__(self):
        return self.title

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])
    
    
class Filebook(models.Model):

    #book=models.ForeignKey('Book',on_delete=models.SET_NULL,null=True)

    portada=models.ImageField(verbose_name='portadas',upload_to='PORTADA_LIBRO') #,height_field='50', width_field='100')
    myfile =  models.FileField(verbose_name="Libro", upload_to='LIBROS')#,validators=[valid_extension])
    

    def __str__(self):
        
        return  '{}'.format(self.myfile)
    def __unique__(self):
        return self.myfile

    def  get_absolute_url(self):
        return reverse("filebook_detail", kwargs={"pk": self.pk})
    
class Author (models.Model):
    """
    model que representa al ahutor


    """
    first_name=models.CharField(null=True,blank=True, max_length=50)
    last_name=models.CharField( default='' ,null=True, blank=True, max_length=50)
    date_of_birth=models.DateField (null=True, blank=True)
    date_of_death=models.DateField("Died",null=True,blank=True)
    foto=models.ImageField(verbose_name='foto',upload_to='FOTO_AUTHOR')
    Biografia=models.TextField(max_length=2000 ,help_text="ingrese un breve resumen de la Bibliografiaexit")
        

    def get_absolute_url(self):
        return reverse("author_detail", kwargs={"pk": self.pk})
    
    
    def __str__(self):
        return "{} {}".format(self.first_name,self.last_name)

    







