from django.shortcuts import render, redirect
from .forms import CustomerForm, Books_orderedForm, Books_availableForm
from .models import Customer, Books_available, Books_ordered
from django.contrib import messages


# Create your views here.
def home(request):
    books = Books_available.objects.all()
    userid = request.GET.get('id')
    orders = Books_ordered.objects.filter(customer=userid)

    order_details = []
    for order in orders:
        try:
            book = Books_available.objects.get(book_id=order.book_id)  
            order_details.append({
                "order": order,
                "image": book.image.url if book.image else None
            })
        except Books_available.DoesNotExist:
            continue


    return render(request, "home.html", {
    "books": books,
    "order_details": order_details
    })

def admin(request):
    form = Books_availableForm()
    if request.method == 'POST':
        form = Books_availableForm(request.POST, request.FILES)
        if form.is_valid():
            books= form.save()
            return redirect('home')
    else :
        form = Books_availableForm()
    return render(request,'admin.html',{"form" : form})

def signup(request):
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        print("hi")
        if form.is_valid():
            print("hello")
            user = form.save()
            user_name = user.name
            user_id = user.id_number
            return redirect(f'/?user={user_name}&id={user_id}')
    else :
        form = CustomerForm()
    return render(request, 'signup.html', {"form" : form})


def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        phone = request.POST.get('phone')

        try:
            user = Customer.objects.get(name=username, phone_number=phone)
            return redirect(f'/?user={user.name}&id={user.id_number}')
        except Customer.DoesNotExist:
            messages.error(request, "Invalid username or phone number")

    return render(request, 'signin.html')
# def place_order(request):
#     user_id = request.GET.get('id')
#     user_info = Customer.objects.get(id_number=user_id)
    
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt  
def place_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            user_id = data.get("user_id")
            items = data.get("items", [])

            customer = Customer.objects.get(id_number=user_id)

            for item in items:
                Books_ordered.objects.create(
                    name=item["name"],
                    book_id=item["book_id"],
                    customer=customer,
                    price=item["price"]
                )
                stock = Books_available.objects.get(book_id = item['book_id']).stock
                print(stock)
                Books_available.objects.update_or_create(
                    book_id = item['book_id'],
                    defaults={
                        'stock' : int(stock) -  int(item['qty'])
                    }
                    )

            return JsonResponse({"message": "Order placed successfully!"})

        except Customer.DoesNotExist:
            return JsonResponse({"message": "Customer not found."}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Error: {str(e)}"}, status=500)

    return JsonResponse({"message": "Invalid request method."}, status=405)
