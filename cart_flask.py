from app import app,session,render_template,current_user,redirect
from models import Items,db_session

## view the cart
@app.route('/cart', methods= ["GET","POST"])
def cart():
    cart_items = session.get('cart',[])
    items_count = 0 
    total_price = 0 
    for i in cart_items: 
        total_price += i['price']
        items_count += 1
    return render_template('./app_pages/cart.html',cart= cart_items,user=current_user,price= total_price,count = items_count)


## add to cart 
@app.route('/cart/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    cart_items = session.get('cart',[])
    item = db_session.query(Items).filter_by(id = item_id).first()
    cart_items.append(
        {
            'id':item.id,
            'title':f"Item: {item.id}",
            'description': f'weight of the item is;{item.item_weight}',
            'weight': item.item_weight,
            'price': float(item.item_weight*27),
        }
    )
    item.item_quantity -=1
    db_session.commit()
    return redirect('/dashboard')


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
@app.route('/checkout')
def checkout(): 
    pass

