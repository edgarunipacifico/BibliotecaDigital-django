from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.http import HttpResponseRedirect,request,HttpResponse
from django.db.models import Q,CharField
from django.db.models import Value as V
from .models import Book,Filebook,Author,Genero,Subgenero,Tema
from django.db.models.functions import Concat
from django.urls import  reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import NewAuthorForm,NewBookForm,LoadFilebook,NewTemaForm,NewSubjeneroForm,NewGeneroForm

def control(request):
    pass


class GeneroCreate(CreateView):
    model=Genero
    template_name='GestorBiblioteca/create_genero.html'
    success_url=reverse_lazy('subgenero_create')
    form_class= NewGeneroForm
    

class SubgeneroCreate(CreateView):
    model=Subgenero
    template_name='GestorBiblioteca/create_subgenero.html'
    success_url=reverse_lazy('tema_create')
    form_class= NewSubjeneroForm
         

    

class TemaCreate(CreateView):
    model=Tema
    template_name='GestorBiblioteca/create_tema.html'
    success_url=reverse_lazy('book_create')
    form_class= NewTemaForm

class AuthorCreate(CreateView):
    model=Author
    template_name='GestorBiblioteca/create_author.html'
    success_url=reverse_lazy('book_create')
    form_class= NewAuthorForm
    context_object_name = 'obj'
  

class BookCreate(CreateView):
    model = Book
    template_name='GestorBiblioteca/create_book.html'
    #fields=['myfile']
    success_url=reverse_lazy('Lista_Book')
    form_class= NewBookForm
    second_form_class=LoadFilebook 
    #aderimos los formularios al contexto
    
    
    

    """
    def  get_context_data(self, **kwargs):
        data=super().get_context_data(**kwargs)
        if self.request.POST:
            data['form2']= self.second_form_class(self.request.POST)    
        else:
            data['form2']=self.second_form_class()
        return data

    def form_valid(self,form,form2):
        context=self.get_context_data()
        book=context['form2','form'] 
        self.object=form.save()
        if book.is_valid():
            book.instance=self.object
            book.save()

        return super().form_valid(form)

    def get_success_url(self):   
        return reverse('book_create')
"""
    def  get_context_data(self, **kwargs):
        
        context=super(BookCreate,self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form']=self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2']=self.second_form_class(self.request.GET)
        return context       

    #guardamos la info formularios 
    def post(self,request,*args, **kwargs):
        
        self.object=self.get_object
        #acdemos al objeto
        #recojemos la informacion ingresaday validamos
        form=self.form_class(request.POST)
        form2=self.second_form_class(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
            book=form.save(commit=False)
            book.bookfile=form2.save()#creamos la relacion
            book.save()
            
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form,form2=form2))
          

class ListBookView(ListView):
    
    model=Book
    #context_object_name='my_booḱ_list'
    template_name='GestorBiblioteca/listbook.html'
    #paginate_by = 6

class AuthorList(ListView):
    
    model=Author
    template_name='GestorBiblioteca/author_list.html'



class BookDetail( DetailView):

    model=Book
    template_name='GestorBiblioteca/book-detail.html'

    
    

class FileBookDetail(DetailView):
    model=Filebook
    template_name='GestorBiblioteca/filebook_detail.html'


class AuthorDetail(DetailView):
    model=Author
    template_name='GestorBiblioteca/author_detail.html'
    

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        context['book_list'] = Book.objects.filter(author__pk=pk)
        
        
        return context
    
    


def index(request):
    book=""

    
    books=Book.objects.all()#.select_related('author')
    author=Author.objects.all()
    generos=Genero.objects.all()
    subgeneros=Subgenero.objects.all()#.select_related('genero')
    temas=Tema.objects.all()#.select_related('subgenero')
    
    # Número de visitas a esta vista, contadas en la variable de sesión.
    contador_visitas=request.session.get('num_visits', 0)
    request.session['num_visits'] = contador_visitas + 1

    return render (request,'GestorBiblioteca/index.html',{
            'temas':temas,'subgeneros':subgeneros,
            'generos':generos,'books':books,'author':author,'contador_visitas':contador_visitas})
    

    
def buscar(request):
    global books
    authors,generos,books=" ","",""
    if  request.GET["busqueda"]:#valida que la cadena no este basida
        #mensaje="articulo buscado: %r" %request.GET["producto"]
        busqueda=request.GET["busqueda"]

        if len(busqueda)>20:#validamos que la cadena no sea demasiada larga

            mensaje="Texto de busqueda demasiado largo <BR>  Maximo 20 carateres"
        
        
        else:
    
            queryset=(Q(title__icontains=busqueda)|
                        Q(area__tema__icontains=busqueda)|
                        Q(author__first_name__icontains=busqueda)|
                        Q(author__last_name__icontains=busqueda)|
                        Q(author__date_of_birth__icontains=busqueda)|
                        Q(author__date_of_death__icontains=busqueda)|
                        Q(Summary__icontains=busqueda))

    

            validador=Book.objects.filter(queryset)
            
            #validador.exists()

            if validador:

                books=Book.objects.filter(queryset)
                
           
                
                
            else:
                
                validador=Genero.objects.filter(nombre__icontains=busqueda).exists()
                if validador:
                    generos=Genero.objects.filter(nombre__icontains=busqueda)
                
                else:
                    
                    authors = Book.objects.all()
                    if authors:
                        authors = authors.annotate(search_name=Concat('author__first_name', 
                        V(' '), 'author__last_name'))
                        authors= authors.filter(search_name__icontains=busqueda)
                        
                        for i in authors:
                            print(i.get_absolute_url)
                                    
        return  render(request,"Biblioteca/resultado_busqueda.html",
            {"books":books,"generos":generos,'authors':authors,"query":busqueda})
    
    else:
        mensaje="no introdujo articulo para la busqueda"

    return HttpResponse(mensaje)

def list_book_x_tema( request,tema_id ):

    list_book=Book.objects.filter(area__id=tema_id)

    return render(request,"Biblioteca/list_book_x_tema.html",{"list_book":list_book})

@login_required
def list_book_x_genero(request,id):

    list_book=Book.objects.filter(area__subgenero__genero_id=id)
    #queryset=Book.objects.select_related('area')
    #list_book=queryset.filter(subgenero__genero_id=id)
    return render(request,"Biblioteca/list_book_x_genero.html", {'list_book':list_book})


def list_book_x_subgenero(request,subgenero_id):

    list_book_x_subgenero=Book.objects.filter(area__subgenero=subgenero_id)
    
    
    return render(request,"Biblioteca/list_book_x_subgenero.html",
                {"list_book_x_subgenero":list_book_x_subgenero})
