from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopping_list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ShoppingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(10), nullable=False)

# Crea le tabelle prima di avviare l'app
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    shopping_list = ShoppingItem.query.all()
    return render_template('index.html', shopping_list=shopping_list)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    quantity = request.form['quantity']
    unit = request.form['unit']

    # Validazione della quantità in base all'unità
    try:
        quantity = float(quantity)
        if quantity <= 0:
            raise ValueError("La quantità deve essere maggiore di zero.")
        
        if unit == 'pezzi' and quantity != int(quantity):
            raise ValueError("Se l'unità è 'pezzi', la quantità deve essere un numero intero.")
        
        if unit == 'kg' and quantity == int(quantity):
            raise ValueError("Se l'unità è 'kg', la quantità deve essere un numero decimale.")
        
        new_item = ShoppingItem(name=name, quantity=quantity, unit=unit)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))
    except ValueError as e:
        return render_template('index.html', error=str(e), shopping_list=ShoppingItem.query.all())

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    item = ShoppingItem.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        unit = request.form['unit']
        
        # Validazione della quantità in base all'unità
        try:
            quantity = float(quantity)
            if quantity <= 0:
                raise ValueError("La quantità deve essere maggiore di zero.")
            
            if unit == 'pezzi' and quantity != int(quantity):
                raise ValueError("Se l'unità è 'pezzi', la quantità deve essere un numero intero.")
            
            if unit == 'kg' and quantity == int(quantity):
                raise ValueError("Se l'unità è 'kg', la quantità deve essere un numero decimale.")
            
            item.name = name
            item.quantity = quantity
            item.unit = unit
            db.session.commit()
            return redirect(url_for('index'))
        except ValueError as e:
            return render_template('edit.html', error=str(e), item=item)

    return render_template('edit.html', item=item)

@app.route('/delete/<int:id>')
def delete(id):
    item = ShoppingItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
