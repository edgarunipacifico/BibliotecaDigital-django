from .import views
from .views import BookDetail,ListBookView,AuthorList,AuthorDetail
    
from django.urls import path



#app_name='GestorBiblioteca'
urlpatterns = [
    
    path('create_subgenero/', views.SubgeneroCreate.as_view(), name='subgenero_create'),
    path('create_genero/',views.GeneroCreate.as_view(),name='genero_create' ),
    path('create_tema/', views.TemaCreate.as_view(), name='tema_create'),
    path('create_author/', views.AuthorCreate.as_view(), name='author_create'),
    path('create_book/', views.BookCreate.as_view(), name='book_create'),
    path('GestorBiblioteca/<int:id>/',views.list_book_x_genero, name='list_book_x_genero'),
    path('',views.index,name='index'),
    path('buscar/',views.buscar,name='busqueda'),
    
    path('book/',views.ListBookView.as_view(),name='Lista_Book'),
    path('<int:tema_id>/',views.list_book_x_tema , name='listbook_x_tema'),
    path('book/<int:pk>',views.BookDetail.as_view(), name='book-detail'),
    


    path('<int:subgenero_id>/', views.list_book_x_subgenero, name='lisbook_x_subgenero'),
    
    #path('/<pk>', views.FileBookDetail.as_view(),name='filebook_detail'),
    
    path('GestorBiblioteca/author/<int:pk>/', AuthorDetail.as_view(),name='author_detail'),
    path('author/',AuthorList.as_view(), name='author_list'),

    


]