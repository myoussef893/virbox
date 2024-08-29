from app import app,session,render_template,current_user,redirect
from models import Items,db_session,Orders
from forms import CheckoutForm
from datetime import datetime as date

## view the cart
@app.route('/cart', methods= ["GET","POST"])
def cart():
    cart_items = session.get('cart',[])
    items_count = 0 
    total_price = 0 
    for i in cart_items: 
        total_price += i['price']
        items_count += 1
    return render_template('./app_pages/cart.html',
                           cart = cart_items,
                           price = total_price,
                           count = items_count
                           )


## add to cart 
@app.route('/cart/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    cart_items = session.get('cart',[])
    item = db_session.query(Items).filter_by(id = item_id).first()
    cart_items.append(
        {
            'id':item.id,
            'title':f"Item: {item.id}",
            'description': f'weight of the item is: {item.item_weight} kg',
            'weight': item.item_weight,
            'price': item.item_weight*10,
        }
    )
    item.item_quantity -=1
    db_session.commit()
    session['cart'] = cart_items
    return redirect('/view_all')


## remove from cart 
@app.route('/cart/remove_from_cart/<int:item_id>')
def remove_from_cart(item_id):
    cart_items = session.get('cart',[])
    updated_cart_items = [item for item in cart_items if item['id']!= item_id]
    revert_quantity = db_session.query(Items).filter_by(id = item_id).first()
    revert_quantity.item_quantity +=1
    db_session.commit()
    session['cart'] = updated_cart_items
    return redirect('/cart')

## clear cart 
@app.route("/cart/clear_cart")
def clear_cart():
    cart_items = session.get('cart',[])
    for i in cart_items: 
        item = db_session.query(Items).filter_by(id = i['id']).first()
        item.item_quantity+=1

    db_session.commit()
    session['cart'] = []
    return redirect('/cart')

## checkout
@app.route('/checkout',methods=['GET',"POST"])
def checkout(): 
    
    form = CheckoutForm()
    cart = session.get('cart',[])
    price = 0 
    weight = 0 
    for i in cart: 
        price += i['price']
        weight +=i['weight']


    if form.validate_on_submit(): 
        new_order = Orders(
            order_date = str(date()),
            items_count = len([i for i in cart]),
            order_weight = weight,
            total_price = price,
            locker = current_user.locker,
            full_name= form.full_name.data,
            phone_number = form.phone_number.data,
            address = form.address.data +" "+form.landmark.data,
            payment_method = form.payment_method.data,
            city = form.city.data,
            status = "Processing"
        )
        db_session.add(new_order)
        db_session.commit()
        clear_cart()
        return redirect('/successful_order')

    return render_template('./app_pages/checkout.html',form=form)


@app.route('/successful_order')
def successful_order(): 
    return '<h1> Order successfully Placed.</h1> '

@app.route('/failed-order')
def failed_order(): 
    return '<h1> Order Failed, Please Try Again. <h1>'