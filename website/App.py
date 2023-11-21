from flask import Flask, render_template, request

app = Flask(__name__)

inventory = []  


@app.route('/')
def index():
    return render_template('index.html', inventory=inventory)


@app.route('/add_item', methods=['POST'])
def add_item():
    item_name = request.form.get('item_name')
    category = request.form.get('category')
    description = request.form.get('decription')
    quantity = request.form.get('quantity')

    
    if item_name and quantity:
        inventory.append({'item_name': item_name, 'category': category,'description': description, 'quantity': quantity})

    return render_template('index.html', inventory=inventory)


if __name__ == '__main__':
    app.run(debug=True)
