from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls. static import static
from . import views


urlpatterns = [
    path('',views.index, name='index'),
    path('books/',views.BookListView.as_view(),name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name ='book-detail'),
    path('editbook/<int:pk>', views.EditBook.as_view(), name = 'edit-book'),
    path('booksinstance/', views.AddBookInstance.as_view(), name ='bookinstance'),
    path('authors/', views.AuthorListView.as_view(), name = 'authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name = 'author-detail'),
    path('mybooks/',views.LoanedBooksByUserListView.as_view(), name = 'my-borrowed'),
    path('myreserved/',views.ReservedBooksByUserListView.as_view(), name = 'my-reserved'),
    path('allborrowed/',views.AllLoanedBooks.as_view(), name = 'all-borrowed'),
    path('addbook/',views.AddBook.as_view(), name = 'add-book'),
    path('addauthor/',views.AddAuthor.as_view(), name = 'add-author'),
    path('genre/',views.GenreView.as_view(), name = 'genre'),
    path('addgenre/',views.AddGenre.as_view(), name = 'add-genre'),
    path('language/',views.LanguageView.as_view(), name = 'language'),
    path('addlanguage/',views.AddLanguage.as_view(), name = 'add-language'),
    path('loanbook/<slug:pk>',views.ToLoanBook.as_view(), name ='loan-book'),
    path('deletebook/<slug:pk>/',views.DeleteBookInstance.as_view(), name = 'delete-book'),
    path('reservebook/<slug:pk>/',views.ReserveBook.as_view(), name = 'reserve-book'),
    path('members/',views.MemberListView.as_view(), name = 'members'),
    path('member/<int:pk>',views.MemberDetailView.as_view(), name = 'member-detail'),
    path('addmember/',views.AddMember.as_view(), name = 'add-member'),
    path('deletemember/<int:pk>/',views.DeleteMember.as_view(), name = 'delete-member'),
    path('editmember/<int:pk>/',views.EditMember.as_view(), name = 'edit-member'),
    path('counter/<int:pk>/',views.CounterBook.as_view(), name = 'counter-book'),
    path('mostcounted/',views.MostCounted.as_view(), name = 'most-counted'),
    path('addreview/<int:book_pk>/',views.AddReview.as_view(), name = 'add-review'),
    path('listreview/',views.ListReview.as_view(), name = 'list-reviews'),
    path('bementor/',views.AddMentor.as_view(), name = 'be-mentor'),
    path('mentorlist/',views.MentorList.as_view(), name = 'mentor-list'),
    path('deletementor/<slug:pk>',views.DeleteMentor.as_view(), name = 'delete-mentor'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

