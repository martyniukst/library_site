from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from .models import Author
from order.models import Order
from book.models import Book
from .forms import CreateAuthorForm
from django.contrib import messages
from rest_framework import viewsets
from .serializers import AuthorSerializer


class AuthorView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

def all_authors(request):
    order_by = request.GET.get('order_by')
    if order_by == None:
        order_by = 'id'
    filter_by_id = request.GET.get('filter_by_id')
    filter_by_name = request.GET.get('filter_by_name')
    filter_by_surname = request.GET.get('filter_by_surname')
    filter_by_patronymic = request.GET.get('filter_by_patronymic')
    if filter_by_id == None: filter_by_id = ''
    if filter_by_name == None: filter_by_name = ''
    if filter_by_surname == None: filter_by_surname = ''
    if filter_by_patronymic == None: filter_by_patronymic = ''

    all_books = Author.objects.all().order_by(order_by).filter(surname__contains=filter_by_surname, id__contains=filter_by_id, name__contains=filter_by_name,
                                                               patronymic__contains=filter_by_patronymic)


    paginator = Paginator(all_books, 5)
    page = request.GET.get('page')
    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)
    context = {'authors': authors, 'order_by':order_by, 'filter_by_surname':filter_by_surname, 'filter_by_id':filter_by_id, 'filter_by_name':filter_by_name,
               'filter_by_patronymic':filter_by_patronymic}
    return render(request, 'author/authors.html', context)


def create_author(request):
    if request.method == 'POST':
        form = CreateAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_authors')
    return render(request, 'author/create_author.html', {})


def show_author_by_id(request, id):
    author = Author.objects.get(id=id)
    books_by_author = Book.objects.filter(authors=author)
    return render(request, 'author/author_id.html', {'author': author, "books_by_author":books_by_author})


def delete_author(request, id):
    orders_book_id = []
    orders_author_id = []
    for order in Order.get_all():
        if order.end_at is None:
            orders_book_id.append(order.book_id)
    for item in orders_book_id:
        book = Book.objects.get(id=item)
        for author in list(book.authors.values_list(flat=True)):
            orders_author_id.append(author)
    print(orders_author_id)
    if id not in orders_author_id:
        Author.delete_by_id(id)
        return redirect('all_authors')
    else:
        messages.info(request, 'Book(s) still in User')
        return redirect('all_authors')


def update_author(request, id):
    author = Author.objects.get(id=id)
    if request.method == 'POST':
        form = CreateAuthorForm(request.POST)
        if form.is_valid():
            form.save()
        author.update(form)
        return redirect('all_authors')
    return render(request, 'author/update_author.html', {'author': author})