from app import app,redirect,render_template,current_user,request,session,flash
from datetime import datetime as date
from forms import PackageForm 
from models import Items,Package,db_session,IntBox


#add item to base 
@app.route('/add_new_item',methods = ['GET','POST'])
def add_item():
    form = PackageForm()
    if form.validate_on_submit():
        new_package = Package(
            scanning_date = str(date.today().date()),
            tracking_number = form.tracking_number.data,
            items_count = form.items_count.data,
            weight = form.package_weight.data,
            locker = form.locker.data,
        )
        print(form.items_count.data)
        db_session.add(new_package)
        db_session.commit()
        
        for item in range(int(form.items_count.data)):
            new_item = Items(
                tracking_number = form.tracking_number.data,
                item_weight = float(float(form.package_weight.data)/int(form.items_count.data)),
                item_clearnace = None,
                item_category = None,
                scanning_date = str(date.today().date()),
                item_quantity = 1,
                locker = form.locker.data,
                status = 'Origin Warehouse.'
            )
            db_session.add(new_item)
            db_session.commit()
        return redirect('/view_all')
    
    return render_template('./app_pages/employees_view/add_package.html',form=form)

# view locker items
@app.route('/my-locker')
def locker_items():
    page = int(request.args.get('page', 1))
    per_page = 10

    all_items = db_session.query(Items).filter_by(item_quantity=1)
    paginated_items = all_items.offset((page - 1) * per_page).limit(per_page)

    items = paginated_items.all()
    total_pages = (all_items.count() + per_page - 1) // per_page

    return render_template("./app_pages/locker.html", items=items, total_pages=total_pages)

# view all the items, as employee
@app.route('/view_all/')
def view_all_items():
    intlBox = session.get('i_box',[])
    page = int(request.args.get('page', 1))
    per_page = 10

    all_items = db_session.query(Items).filter_by(item_quantity=1)
    paginated_items = all_items.offset((page - 1) * per_page).limit(per_page)

    items = paginated_items.all()
    total_pages = (all_items.count() + per_page - 1) // per_page

    counter=[i['id'] for i in intlBox]
    return render_template("./app_pages/employees_view/view_items.html", items=items, total_pages=total_pages,counter=len(counter))

#remove item from base 
@app.route('/delete_item/<int:item_id>')
def delete_item(item_id):
    item = db_session.query(Items).filter_by(id = item_id).first()
    db_session.delete(item)
    db_session.commit()    
    return redirect('/view_all')

#update item in base 
@app.route('/update_item/<int:item_id>',methods=['POST','GET'])
def update_item(item_id): 
    item_id = db_session.query(Items).filter_by(id=item_id).first()
    if request.method == 'post': 
        item_id.item_weight=request.args.get('weight_input')
    db_session.commit()
    return redirect('/view_all')

# add items to international box: 
@app.route('/add_to_intlbox/<int:item_id>',methods=['Get','Post'])
def addToIntlBox(item_id):
    intlBox = session.get('i_box',[])
    item = db_session.query(Items).filter_by(id = item_id).first()
    if item.status == "Origin Warehouse.":
        intlBox.append(
            {
                'id':item.id,
                'title':f"Item: {item.id}",
                'description': f'weight of the item is: {item.item_weight} kg',
                'weight': item.item_weight,
            }
        )
        item.status = "In International Box"
        db_session.commit()
        session['i_box'] = intlBox
    else: 
        flash()    

    return redirect('/view_all')

@app.route('/create_international_box',methods = ['GET','POST'])
def create_international_box(): 
    intlBox = session.get('i_box',[])
    total_weight = 0
    items_count = 0

    for i in intlBox: 
        total_weight += i['weight']
        items_count += 1 

    if request.method == 'Post': 
        new_box = IntBox(
            tracking_number = request.form['tn'],
            total_weight = total_weight,
            creation_date = str(date()),
            items_count = items_count,
            shipping_company = request.args['shipping-company'] ,
            box_value = request.form['value']

        )
    return render_template('./app_pages/employees_view/wrap_intl_box.html')

@app.route('/view_item',methods=['POST','GET'])
def view_item(item_id): 
    
    pass