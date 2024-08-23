from app import app,redirect,render_template,current_user,request
from datetime import datetime as date
from forms import PackageForm 
from models import Items,Package,db_session

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
                item_weight = None,
                item_clearnace = None,
                item_category = None,
                scanning_date = str(date.today().date()),
                item_quantity = 1,
                locker = form.locker.data,
                status = 'Pending Review'
            )
            db_session.add(new_item)
            db_session.commit()
        return redirect('/cart')
    
    return render_template('./app_pages/employees_view/add_package.html',form=form)



# view all items
@app.route('/view_all/')
def view_all_items():
    all_items = db_session.query(Items)
    
    return render_template("./app_pages/employees_view/view_items.html",items = all_items)

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