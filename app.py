import sqlite3
from flask import Flask, render_template, request, g
from logics import get_info_from_excel
app = Flask(__name__)

# Function to connect to the database
def get_db():
    print(g,'888888888888888888888888888888')
    if 'db' not in g:
        g.db = sqlite3.connect('dockets.db')
        g.db.execute('''
            CREATE TABLE IF NOT EXISTS dockets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                start_time TEXT,
                end_time TEXT,
                hours_worked INTEGER,
                rate_per_hour REAL,
                supplier_name TEXT,
                purchase_order TEXT
            )
        ''')
        g.db.commit()
    return g.db



@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/create_docket', methods=['GET', 'POST'])
def create_docket():
    #retrieving supplier name and purchase order
    supllier_dict = get_info_from_excel.get_info(r'logics\export29913.xlsx')

    if request.method == 'POST':
        name = request.form['name']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        hours_worked = request.form['hours_worked']
        rate_per_hour = request.form['rate_per_hour']
        supplier_name = request.form['supplier_name']
        purchase_order = request.form['purchase_order']
        
        db = get_db()
        db.execute("INSERT INTO dockets (name, start_time, end_time, hours_worked, rate_per_hour, supplier_name, purchase_order) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (name, start_time, end_time, hours_worked, rate_per_hour, supplier_name, purchase_order))
        db.commit()

        # Redirect to the list of dockets after successful submission
        return render_template('success.html')

    return render_template(r'form.html',suppliers = supllier_dict)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/view_dockets')
def view_dockets():
    db = get_db()
    cursor = db.execute("SELECT * FROM dockets")
    dockets = cursor.fetchall()
    print(dockets,'ppppppppppppp')
    return render_template('dockets.html', dockets=dockets)

if __name__ == '__main__':
    app.run(debug=True)
