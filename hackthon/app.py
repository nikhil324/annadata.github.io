from flask import Flask,render_template,request,flash,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,login_required,logout_user,UserMixin,current_user
from datetime import datetime
import sqlite3
app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.secret_key="nikhil@1234" 
db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)

class Signup(UserMixin,db.Model):
    Unique_id=db.Column(db.INTEGER,primary_key=True)
    Password=db.Column(db.TEXT(50))
    Address=db.Column(db.TEXT(100))
    Village=db.Column(db.TEXT(50))
    State =db.Column(db.TEXT(100))
    Phone_no=db.Column(db.TEXT(50))
    Emailid=db.Column(db.TEXT(100))

    def get_id(self):
      return self.Unique_id
class Seller(UserMixin,db.Model):
    Commodity=db.Column(db.TEXT(50))
    Quantity=db.Column(db.TEXT(100))
    State=db.Column(db.TEXT(50))
    Date =db.Column(db.TEXT(100))
    Unique_id=db.Column(db.INTEGER,primary_key=True)
    Max_Price_Min_price =db.Column(db.TEXT(100))
    Contact_No=db.Column(db.TEXT(50))
    Email_id=db.Column(db.TEXT(100))
    Name=db.Column(db.TEXT(50))
    def __repr__(self):
      return "Commodity:{0}|Quantity:{1}|State:{2}|Date:{3}|Unique_id:{4}|Max_Price_Min_price:{5}|Contact_No:{6}|Email_id:{7}|Name:{8}".format(self.Commodity,self.Quantity,self.State,self.Date,self.Unique_id,self.Max_Price_Min_price,self.Contact_No,self.Email_id,self.Name)
    def get_id(self):
      return self.Unique_id
class Buyer(UserMixin,db.Model):
    Commodity=db.Column(db.TEXT(50))
    Quantity=db.Column(db.TEXT(100))
    State=db.Column(db.TEXT(50))
    Date =db.Column(db.TEXT(100))
    Farmer_Id=db.Column(db.INTEGER,primary_key=True)
    Your_Price =db.Column(db.TEXT(100))
    Contact_No=db.Column(db.TEXT(50))
    Farmer_Name=db.Column(db.TEXT(100))
    Name=db.Column(db.TEXT(50))
    Transport=db.Column(db.TEXT(50))

    def __repr__(self):
      return "Commodity:{0}|Quantity:{1}|State:{2}|Date:{3}|Farmer_Id:{4}|Your_price:{5}|Contact_No:{6}|Farmer_Name:{7}|Name:{8}|Transport:{9}".format(self.Commodity,self.Quantity,self.State,self.Date,self.Farmer_Id,self.Your_price,self.Contact_No,self.Farmer_Name,self.Name,self.Transport)
    def get_id(self):
      return self.Farmer_id


@login_manager.user_loader
def user_loader(Unique_id):
  return Seller.query.get(Unique_id)
@login_manager.user_loader
def user_loader(Unique_id):
  return Signup.query.get(Unique_id)
@app.route("/")
def home():
     sell=Seller.query.all()
     return render_template("index.html",sell=sell)
@app.route("/hindi")
def homehindi():
  sell=Seller.query.all()
  return render_template("hindi.html",sell=sell)
@app.route("/login")
def login():
	return render_template("login.html")
@app.route("/signup")
def signup():  
    return render_template("signup.html") 
@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=='POST':
            uniqueid = request.form.get('id')
            pas = request.form.get('Password')
            add = request.form.get('add')
            village = request.form.get('village')
            state = request.form.get('state')
            phone = request.form.get('phone')
            email = request.form.get('email')
            if uniqueid and pas:
              user = Signup.query.filter_by(Unique_id=uniqueid).first()    
              if user:
                  return "PLEASE ENTER THE UNIQUE ID THIS ID IS ALREADY EXIST"
              else:
                  sign=Signup(Unique_id=uniqueid,Password=pas,Address=add,Village=village,State=state,Phone_no=phone,Emailid=email)
                  db.session.add(sign)
                  db.session.commit()
                  return render_template("welcome.html")
            else:
                return "fill all required!!!"
@app.route("/choice",methods=['GET', 'POST'])
def choice():
    if request.method=='POST':
        ids = request.form.get('ids_no')
        pas = request.form.get('password')
        if ids and pas:
          user = Signup.query.filter_by(Unique_id=ids,Password=pas).first()    
          if user:
            login_user(user, remember=True)
            return render_template("choice.html")
          else:
            return "PLEASE ENTER THE VALID USERID OR PASSWORD"
        else:
          return 'PLEASE FILL ALL REQUIRED'
@app.route('/remove')
def logout():
  logout_user()
  return render_template('index.html')              
@app.route('/sell')
def sell():
    return render_template('seller.html')  
@app.route("/seller",methods=['GET','POST'])
def seller():
    if request.method=='POST':
            commod = request.form.get('Commodity')
            quant = request.form.get('Quantity')
            state = request.form.get('State')
            date = request.form.get('Date')
            uni_id = request.form.get('id')
            max_min = request.form.get('Max-Min Price')
            no = request.form.get('Contact')
            email = request.form.get('email')
            name = request.form.get('name')
            if commod and uni_id :
                  sell=Seller(Commodity=commod,Quantity=quant,State=state,Date=date,Unique_id=uni_id,Max_Price_Min_price=max_min,Contact_No=no,Email_id=email,Name=name)                  

                  db.session.add(sell)
                  db.session.commit()
                  return render_template("sell_wel.html")
            else:
                return "fill all required!!!"                                               	
@app.route('/buy')
def buy():
    return render_template('buyer.html')
@app.route('/buyer',methods=['GET', 'POST'])
def buyer():
	 if request.method=='POST':
	 	ids = request.form.get('ids')
	 	user = Seller.query.filter_by(Unique_id=ids).first()
	 	if user:
	 		login_user(user, remember=True)
	 		return render_template("buyform.html")
	 	else:
	 		return "PLEASE ENTER THE VALID USERID"
@app.route("/buyform",methods=['GET','POST'])
def buyform():
    if request.method=='POST':
            commod = request.form.get('Commodity')
            quant = request.form.get('Quantity')
            state = request.form.get('State')
            date = request.form.get('Date')
            uni_id = request.form.get('id')
            price = request.form.get('cost')
            no = request.form.get('Contact')
            farmer = request.form.get('farmer')
            name = request.form.get('name')
            transport = request.form.get('transport')
            if farmer and uni_id :
                  buy=Buyer(Commodity=commod,Quantity=quant,State=state,Date=date,Farmer_Id=uni_id,Your_Price=price,Contact_No=no,Farmer_Name=farmer,Name=name,Transport=transport)                  

                  db.session.add(buy)
                  db.session.commit()
                  return render_template("sell_wel.html")
            else:
                return "fill all required!!!"               
@app.route('/selllist')
def selllist():
     sell=Seller.query.all()
     return render_template("selllist.html",sell=sell)
@app.route('/buylist')
def buylist():
     buy=Buyer.query.all()
     return render_template("buylist.html",buy=buy)
@app.route('/disrate')
def disrate():
     return render_template("districrate.html")         
@app.route('/dismandies')
def dismandies():
     return render_template("dismandies.html")
@app.route('/gallery')      
def gallery():
    return render_template("gallery.html")     

if __name__ == '__main__':          
	app.run(debug=True)