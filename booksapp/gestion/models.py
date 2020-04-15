from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
import uuid # Requerida para las instancias de libros únicos
import numpy as np

class Genre(models.Model):
    name = models.CharField(verbose_name = 'Genero', max_length=200,
        help_text="Ingrese el nombre del género (p. ej. Ciencia Ficción, Poesía Francesa etc.)")
    
    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(verbose_name = 'Lenguaje', max_length=200,
        help_text="Ingrese lenguaje de libro")
    
    def __str__(self):
        return self.name

class Member(models.Model):
    first_name = models.CharField(max_length = 100, verbose_name = 'Nombre')
    last_name = models.CharField(max_length = 100, verbose_name = 'Apellido')
    email = models.EmailField(blank = True, null = True)
    phone_num = models.CharField(max_length = 15, verbose_name = 'No Telefono')
    memberID = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank = True, verbose_name="ID de") 

    def __str__(self):
        return '%s %s' % (self.first_name,self.last_name)


class Book(models.Model):
    """
    Modelo que representa un libro (pero no un Ejemplar específico).
    """
    title = models.CharField(verbose_name = 'Titulo', max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, verbose_name = 'Autor')
    # ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
    # 'Author' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.
    summary = models.TextField(max_length=1000, 
        help_text="Ingrese una breve descripción del libro", verbose_name = 'Resumen')  
    isbn = models.CharField('ISBN',max_length=13,
        help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, 
        help_text="Seleccione los generos de este libro", verbose_name = 'Genero')
    # ManyToManyField, porque un género puede contener muchos libros y un libro puede cubrir varios géneros.
    # La clase Genre ya ha sido definida, entonces podemos especificar el objeto arriba.
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, verbose_name = 'Lenguaje')
    image = models.ImageField(upload_to = 'gestion', null = True, blank = True, verbose_name = 'Imagen')
    counter = models.IntegerField(blank = True, null = True, default = 0)
    
    def __str__(self):

        return self.title
    
    def get_absolute_url(self):

        return reverse('book-detail', args=[str(self.id)]) #Devuelve la URL a una instancia particular de Book
    
    def display_genre(self):
  
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ]) #Crea string para el genero (para Admin)
    
    display_genre.short_description = 'Genre'

    def average_rating(self):       #funcion para obtener el promedio de ratings
        all_ratings = map(lambda x: x.rating, self.review_set.all())
        return np.mean(list(all_ratings),dtype='int8')


class BookInstance(models.Model):
    """
    Modelo que representa una copia específica de un libro (una biblioteca puede tener varios ejemplares de un libro)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, verbose_name = 'Libro') 
    imprint = models.CharField(max_length=200, verbose_name = 'Editorial')
    due_back = models.DateField(null=True, blank=True, verbose_name = 'Fecha devolución', help_text = 'Si tiene fecha de devolucion el estado no puede ser Disponible')
    loan_date = models.DateField(null=True, blank=True,)

    LOAN_STATUS = (
        ('o', 'En prestamo'),
        ('a', 'Disponible'),
        ('r', 'Reservado'),
    )

    status = models.CharField(max_length = 1, choices = LOAN_STATUS, blank = True, default='a', verbose_name = 'Estado', help_text = 'No puede estar diponible y con fecha de devolucion')

    MAIN_CLASIFICATION = (
        ('a','Academico'),
        ('l','Literatura'),
        ('n','No ficción'),
    )

    main_class = models.CharField(max_length = 1, choices = MAIN_CLASIFICATION, blank = True, verbose_name = 'Estantería',  help_text = '(Academico, Literatura, No ficción)')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank = True, verbose_name="Prestatario")
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)        

    def __str__(self):

        return '%s (%s)' % (self.id,self.book.title)


class Author(models.Model):

    first_name = models.CharField(max_length=100, verbose_name = 'Nombre')
    last_name = models.CharField(max_length=100, verbose_name = 'Apellido')
    
    class Meta:
        ordering = ['last_name']
    
    def get_absolute_url(self):
 
        return reverse('author-detail', args=[str(self.id)]) #Retorna la url para acceder a una instancia particular de un autor.
   
    def __str__(self):

        return '%s, %s' % (self.last_name, self.first_name)


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    book = models.ForeignKey(Book, null = True, on_delete = models.DO_NOTHING, verbose_name = 'Libro')
    pub_date = models.DateTimeField(auto_now=True,verbose_name = 'Fecha de publicacion')
    user_name = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank = True)
    comment = models.TextField(verbose_name = 'Reseña')
    rating = models.IntegerField(choices=RATING_CHOICES,verbose_name = 'Clasificación')
    class Meta:
        ordering = ['-pub_date']

    def get_absolute_url(self):

        return reverse('review-detail', args=[str(self.id)])

class Mentor(models.Model):
    mentor = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Referente')
    book = models.ForeignKey(Book, on_delete = models.CASCADE, verbose_name = 'Libro')
    contact_email = models.EmailField(verbose_name = 'E-mail de contacto')




