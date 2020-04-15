from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime 
from django import forms
from .models import Book, Author, Language, Genre, BookInstance


class AddBookInstanceForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book','imprint','main_class',]


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','author','summary','isbn','genre','language','image',]


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name','last_name',]

class AddLanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name',]

class AddGenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name',]




