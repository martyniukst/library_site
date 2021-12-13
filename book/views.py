from django.shortcuts import render, redirect
from .models import Book
from author.models import Author
from order.models import Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CreateBookForm, UpdateBookForm
from django.contrib import messages
from rest_framework import viewsets
from .serializers import BookSerializer


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


def all_books(request):
    order_by = request.GET.get('order_by')
    if order_by == None:
        order_by = 'id'
    filter_by_id = request.GET.get('filter_by_id')
    filter_by_name = request.GET.get('filter_by_name')
    filter_by_author = request.GET.get('filter_by_author')
    filter_by_count = request.GET.get('filter_by_count')
    filter_by_description = request.GET.get('filter_by_description')
    if filter_by_id == None: filter_by_id = ''
    if filter_by_name == None: filter_by_name = ''
    if filter_by_author == None: filter_by_author = ''
    if filter_by_count == None: filter_by_count = ''
    if filter_by_description == None: filter_by_description = ''
    all_books = Book.objects.all().order_by(order_by).filter(count__contains=filter_by_count, authors__full_name__contains=filter_by_author, id__contains=filter_by_id, name__contains=filter_by_name, description__contains=filter_by_description)


    paginator = Paginator(all_books, 10)
    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    context = {'books': books, 'order_by':order_by, 'filter_by_count':filter_by_count, 'filter_by_id':filter_by_id, 'filter_by_name':filter_by_name,
               'filter_by_description':filter_by_description, 'filter_by_author':filter_by_author}
    return render(request, 'book/books.html', context)


def unordered_book(request):
    order_objects = Order.objects.all()
    books = Book.objects.all()
    obj_dict={}
    new_dict={}
    for item in order_objects:
        if item.book_id not in obj_dict:
            obj_dict[item.book_id]=item.book_count
        else:
            obj_dict[item.book_id]+=item.book_count
    for item in books:
        if item.id not in obj_dict.keys():
            new_dict[item]=item.count
        elif obj_dict[item.id]<item.count:
            new_dict[item]=item.count-obj_dict[item.id]
    context = {'test_list': new_dict}
    return render(request, 'book/unordered_book.html', context)


def show_book_by_id(request, id):
    book = Book.objects.get(id=id)
    orders_book= Order.objects.filter(book=id)
    return render(request, 'book/book_id.html', {'book': book, 'orders_book':orders_book})


@login_required(login_url='/user/login')
def delete_book(request, id):
    orders_book_id = []
    for order in Order.get_all():
        if order.end_at is None:
            orders_book_id.append(order.book_id)
    if id not in orders_book_id:
        Book.delete_by_id(id)
        return redirect('all_books')
    else:
        messages.info(request, 'Book(s) still in User')
        return redirect('all_books')


@login_required(login_url='/user/login')
def create_book(request):
    authors_all = Author.objects.all()
    form = CreateBookForm()
    if request.method == "POST":
        form = CreateBookForm(request.POST)
        if form.is_valid():
            for book in Book.objects.all():
                if book.name == form.cleaned_data['name']:
                    for item in list(form.cleaned_data['authors'].values_list(flat=True)):
                        if item in list(book.authors.all().values_list(flat=True)):
                            messages.error(request, f'Error:  This book already exist')
                            return redirect('create_book')
            form.save()
            return redirect('all_books')
    context = {'form': form, 'authors_all':authors_all}
    return render(request,'book/create_book.html',context)

@login_required(login_url='/user/login')
def update_book(request, id):
    book = Book.objects.get(id=id)
    form = UpdateBookForm(instance=book)
    if request.method == "POST":
        form = UpdateBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('all_books')
    context = {'form': form, 'book':book}
    return render(request,'book/update_book.html',context)



