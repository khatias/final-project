from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Category, Product, Basket, BasketItem
import requests


def import_data(request):
    categories_url = 'https://restaurant.stepprojects.ge/api/Categories/GetAll'
    products_url = 'https://restaurant.stepprojects.ge/api/Products/GetAll'
    
    categories_response = requests.get(categories_url).json()
    for category_data in categories_response:
        Category.objects.get_or_create(
            id=category_data['id'],
            defaults={'name': category_data['name']}
        )
        
    products_response = requests.get(products_url).json()
    for product_data in products_response:
        Product.objects.get_or_create(
            id=product_data['id'],
            defaults={
                'name': product_data['name'],
                'price': product_data['price'],
                'nuts': product_data['nuts'],
                'image': product_data['image'],
                'vegetarian': product_data['vegeterian'],
                'spiciness': product_data['spiciness'],
                'category_id': product_data['categoryId']
            }
        )
    return render(request, 'myrestaurant/category_list.html', {'categories': Category.objects.all()})

def category_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    spiciness_level = request.GET.get('spiciness', None)
    if spiciness_level is not None and spiciness_level.isdigit():
        products = products.filter(spiciness=int(spiciness_level))

    if 'vegetarian' in request.GET and request.GET['vegetarian'] == 'on':
        products = products.filter(vegetarian=True)


    if 'nuts' in request.GET and request.GET['nuts'] == 'on':
        products = products.filter(nuts=True)    

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'myrestaurant/category_list.html', context)



def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()
    return render(request, 'myrestaurant/category_detail.html', {'category': category, 'products': products})



def basket_list(request):
    baskets = Basket.objects.all()
    return JsonResponse({'baskets': list(baskets.values())})

def update_basket(request):
    if request.method == 'POST':
        if 'update_quantity' in request.POST:
            item_id = request.POST['update_quantity']
            new_quantity = int(request.POST[f'quantity_{item_id}'])
        
            try:
                basket_item = BasketItem.objects.get(id=item_id)
                basket_item.quantity = new_quantity
                basket_item.save()
            except BasketItem.DoesNotExist:
                return JsonResponse({'error': 'Basket item does not exist'}, status=404)
        
        elif 'delete_item' in request.POST:
            item_id = request.POST['delete_item']
        
            try:
                basket_item = BasketItem.objects.get(id=item_id)
                basket_item.delete()
            except BasketItem.DoesNotExist:
                return JsonResponse({'error': 'Basket item does not exist'}, status=404)
        
        return redirect('basket') 

    return JsonResponse({'error': 'POST request required'})

def add_to_basket(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        basket, created = Basket.objects.get_or_create(name='Default Basket')


        basket_item, created = BasketItem.objects.get_or_create(
            basket=basket,
            product_id=product_id,
            defaults={'quantity': quantity}
        )

        if not created:
            basket_item.quantity += quantity
            basket_item.save()

        return redirect('basket')  

    return JsonResponse({'error': 'POST request required'})

def view_basket(request):
    basket, created = Basket.objects.get_or_create(name='Default Basket')
    items = basket.items.all()
    total_items = items.count()
    total_price = sum(item.product.price * item.quantity for item in items)

    context = {
        'basket': basket,
        'items': items,
        'total_items': total_items,
        'total_price': total_price,
    }
    return render(request, 'myrestaurant/basket.html', context)

def delete_product_from_basket(request, id):

    if request.method == 'DELETE':

        return JsonResponse({'message': 'Product deleted from basket'})

    return JsonResponse({'error': 'DELETE request required'})