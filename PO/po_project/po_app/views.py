from django.shortcuts import render, redirect
from .models import *

# Create your views here.

def offert(request):
    items = []

    basket = getBasketInUse()

    if request.method == "POST":
        vars = request.POST
        type = vars["formtype"]

        if type == "search":
            filter_value = vars["searchValue"]
            if filter_value == "":
                items = []
            else:
                items = Stock.objects.filter(name=filter_value).all().order_by("name")
        elif type == "add":
            item_id = vars["item_id"]
            added_item = Stock.objects.get(id=item_id)
            if added_item.left - 1 >= 0:
                added_item.left = added_item.left - 1
                added_item.save()
                basket_item = None
                try:
                    basket_item = StockInBasket.objects.get(basket=basket, item=added_item)
                except Exception:
                    StockInBasket.objects.create(basket=basket, item=added_item)
                    basket_item = StockInBasket.objects.get(basket=basket, item=added_item)
                basket_item.number = basket_item.number + 1
                basket_item.save()

    if items == []:
        items = Stock.objects.all().order_by('name')

    data = {"items": items}
    return render(request, "offert.html", data)

def basket(request, error=None):

    items = []

    basket = getBasketInUse()

    if request.method == "POST":
        vars = request.POST
        type = vars["formtype"]

        if type == "add":
            item_id = vars["item_id"]
            basket_item = StockInBasket.objects.get(id=item_id)
            if basket_item.item.left - 1 >= 0:
                basket_item.item.left = basket_item.item.left - 1
                basket_item.item.save()
                basket_item.number = basket_item.number + 1
                basket_item.save()
        elif type == "delete":
            item_id = vars["item_id"]
            basket_item = StockInBasket.objects.get(id=item_id)
            basket_item.item.left = basket_item.item.left + 1
            basket_item.item.save()
            basket_item.number = basket_item.number - 1
            if basket_item.number == 0:
                basket_item.delete()
            else:
                basket_item.save()
        elif type == "deleteAll":
            for basket_item in StockInBasket.objects.filter(basket=basket).all():
                basket_item.item.left = basket_item.item.left + basket_item.number
                basket_item.item.save()
                basket_item.delete()

    items = StockInBasket.objects.filter(basket=basket).all().order_by("item__name")

    total_price = 0
    for item in  items:
        total_price += item.number * item.item.price

    basket.total_price = total_price
    basket.save()

    data = {"items": items, "sum": total_price, "error": error}

    return render(request, "basket.html", data)

def order(request):

    basket = None
    basket_state = None

    try:
        basket_state = BasketState.objects.get(name="W realizacji")
    except Exception:
        BasketState.objects.create(name="W realizacji")
        basket_state = BasketState.objects.get(name="W realizacji")

    try:
        basket = Basket.objects.get(state=basket_state)
    except Exception:
        Basket.objects.create(state=basket_state)
        basket = Basket.objects.get(state=basket_state)

    data = {"sum": basket.total_price}

    return render(request, "order.html", data)

def order_basket(request):

    # TODO Implement payment
    error = False
    if error:
        return redirect('basket_error', error='Błąd płatności')

    basket = getBasketInUse()

    if request.method == "POST":
        vars = request.POST
        delivery_type = ""
        payment_method = vars["payment_method"]

        try:
            vars["deliveryTypeDelivery"]
            delivery_type = "delivery"
        except KeyError:
            vars["deliveryTypeTakeaway"]
            delivery_type = "takeaway"

        delivery = None
        payment = None

        if delivery_type == "delivery":
            city=vars["cityAddress"]
            street=vars["streetAddress"]
            home=vars["homeNumber"]
            address = None

            try:
                address = Address.objects.get(city=city, street=street, number=home)
            except Exception:
                Address.objects.create(city=city, street=street, number=home)
                address = Address.objects.get(city=city, street=street, number=home)

            delivery_state = None

            try:
                delivery_state = DeliveryState.objects.get(name="W realizacji")
            except Exception:
                DeliveryState.objects.create(name="W realizacji")
                delivery_state = DeliveryState.objects.get(name="W realizacji")
            
            Delivery.objects.create(address=address, state=delivery_state)
            delivery = Delivery.objects.get(address=address, state=delivery_state)

        # TODO Implement payment
        if payment_method == "online":
            receipt_number = "DEFAULT"
            Bill.objects.create(receipt_number=receipt_number)
            payment = Bill.objects.get(receipt_number=receipt_number)
        
        order_state = None

        try:
            order_state = OrderState.objects.get(name="W realizacji")
        except Exception:
            OrderState.objects.create(name="W realizacji")
            order_state = OrderState.objects.get(name="W realizacji")

        date = vars["datepicker"]

        Order.objects.create(state=order_state, delivery=delivery, receipt=payment, basket=basket, date=date)     
        
    new_basket_state = None

    try:
        new_basket_state = BasketState.objects.get(name="Zrealizowany")
    except Exception:
        BasketState.objects.create(name="Zrealizowany")
        new_basket_state = BasketState.objects.get(name="Zrealizowany")

    basket.state = new_basket_state
    basket.save()

    return redirect('basket')

def getBasketInUse():

    basket = None
    basket_state = None

    try:
        basket_state = BasketState.objects.get(name="W realizacji")
    except Exception:
        BasketState.objects.create(name="W realizacji")
        basket_state = BasketState.objects.get(name="W realizacji")

    try:
        basket = Basket.objects.get(state=basket_state)
    except Exception:
        Basket.objects.create(state=basket_state)
        basket = Basket.objects.get(state=basket_state)

    return basket
