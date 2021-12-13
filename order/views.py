from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Order
from authentication.models import CustomUser
from book.models import Book
from datetime import datetime
import pytz
from django.contrib import messages
from rest_framework import viewsets
from .serializers import OrderSerializer

utc=pytz.UTC

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


def show_all_orders(request):
    order_by = request.GET.get('order_by')
    if order_by == None:
        order_by = 'id'
    filter_by_id = request.GET.get('filter_by_id')
    filter_by_user = request.GET.get('filter_by_user')
    filter_by_book = request.GET.get('filter_by_book')
    filter_by_created_at = request.GET.get('filter_by_created_at')
    filter_by_plated_end_at = request.GET.get('filter_by_plated_end_at')
    filter_by_book_count = request.GET.get('filter_by_book_count')
    filter_by_end_at = request.GET.get('filter_by_end_at')

    if filter_by_id == None: filter_by_id = ''
    if filter_by_user == None: filter_by_user = ''
    if filter_by_book == None: filter_by_book = ''
    if filter_by_created_at == None: filter_by_created_at = ''
    if filter_by_plated_end_at == None: filter_by_plated_end_at = ''
    if filter_by_book_count == None: filter_by_book_count = ''
    if filter_by_end_at == None: filter_by_end_at =''
    all_orders = Order.objects.all().order_by(order_by).filter(id__contains=filter_by_id,
                                                                   user__last_name__contains=filter_by_user,
                                                                   book__name__contains=filter_by_book,
                                                                   created_at__contains=filter_by_created_at,
                                                                   plated_end_at__contains=filter_by_plated_end_at,
                                                                   book_count__contains=filter_by_book_count)
    print(all_orders)


    paginator = Paginator(all_orders, 5)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    context = {'orders': orders, 'order_by':order_by, 'filter_by_id':filter_by_id, 'filter_by_user':filter_by_user, 'filter_by_book':filter_by_book,
               'filter_by_created_at':filter_by_created_at, 'filter_by_book_count':filter_by_book_count, 'filter_by_end_at':filter_by_end_at,
               'filter_by_plated_end_at':filter_by_plated_end_at}
    return render(request, 'order/orders.html', context)

def show_order_by_id(request, id):
    order = Order.objects.get(id=id)
    return render(request, 'order/order_id.html', {'order': order})


def create_order(request):
    users = CustomUser.objects.all()
    books = Book.objects.all()
    from datetime import date, timedelta
    today = date.today()
    delta = timedelta(days=7)
    date = (today+delta).strftime("%Y-%m-%d")
    if request.method == 'POST':
        user = CustomUser.objects.get(id=request.POST.get('user'))
        book = Book.objects.get(id=request.POST.get('book'))
        book_count= request.POST.get('book_count')
        plated_end_at = request.POST.get('plated_end_at')
        if int(book_count) <= int(book.count)-int(list(Order.objects.filter(end_at__isnull=True).values_list('book_id', flat=True)).count(book.id)):
            Order.create(user, book,book_count, plated_end_at)
            return redirect('all_orders')
        else:
            messages.error(request, f'Error: No more this book {book.name} in library')
            return redirect('all_orders')
    return render(request, 'order/create_order.html', {'date':date, 'users': users, 'books': books})


def delete_order(request, id):
    order = Order.objects.get(id=id)
    if order.end_at != None:
        Order.delete_by_id(id)
    else:
        messages.error(request, f'Error: This order already open!')
        return redirect('all_orders')
    return redirect('all_orders')


def update_order(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        end_at = request.POST.get('end_at')
        if end_at =='1':
            end_at = datetime.now()
        else:
            end_at = None
        plated_end_at = request.POST.get('plated_end_at')
        order.update(plated_end_at, end_at)
        return redirect('all_orders')
    return render(request, 'order/update_order.html', {'order': order})

def show_expired_order(request):
    orders = []
    for order in Order.get_all():
        if order.end_at is None and order.plated_end_at.replace(tzinfo=utc) < datetime.now().replace(tzinfo=utc):
            orders.append(order)
        elif order.end_at is not None and order.plated_end_at.replace(tzinfo=utc)<order.end_at.replace(tzinfo=utc):
            orders.append(order)

    return render(request, 'order/expired_order.html', {'orders': orders})
