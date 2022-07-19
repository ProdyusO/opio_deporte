"""View's module."""
# pylint: disable=E0402, C0103, W0612, C0200
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage

from ipware import get_client_ip
from .models import Product, Category, CartProduct, Customer
from .forms import CustomerForm
from .utilities import send_email_to_boss, send_email_to_customer


def index(request):
    """Main view"""
    categories = Category.objects.all()

    products = Product.objects.all()
    paginator = Paginator(products, 12)
    page_num = request.GET.get("page", 1)
    try:
        paginated_products = paginator.page(page_num)
    except EmptyPage:
        paginated_products = paginator.page(1)

    ip = get_client_ip(request)[0]
    customer, created = Customer.objects.get_or_create(name=ip)
    customer_orders = CartProduct.objects.filter(customer=customer, in_order=False)

    context = {
        "categories": categories,
        "customer_orders": customer_orders,
        "paginated_products": paginated_products,
    }

    return render(request, "layout/basic.html", context)


def category_detail_view(request, category_id):
    """Shows categories."""
    products = Product.objects.filter(category=category_id)

    ip = get_client_ip(request)[0]
    customer = get_object_or_404(Customer, name=ip)
    customer_orders = CartProduct.objects.filter(customer=customer, in_order=False)

    context = {"products": products, "customer_orders": customer_orders}

    return render(request, "shop/category.html", context)


def product_detail_view(request, pk):
    """Shows products."""
    product = Product.objects.get(pk=pk)

    ip = get_client_ip(request)[0]
    customer, created = Customer.objects.get_or_create(name=ip)
    customer_orders = CartProduct.objects.filter(customer=customer, in_order=False)

    context = {"product": product, "customer_orders": customer_orders}

    return render(request, "shop/detail.html", context)


def cart_product_view(request, pk):
    """Shows product into cart."""
    ip = get_client_ip(request)[0]

    cart_product = CartProduct()
    item = get_object_or_404(Product, pk=pk)
    cart_product.product = item
    cart_product.price = item.price
    cart_product.customer = get_object_or_404(Customer, name=ip)
    cart_product.save()

    messages.add_message(request, messages.SUCCESS, "Товар успішно додано до кошику")

    return redirect("index")


def cart_view(request):
    """Shows cart."""
    ip = get_client_ip(request)[0]

    owner = get_object_or_404(Customer, name=ip)
    customer_orders = CartProduct.objects.filter(customer=owner, in_order=False)

    price = 0
    for i in range(len(customer_orders)):
        price += customer_orders[i].total

    form = CustomerForm(request.POST or None)

    context = {"customer_orders": customer_orders, "total": price, "form": form}

    if request.method == "POST":
        if form.is_valid():
            owner = get_object_or_404(Customer, name=ip)
            owner.first_name = form.cleaned_data["first_name"]
            owner.last_name = form.cleaned_data["last_name"]
            owner.email = form.cleaned_data["email"]
            owner.phone_number = form.cleaned_data["phone_number"]
            owner.buying_type = form.cleaned_data["buying_type"]
            owner.comment = form.cleaned_data["comment"]
            owner.new_post = form.cleaned_data["new_post"]
            owner.save()
            for i in range(len(customer_orders)):
                customer_orders[i].in_order = True
                customer_orders[i].save()

            send_email_to_boss(owner, customer_orders, price)
            send_email_to_customer(owner, customer_orders, price)
            messages.add_message(
                request,
                messages.SUCCESS,
                "Дякуємо за замовлення, адміністрація сайту зв'яжеться з Вами найближчим часом!",
            )
            return redirect("index")

    return render(request, "shop/cart.html", context)


def change_quantity(request, pk):
    """Changes quantity of items."""
    cart_product = get_object_or_404(CartProduct, pk=pk)

    qwt = int(request.POST.get("qwt"))
    cart_product.quantity = qwt
    cart_product.save()

    return redirect("cart")


def delete_cart_product(request, pk):
    """Deletes item from cart."""
    item = get_object_or_404(CartProduct, pk=pk)
    item.delete()

    messages.add_message(request, messages.ERROR, "Видалено")

    return redirect("cart")
