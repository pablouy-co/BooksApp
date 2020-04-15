from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from datetime import timedelta
import datetime
from .models import Book, Author, BookInstance, Genre, Language, Member, Review, Mentor
from .forms import AddBookForm, AddAuthorForm, AddGenreForm, AddLanguageForm
from .forms import  AddBookInstanceForm

@login_required
def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Libros disponibles (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # El 'all()' esta implícito por defecto.
    
    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
    )
'''------------------------Clases de ingreso (Libro, Autor, Lenguaje, Genero)------------------------'''

class AddBook(PermissionRequiredMixin,generic.CreateView):
    model = Book
    permission_required = 'gestion.can_mark_returned'
    form_class = AddBookForm
    success_url = reverse_lazy('add-book')

class AddAuthor(PermissionRequiredMixin,generic.CreateView):
    model = Author
    permission_required = 'gestion.can_mark_returned'
    form_class = AddAuthorForm
    success_url = reverse_lazy('add-author')

class AddGenre(PermissionRequiredMixin,generic.CreateView):
    model = Genre
    permission_required = 'gestion.can_mark_returned'
    form_class = AddGenreForm
    success_url = reverse_lazy('add-genre')

class AddLanguage(PermissionRequiredMixin,generic.CreateView):
    model = Language
    permission_required = 'gestion.can_mark_returned'
    form_class = AddLanguageForm
    success_url = reverse_lazy('add-language')

class AddBookInstance(PermissionRequiredMixin,generic.CreateView):
    model = BookInstance
    permission_required = 'gestion.can_mark_returned'
    form_class = AddBookInstanceForm
    template_name = 'gestion/bookinstance_add_form.html'
    success_url = reverse_lazy('bookinstance')

class AddMember(PermissionRequiredMixin,generic.CreateView):
    model = Member
    permission_required = 'gestion.can_mark_returned'
    fields = ['first_name','last_name','email','phone_num','memberID',]
    success_url = reverse_lazy('members')

class AddMentor(LoginRequiredMixin,generic.CreateView):
    model = Mentor
    fields = ['book','contact_email',]
    success_url = reverse_lazy('mentor-list')

    def form_valid(self, form):
        form.instance.mentor = self.request.user
        return super().form_valid(form)


'''----------------------------Clases para edición------------------------------------------------'''
class EditBook(PermissionRequiredMixin,generic.UpdateView):
    model = Book
    permission_required = 'gestion.can_mark_returned'
    form_class = AddBookForm
    success_url = reverse_lazy('authors')


class ToLoanBook(generic.UpdateView):
    model = BookInstance
    fields = ['borrower',]
    template_name = 'gestion/loan-book.html'
    success_url = reverse_lazy('all-borrowed')
    
    def form_valid(self, form):
        dueback = datetime.datetime.now() + timedelta(days=15)
        # Entramos al if si el usuario autenticado es admin
        if self.request.user.is_superuser:
            if form.instance.status == 'a':
                form.instance.status = 'o' # Damos el valor de "a" al campo status si es "o"
                form.instance.due_back = dueback
 
            elif form.instance.status == 'o':
                form.instance.status = 'a' # Damos el valor de "a" al campo status si es "r"
                form.instance.borrower = None #Al devolver, borrower y fecha deben quedar vacias
                form.instance.due_back = None

            elif form.instance.status == 'r':
                form.instance.status = 'o'
                form.instance.due_back = dueback
                
        return super().form_valid(form)

class ReserveBook(generic.UpdateView):
    model = BookInstance
    fields = ['status',]
    template_name = 'gestion/reserve-book.html'
    success_url = reverse_lazy('my-reserved')
    
    def form_valid(self, form):
        # Entramos al if si el usuario autenticado no es admin
        if not self.request.user.is_superuser:
            if form.instance.status == 'a':
                form.instance.status = 'r' # Damos el valor de "r" al campo status si es "a"
                form.instance.borrower = self.request.user  
            elif form.instance.status == 'r':
                form.instance.status = 'a' # Damos el valor de "a" al campo status si es "r"
                form.instance.borrower = None

        return super().form_valid(form)
        

class EditMember(PermissionRequiredMixin,generic.UpdateView):
    model = Member
    permission_required = 'gestion.can_mark_returned'
    fields = ['first_name','last_name','email','phone_num','memberID',]
    success_url = reverse_lazy('members')

class CounterBook(generic.UpdateView):
    model = Book
    fields = ['counter',]
    template_name = 'gestion/counter_book.html'
    success_url = reverse_lazy('authors')

    def form_valid(self,form):
        form.instance.counter = form.instance.counter + 1
        return super().form_valid(form)

'''
def reserveBook (request,id):
    status = BookInstance.objects.get(id = id)
    if request.method == 'GET':
        bookinstance_form = ToLoanBookForm(instance = status)
    else:
        bookinstance_form = ToLoanBookForm(request.POST, instance = status)
        if bookinstance_form.is_valid():
            bookinstance_form.save()
        redirect('index')
    return render(request,'gestion/bookinstance_add.html',{'bookinstance_form':bookinstance_form})'''

'''---------------------------------------Clases para vistas--------------------------------------------'''
class BookListView(generic.ListView):
    model = Book
    #paginate_by = 5 #paginacion

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query != None:
            object_list = Book.objects.filter(
                Q(title__icontains=query) | Q(author__first_name__icontains=query) | Q(author__last_name__icontains=query)
            )
            return object_list

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(LoginRequiredMixin,generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class GenreView(generic.ListView):
    model = Genre
    paginate_by = 10

class LanguageView(generic.ListView):
    model = Language
    paginate_by = 10

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'gestion/bookinstance_list_borrowed_user.html'
    paginate_by = 10
      
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class ReservedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'gestion/list_reserved_books_user.html'
    paginate_by = 10
      
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='r').order_by('due_back')

class AllLoanedBooks(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'gestion.can_mark_returned'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

class MemberListView(generic.ListView):
    model = Member
    paginate_by = 10

class MemberDetailView(generic.DetailView):
    model = Member

class MostCounted(generic.ListView):
    model = Book
    template_name = 'gestion/most_counted.html'

class MentorList(generic.ListView):
    model = Mentor

'''------------------------------------------------Clases para borrar-----------------------------------'''

class DeleteBookInstance(PermissionRequiredMixin, generic.DeleteView):
    model = BookInstance
    permission_required = 'gestion.can_mark_returned'
    success_url = reverse_lazy('authors')

class DeleteMember(PermissionRequiredMixin,generic.DeleteView):
    model = Member
    permission_required = 'gestion.can_mark_returned'
    success_url = reverse_lazy('members')

class DeleteMentor(LoginRequiredMixin,generic.DeleteView):
    model = Mentor
    success_url = reverse_lazy ('mentor-list')


'''------------------RESEÑAS----------------------------'''

class AddReview(LoginRequiredMixin,generic.CreateView):
    model = Review
    fields = ('comment','rating',)
    success_url = reverse_lazy('list-reviews')

    def form_valid(self, form):

        book = Book.objects.get(pk = self.kwargs.get('book_pk')) #Obtengo el libro
        form.instance.book = book
        form.instance.user_name =  self.request.user
        
        return super().form_valid(form)


class ListReview(generic.ListView):
    model = Review
    paginate_by = 5


