from .models import CustomUser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from order.models import Order
from book.models import Book
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework import viewsets
from .serializers import CustomUserSerializer


class CustomUserView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

@login_required(login_url='login')
def show_all_users(request):
    order_by = request.GET.get('order_by')
    if order_by == None:
        order_by = 'id'
    filter_by_id = request.GET.get('filter_by_id')
    filter_by_last_name = request.GET.get('filter_by_last_name')
    filter_by_first_name = request.GET.get('filter_by_first_name')
    filter_by_middle_name = request.GET.get('filter_by_middle_name')
    filter_by_email = request.GET.get('filter_by_email')
    filter_by_role = request.GET.get('filter_by_role')
    filter_by_created_at = request.GET.get('filter_by_created_at')
    if filter_by_id == None: filter_by_id = ''
    if filter_by_last_name == None: filter_by_last_name = ''
    if filter_by_first_name == None: filter_by_first_name = ''
    if filter_by_middle_name == None: filter_by_middle_name = ''
    if filter_by_email == None: filter_by_email = ''
    if filter_by_role == None: filter_by_role = ''
    if filter_by_created_at == None: filter_by_created_at = ''

    all_users = CustomUser.objects.all().order_by(order_by).filter(id__contains=filter_by_id,
                                                                   last_name__contains=filter_by_last_name,
                                                                   first_name__contains=filter_by_first_name,
                                                                   middle_name__contains=filter_by_middle_name,
                                                                   email__contains=filter_by_email,
                                                                   role__contains=filter_by_role,
                                                                   created_at__contains=filter_by_created_at)


    paginator = Paginator(all_users, 3)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    context = {'users': users, 'order_by':order_by, 'filter_by_id':filter_by_id, 'filter_by_last_name':filter_by_last_name, 'filter_by_first_name':filter_by_first_name,
               'filter_by_middle_name':filter_by_middle_name, 'filter_by_email':filter_by_email, 'filter_by_role':filter_by_role,
               'filter_by_created_at':filter_by_created_at}
    return render(request, 'authentication/users.html', context)


def create_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        CustomUser.create(email, password, first_name, middle_name, last_name)
        return redirect('all_users')
    return render(request, 'authentication/create_user.html', {})




def show_user_by_id(request, id):
    user = CustomUser.objects.get(id=id)
    orders_by_user = Order.objects.filter(user=user)
    return render(request, 'authentication/user_id.html', {'user': user, 'orders_by_user':orders_by_user})

def profile(request, id):
    user = CustomUser.objects.get(id=id)
    orders_by_user = Order.objects.filter(user=user)
    return render(request, 'authentication/profile.html', {'user': user, 'orders_by_user':orders_by_user})

def delete_user(request, id):
    orders_user_id = []
    for order in Order.get_all():
        if order.end_at is None:
            orders_user_id.append(order.user_id)
    if id not in orders_user_id:
        CustomUser.delete_by_id(id)
        return redirect('all_users')
    else:
        messages.info(request, 'User have open order')
        return redirect('all_users')


def update_user(request, id):
    user = CustomUser.objects.get(id=id)
    if request.method == 'POST':

        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        is_active = True
        if role == '1':
            is_staff = True
        elif role == '0':
            is_staff = False
        user.update(first_name, last_name, middle_name, password, role, is_active, is_staff)

        return redirect('all_users')
    return render(request, 'authentication/update_user.html', {'user': user})


def register_page(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('first_name')
            messages.success(request,'Account was created for ' + user)
            return redirect('login')
    context = {'form': form}
    return render(request,'authentication/register.html',context)


def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/book')
        else:
            messages.info(request,'Email OR password is incorrect')

    context = {}
    return render(request,'authentication/login.html',context)


def user_order(request, id):
    user = CustomUser.objects.get(id=id)
    books = Book.objects.all()
    from datetime import date, timedelta
    today = date.today()
    delta = timedelta(days=7)
    date = (today+delta).strftime("%Y-%m-%d")
    if request.method == 'POST':
        print("fwfgerg")
        user = CustomUser.objects.get(id=request.POST.get('user'))
        book = Book.objects.get(id=request.POST.get('book'))
        book_count= request.POST.get('book_count')
        plated_end_at = request.POST.get('plated_end_at')
        if int(book_count) <= int(book.count)-int(list(Order.objects.filter(end_at__isnull=True).values_list('book_id', flat=True)).count(book.id)):
            print('Ok')
            Order.create(user, book, book_count, plated_end_at)
            return redirect('user_id',id)
        else:
            print('Bad(')
            messages.error(request, f'Error: No more this book {book.name} in library')
            return redirect('user_id',id)
    return render(request, 'authentication/user_order.html', {'user': user, 'books':books, 'date':date})


def log_out(request):
    logout(request)
    return redirect('login')
