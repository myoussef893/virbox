from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,FloatField,PasswordField,EmailField,SubmitField,SelectField,MultipleFileField
from wtforms.validators import DataRequired,length
from models import User,db_session
department_choices = ['Super User','Managers','Customer Care','Finances','Sorting','Logistics',]
egypt_cities_choices = ["",
    "Cairo", "Alexandria", "Giza", "Shubra El-Kheima", "Port Said", "Suez", "Luxor", 
    "al-Mansura", "El-Mahalla El-Kubra", "Tanta", "Asyut", "Ismailia", "Fayyum", 
    "Zagazig", "Aswan", "Damietta", "Damanhur", "al-Minya", "Beni Suef", "Qena", 
    "Sohag", "Hurghada", "6th of October City", "Shibin El Kom", "Banha", 
    "Kafr el-Sheikh", "Arish", "Mallawi", "10th of Ramadan City", "Bilbais", 
    "Marsa Matruh", "Idfu", "Mit Ghamr", "Al-Hamidiyya", "Desouk", "Qalyub", 
    "Abu Kabir", "Kafr el-Dawwar", "Girga", "Akhmim", "Matareya"
]
payment_methods = ['','Bank Deposit/Transfer','Credit Card', 'Cash On Delivery']

lockers = [i.locker for i in db_session.query(User)]

## Checkout
class CheckoutForm(FlaskForm):
    full_name = StringField("Full Name:",validators=[DataRequired()])
    phone_number = StringField('Phone Number',validators=[DataRequired(),length(max=11,min=11)])
    address = StringField('Address:',validators=[DataRequired()])
    city= SelectField('City:',choices=egypt_cities_choices)
    landmark = StringField('Land Mark:')
    payment_method = SelectField('Payment Method:',choices=payment_methods,validators=[DataRequired()])
    submit = SubmitField('Order Now')
    



## Login 
class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

## Register
class RegisterationForm(FlaskForm): 
    full_name = StringField('Full Name',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    phone_number = IntegerField('Phone Number',validators=[DataRequired()])
    email = EmailField('email',validators=[DataRequired()])
    pwd = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Register')

## Package Creator
class PackageForm(FlaskForm): 
    tracking_number = StringField('Tracking Number',validators=[DataRequired()])
    items_count = StringField('Items Count in Package',validators=[DataRequired()])
    package_weight = FloatField('Package Weight:',validators=[DataRequired()])
    locker = SelectField('Locker of the User:',choices=lockers,validators=[DataRequired()])
    submit = SubmitField('Save')

# Item Form Editor

class ItemForm(FlaskForm): 
    pass