from django.contrib import admin

from .models import Author,Book,Genero,Filebook,Subgenero,Tema
# Register your models here.




#defina clase admin
class BookInline(admin.TabularInline):
    model = Book
    


#class   GeneroInline(admin.TabularInline):
#    model=Genero
class TemaInLine(admin.TabularInline):

    model=Tema
    fk_name='subgenero'

#class FileBookInline(admin.TabularInline):
    #model=Filebook
    

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    
    list_filter=('title','area','author')

    list_display=('title','author','area','Summary','bookfile')
    search_fields=['title','area__tema','author__first_name','author__last_name']
    readonly_fields=('create','update')
    #inlines=[FileBookInline]
    fieldsets=(None,
    {'fields':
    ('title','author','area','Summary','bookfile')
    }),
    ('Availability',{
        'fields':
        ('date_of_birth','date_of_death')
       })
            
                
   


@admin.register(Filebook)
class FilebookAdmin(admin.ModelAdmin):
    list_display=('portada','myfile')
    search_fields=('portada','myfile')
    list_filter=('portada','myfile')

    

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    search_fields=['nombre']
      


@admin.register(Subgenero)
class SubgeneroAdmin(admin.ModelAdmin):

    list_display=['nombre','genero']
    search_fields=['nombre' ,'genero__nombre']
    inlines=[TemaInLine]
    

@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):

    

    search_fields=['tema','subgenero__nombre'] 
    list_filter=('tema','subgenero__nombre') 
    list_display=('tema','subgenero')
    
    
           

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','date_of_birth','date_of_death')

    fields=['first_name','last_name','foto','Biografia',('date_of_birth','date_of_death')]
    

    list_filter=('first_name','last_name')
    search_fields=('first_name','last_name')

    inlines=[BookInline]