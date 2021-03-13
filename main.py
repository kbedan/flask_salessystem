from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config.from_object(Development)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/sales'
db = SQLAlchemy(app)

@app.before_first_request
def create_table():
    db.create_all()

class Sale(db.Model):
    __tablename__ = "sales"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
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

if __name__ == '__main__':
   app.run(debug=True)