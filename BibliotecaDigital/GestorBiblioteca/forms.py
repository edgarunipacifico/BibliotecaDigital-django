
from .models import Book,Author,Filebook,Tema,Subgenero,Genero
from django_select2 import forms as s2forms
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django import forms

#FilebookFormset=inlineformset_factory(
# Filebook,Book, fields=('bookfile','title','author','Summary')
#)


class AuthorWidget(s2forms.ModelSelect2Widget):

    
    search_fields = [
        "first_name__icontains",
        "last_name__icontains",
    ]
   
   
class TemaWidget(s2forms.ModelSelect2Widget):

    search_fields = [
        "tema__icontains",
        
    ]
class NewSubjeneroForm(forms.ModelForm):
    class Meta:
        model=Subgenero
        fields='__all__'

class NewGeneroForm(forms.ModelForm):
    class Meta:
        model=Genero
        fields='__all__'
        
class NewTemaForm(forms.ModelForm):
    
    class Meta:
        model=Tema
        fields='__all__'

class NewAuthorForm(forms.ModelForm):


    class Meta:
        model=Author
        fields=['first_name','last_name','date_of_birth','date_of_death','foto']
        labels={
            'first_name':'first_name',
            'last_name':'last_name',
            'date_of_birth':'date_of_birth',
            'date_of_death':'date_of_death',
            'foto':'foto',

        }   
        input_formats=['%d/%m/%Y %H:%M'],
        widgets={
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'date_of_birth':forms.DateInput(attrs={'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'}),
            'date_of_death':forms.DateInput(attrs={'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker2'}),
            'foto':forms.FileInput(attrs={'class':'form-control'}),
            'Biografia':forms.Textarea(attrs={'class':'form-control'}),          
        }


class LoadFilebook(forms.ModelForm):
    class Meta:
        model=Filebook
        fields='__all__'

class NewBookForm(forms.ModelForm):
    
   
    class Meta:
        model = Book
        fields =('title','author','Summary','area')

        widgets = {
         "title":forms.TextInput(attrs={'class':'form-control',
         'placeholder':'Title of book','autofocus': 'autofocus','id':'title'}),       
         "Summary":forms.Textarea(attrs={'class':'form-control',
         'placeholder':'Resumen del libro','spellcheck':'true','id':'Summary'}),
         "author": AuthorWidget(attrs={'class':'form-control','id':'author'}),
         "area":TemaWidget(attrs={'class':'form-control','id':'area'}),  
       } 
