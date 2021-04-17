from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config.from_object(Development)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://liexcoytcosxnj:34737de85c83796cc8e13eeb1ddd34ca09d8528c6cace23deffda0f91f08fae0@ec2-52-209-134-160.eu-west-1.compute.amazonaws.com:5432/d241ijf9g2avvh'
db = SQLAlchemy(app)

@app.before_first_request
def create_table():
    db.create_all()

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    quantity = db.Column(db.Integer, unique=False)
    buying_price = db.Column(db.Integer, unique=False)
    selling_price = db.Column(db.Integer, unique=False)

class Sale(db.Model):
    __tablename__ = "sales"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    quantity = db.Column(db.Integer, unique=False,  nullable=False)
    buying_price= db.Column(db.Integer, unique=False, nullable=False)
    selling_price= db.Column(db.Integer, unique=False, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def salesitem():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        buying_price = request.form['buying_price']
        selling_price = request.form['selling_price']

        record = Sale(name=name, quantity=quantity,
                      buying_price=buying_price, selling_price=selling_price)
        db.session.add(record)
        db.session.commit()
        print("Your test is successful")
        return redirect(url_for('salesitem'))
    
    records=Sale.query.all()
    return render_template('items.html', records = records) 

@app.route('/sales', methods = ['POST'])
def saleslisting():
    if request.method == 'POST':
        item_id = request.form['item_id']
        quantity = request.form['item_quantity']
        print("test", item_id, quantity)

        item_to_edit = Item.query.filter_by(id = item_id).first()
        item_to_edit.item_quantity = int(item_to_edit.item_quantity) - int(quantity)

        if int(item_to_edit.item_quantity) - int(quantity) <= 0:
            print("Quantity entered is more than the stock available")
            return redirect(url_for('salesitem'))
            
        db.session.add(item_to_edit)
        db.session.commit()        

        a = Sale(item_id = item_id, quantity = quantity)
        db.session.add(a)
        db.session.commit()
        print("Record successfully added")
        
        return redirect(url_for('itemlisting'))   

if __name__ == '__main__':
   app.run(debug=True)