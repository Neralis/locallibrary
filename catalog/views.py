from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from datetime import date

class BookListView(generic.ListView):
    model = Book
    paginate_by = 1

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllBorrowedBooksView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_all_borrowed.html'  # Создадим шаблон позже
    context_object_name = 'borrowed_books'
    permission_required = 'catalog.can_mark_returned'  # Выберите подходящий permission или замените на `is_staff`

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')  # Например, книги "на руках"


def author_detail_view(request, primary_key):
    author = get_object_or_404(Author, pk = primary_key)
    return render(request, 'catalog/author_detail.html', context={'author': author})

def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # Метод 'all()' применён по умолчанию.
    
    num_book_with_word_1984 = Book.objects.filter(title__icontains = "1984").count()
    num_genres_with_word_f = Genre.objects.filter(name__icontains = "фантастика").count()

    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors,
'num_book_with_word_1984':num_book_with_word_1984,'num_genres_with_word_f':num_genres_with_word_f, 'num_visits':num_visits}
    ) 