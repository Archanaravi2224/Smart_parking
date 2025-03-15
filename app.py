from flask import Flask,redirect,url_for,render_template,request,session,flash,jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

import sqlite3

from sqlalchemy import column



from flask_cors import CORS

import json
import math


from create_dealers import get_dealer_by_id, get_slots_by_dealer, update_slot_status, update_total_slots,get_available_slots,get_all_slots

app = Flask(__name__)
CORS(app)


''''
dealer = get_dealer_by_id(session["dealer_id"])
slots = get_slots_by_dealer(session["dealer_id"])
update_slot_status(slot_id, "booked")  # Example usage
'''





app.register_blueprint(second,url_prefix="/source")

@app.route("/search_parking")
def search_parking():
    return render_template("search_parking.html")








# Initialize the SQLite database
def init_db():
    with sqlite3.connect('gps_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gps_data (
                name TEXT NOT NULL,
                
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                description  TEXT NOT NULL,
                price INTEGER NO NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parking_areas (
                name TEXT NOT NULL,
                
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                description  TEXT NOT NULL,
                price INTEGER NO NULL
            )
        ''')
       
        cursor.execute('''
          CREATE TABLE IF NOT EXISTS bookings (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          parking_id INTEGER,
          user_name TEXT,
          timing TEXT
          )
        ''')

        conn.commit()

# Route to serve the map page
@app.route('/source')
def source():
    return app.send_static_file('source.html')  # Ensure you have a map.html in your static folder



@app.route('/parking')
def parking():
    return render_template('parking.html')

    
 


@app.route('/booking-details')
def booking_details():
    name = request.args.get('name')
    distance = request.args.get('distance')
    return render_template('booking_details.html', name=name, distance=distance)


@app.route('/map_page')
def map_page():
    return render_template('combined_map.html')

@app.route('/dis')
def dis():
    return render_template('dis.html')

@app.route('/hotels')
def hotels():
    return render_template('hotels.html')


# Route to handle GPS data updates
@app.route('/gps/update', methods=['POST'])
def update_gps():
    data = request.get_json()  # Get the JSON data from the request
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    timestamp = data.get('timestamp')
    
    # Insert data into the database
    with sqlite3.connect('gps_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO gps_data (latitude, longitude, timestamp, description)
            VALUES (?, ?, ?, ?)
        ''', (latitude, longitude, timestamp, "User Location"))
        conn.commit()
    
    return jsonify({'status': 'success'}), 200  # Send a success response



@app.route('/api/parking', methods=['GET'])
def get_parking_areas():
    with sqlite3.connect('gps_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM parking_areas")
        parking_areas = cursor.fetchall()
    return jsonify(parking_areas)  # Return the parking areas as JSON


@app.route('/api/map_page', methods=['GET'])
def get_parking_data():
    conn = sqlite3.connect('gps_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, latitude, longitude,price FROM parking_areas')
    parking_data = cursor.fetchall()
    conn.close()

    # Convert to JSON
    return jsonify([{'name': row[0], 'lat': row[1], 'lng': row[2],'pri': row[3]} for row in parking_data])


'''
def get_distance(lat1, lng1, lat2, lng2):
    # Dummy function for now (replace with Haversine formula if needed)
    return ((lat1 - lat2) ** 2 + (lng1 - lng2) ** 2) ** 0.5  


@app.route('/booking')
def booking():
    user_lat = float(request.args.get('lat', 0))
    user_lng = float(request.args.get('lng', 0))

    conn = sqlite3.connect('gps_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, latitude, longitude, price FROM parking_areas")
    parking_spots = cursor.fetchall()
    conn.close()

    parking_list = []
    for spot in parking_spots:
        distance = get_distance(user_lat, user_lng, spot[2], spot[3])
        parking_list.append({
            "id": spot[0],
            "name": spot[1],
            "lat": spot[2],
            "lng": spot[3],
            "price": spot[4],
            "distance": distance
        })

    # Sort by distance & take 5 nearest spots
    nearest_parking = sorted(parking_list, key=lambda x: x["distance"])[:5]

    return render_template("booking.html", nearest_parking=nearest_parking)
'''


def get_distance(lat1, lon1, lat2, lon2):
    """Haversine Formula to calculate distance between two coordinates."""
    R = 6371  # Radius of Earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c  # Distance in km


@app.route('/get_parking_details', methods=['POST'])
def get_parking_details():
    """Fetch parking details based on nearest lat/lng from localStorage."""
    data = request.get_json()
    nearest_parking = data.get('nearestParking', [])

    if not nearest_parking:
        return jsonify([])  # No data

    conn = sqlite3.connect('gps_data.db')
    cursor = conn.cursor()

    parking_list = []
    for spot in nearest_parking:
        lat, lng = float(spot["lat"]), float(spot["lng"])

        # Use a small range to handle float precision issues
        cursor.execute("""
            SELECT id, name, price FROM parking_areas 
            WHERE latitude BETWEEN ? AND ? 
            AND longitude BETWEEN ? AND ?
        """, (lat - 0.0005, lat + 0.0005, lng - 0.0005, lng + 0.0005))

        result = cursor.fetchone()
        if result:
            parking_list.append({
                "id": result[0],
                "name": result[1],
                "price": result[2]
            })
        else:
            print(f"❌ No match found for: {lat}, {lng}")  # Debugging log

    conn.close()
    return jsonify(parking_list)


@app.route('/booking')
def booking():
    return render_template("booking.html")  # No need to pass nearest_parking now


@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    parking_id = request.form.get('parking_id')

    if not parking_id:
        return "Error: No parking spot selected", 400  # Handle missing ID

    try:
        parking_id = int(parking_id)  # Convert to integer to prevent SQL issues
    except ValueError:
        return "Error: Invalid parking ID format", 400

    print(f"🚀 Received Parking ID: {parking_id}")  # Debugging log

    conn = sqlite3.connect('gps_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, price, latitude, longitude FROM parking_areas WHERE id = ?", (parking_id,))
    parking_details = cursor.fetchone()
    conn.close()

    if parking_details:
        return render_template("confirm_booking.html", parking={
            "id": parking_id,
            "name": parking_details[0],
            "price": parking_details[1],
            "latitude": parking_details[2],
            "longitude": parking_details[3]
        })
    else:
        return "Error: Parking spot not found", 404
   
# Database initialization (Run once to create the table)
def create_table():
    conn = sqlite3.connect('gps_data.db')
    cursor = conn.cursor()
    

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings1 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        user_phone TEXT NOT NULL,
        parking_id INTEGER NOT NULL,
        slot_id INTEGER NOT NULL,
        parking_name TEXT NOT NULL,
        current_datetime_display TEXT DEFAULT (datetime('now', 'localtime')),  -- Stores the current booking timestamp
        start_time TEXT NOT NULL,  -- User-selected start time
        end_time TEXT NOT NULL,  -- Calculated end time (start_time + duration)
        price_per_hour REAL NOT NULL,
        duration INTEGER NOT NULL,
        total_price REAL NOT NULL,
        payment_method TEXT NOT NULL
        
    )
''')

    conn.commit()
    conn.close()


'''

# Route for Final Payment Page
@app.route('/final_payment/<int:parking_id>')
def final_payment(parking_id):
    # Fetch parking details from the database
    conn = sqlite3.connect('gps_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price FROM parking_areas WHERE id = ?", (parking_id,))
    parking = cursor.fetchone()
    conn.close()

    if parking:
        parking_data = {
            'id': parking[0],
            'name': parking[1],
            'price': parking[2]
        }
        return render_template('final_payment.html', parking=parking_data)
    else:
        return "Parking spot not found", 404
'''
# Route to handle payment confirmation and store data in the database
@app.route('/confirm_payment', methods=['POST'])
def confirm_payment():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_phone = request.form['user_phone']
        parking_id = request.form['parking_id']
        slot_id= request.form['slot_id']
        parking_name = request.form['parking_name']
        current_datetime_display = request.form['current_datetime_display']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        duration = int(request.form['duration'])
        price_per_hour = float(request.form['price_per_hour'])
        total_price = float(request.form['total_price'])
        payment_method = request.form['payment_method']

        # Insert booking into database
        conn = sqlite3.connect('gps_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bookings1 (user_name, user_phone, parking_id,slot_id, parking_name,   current_datetime_display,start_time,end_time,price_per_hour, duration, total_price, payment_method)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?)
        ''', (user_name, user_phone, parking_id,slot_id, parking_name,  current_datetime_display,start_time,end_time ,price_per_hour, duration, total_price, payment_method))
        conn.commit()
        conn.close()

        return render_template('confirm_payment.html', 
                               user_name=user_name, 
                               user_phone=user_phone,
                               slot_id=slot_id, 
                               parking_name=parking_name, 
                               current_datetime_display=current_datetime_display,
                               start_time=start_time,
                               end_time= end_time,
                               price_per_hour=price_per_hour, 
                               duration=duration, 
                               total_price=total_price, 
                               payment_method=payment_method)
       

@app.route('/view_bills')
def view_bills():
    conn = sqlite3.connect('gps_data.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM bookings1")
    bills = cursor.fetchall()
    
    conn.close()
    
    return render_template('view_bills.html', bills=bills)

# Route to delete a specific bill by ID
@app.route('/delete_bill/<int:bill_id>', methods=['POST'])
def delete_bill(bill_id):
    conn = sqlite3.connect('gps_data.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM bookings1 WHERE id = ?", (bill_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('view_bills'))


@app.route('/payment_slip', methods=['GET', 'POST'])
def payment_slip():
    bill_details = None  # Initialize variable for storing bill details

    if request.method == 'POST':
        user_phone = request.form['user_phone']  # Get phone number from form input
        
        # Connect to SQLite database and fetch the bill details
        conn = sqlite3.connect('gps_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings1 WHERE user_phone = ?", (user_phone,))
        bill_details = cursor.fetchone()
        conn.close()

    return render_template('payment_slip.html', bill=bill_details)  # Pass bill details to template







DATABASE = "gps_data.db"

# Function to connect to database
def connect_db():
    return sqlite3.connect(DATABASE)

# Route to display parking areas
@app.route("/parking_areas")
def parking_areas():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parking_areas")
    parking_spots = cursor.fetchall()
    conn.close()
    return render_template("parking_areas.html", parking_spots=parking_spots)

# Route to add a new parking area
@app.route("/add_parking", methods=["POST"])
def add_parking():
    if request.method == "POST":
        name = request.form["name"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        description = request.form["description"]
        price = request.form["price"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO parking_areas (name, latitude, longitude, description, price) VALUES (?, ?, ?, ?, ?)", 
                       (name, latitude, longitude, description, price))
        conn.commit()
        conn.close()

        flash("Parking area added successfully!", "success")
        return redirect(url_for("parking_areas"))

# Route to delete a parking area
@app.route("/delete_parking/<int:parking_id>", methods=["POST"])
def delete_parking(parking_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM parking_areas WHERE id=?", (parking_id,))
    conn.commit()
    conn.close()

    flash("Parking area deleted successfully!", "success")
    return redirect(url_for("parking_areas"))



app.secret_key="hello"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.permanent_session_lifetime=timedelta(minutes=5)

db= SQLAlchemy(app)

class users(db.Model):
    id =db.Column("id" ,db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

    def __init__(self,name,email):
        self.name=name
        self.email=email



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/view")
def view():
    return render_template("view.html",values=users.query.all())


@app.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    user = users.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully!", "success")
    else:
        flash("User not found!", "danger")
    
    return redirect(url_for("view"))


@app.route("/dashboard")
def dashboard():
        return render_template("dashboard.html")

@app.route("/adashboard")
def adashboard():
        return render_template("adashboard.html")




ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


@app.route("/admin", methods=["POST", "GET"])
def admin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = username   
            return render_template("adashboard.html")  
        else:
            flash("Invalid Credentials. Please try again.")  
            return render_template("alogin.html") 
    return render_template("alogin.html")   



@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent=True
        user = request.form["nm"]
        session["user"]=user

        found_user=users.query.filter_by(name=user).first()
        if found_user:
           session["email"]=found_user.email
        else:
            usr=users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("Login Successfull!!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!!")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user",methods=["POST","GET"])
def user():
    email = None
    if "user" in session:
        user=session["user"]

        if request.method == "POST":
            email=request.form["email"]
            session["email"]=email
            found_user=users.query.filter_by(name=user).first()
            found_user.email=email
            db.session.commit()
            flash("Email was saved!")
        else:
            if "email" in session:
                email=session["email"]
        return render_template("user.html",email=email)
    else:
        flash("You are not logged In!!")
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    flash("you have logged out","info")
    
    session.pop("user",None)
    session.pop("email",None)
    return redirect(url_for("login"))


@app.route("/alogout")
def alogout():
    flash("you have logged out","info")
    return render_template("alogin.html")















# Dealer Login Page
@app.route("/dlogin", methods=["GET", "POST"])
def dlogin():
    if request.method == "POST":
        dealer_id = request.form["dealer_id"]
        password = request.form["password"]

        dealer = get_dealer_by_id(dealer_id)
        if dealer and dealer["password"] == password:
            session["dealer_id"] = dealer_id
            return redirect("/ddashboard")
        else:
            return render_template("dlogin.html", error="Invalid ID or password.")

    return render_template("dlogin.html")

# Dealer Dashboard (Slot Management)
@app.route("/ddashboard")
def ddashboard():
    if "dealer_id" not in session:
        return redirect("/dlogin")

    dealer_id = session["dealer_id"]
    dealer = get_dealer_by_id(dealer_id)
    slots = get_slots_by_dealer(dealer_id)

    return render_template("ddashboard.html", dealer=dealer, slots=slots)

# Update Slot Status (SECURE POST REQUEST)
@app.route("/update_slot", methods=["POST"])
def update_slot():
    if "dealer_id" not in session:
        return redirect("/dlogin")

    slot_id = request.form.get("slot_id")
    status = request.form.get("status")

    if status not in ["available", "booked"]:
        return "Invalid status", 400

    update_slot_status(slot_id, status)
    return redirect("/ddashboard")

# Update Total Slots for Dealer
@app.route("/update_total_slots", methods=["POST"])
def update_total_slots_route():
    if "dealer_id" not in session:
        return redirect("/dlogin")

    dealer_id = session["dealer_id"]
    new_slot_count = int(request.form["total_slots"])

    update_total_slots(dealer_id, new_slot_count)
    return redirect("/ddashboard")

@app.route("/confirm_slots/<int:parking_id>")
def confirm_slots(parking_id):
    slots = get_all_slots(parking_id)  # Fetch all slots

    # Debugging: Print slot data to check if Flask is sending correct data
    print(f"🚀 Parking ID: {parking_id}, Slots Sent: {slots}")

    return render_template("confirm_slots.html", parking_id=parking_id, slots=slots)


@app.route("/book_slot/<int:slot_id>/<int:parking_id>")
def book_slot( slot_id,parking_id):
    """Update slot status and redirect to final payment page."""
    update_slot_status(slot_id, "booked")  # Update slot to 'booked'
    
    # Redirect to final payment page
    print(f"🚀 Parking ID: {parking_id}, Slots Sent: {slot_id}")
    return redirect(f"/final_payment/{parking_id}/{slot_id}")

@app.route("/final_payment/<int:slot_id>/<int:parking_id>")
def final_payment(slot_id, parking_id):
    """Fetch parking and slot details, then render final payment page."""
    
    conn = sqlite3.connect('gps_data.db')
    cursor = conn.cursor()
    
    # Fetch parking details
    cursor.execute("SELECT id, name, price FROM parking_areas WHERE id = ?", (parking_id,))
    parking = cursor.fetchone()

    # Fetch slot details
    cursor.execute("SELECT id FROM slots WHERE id = ?", (slot_id,))
    slot = cursor.fetchone()
    
    conn.close()

    # Debugging: Print the values retrieved
    print(f"🚀 Debug: Parking ID: {parking_id}, Slot ID: {slot_id}")
    print(f"🚀 Debug: Parking Data: {parking}")
    print(f"🚀 Debug: Slot Data: {slot}")

    if not parking:
        return "Parking spot not found", 404
    if not slot:
        return "Slot not found", 404

    # Convert fetched tuples to dictionaries for Jinja
    parking_data = {
        'id': parking[0],
        'name': parking[1],
        'price': parking[2]
    }

    slot_data = slot[0]

    return render_template("final_payment.html", slot=slot_data, parking=parking_data)


'''
'''

# Logout
@app.route("/dlogout")
def dlogout():
    session.clear()
    return redirect("/")
if __name__ == '__main__':
    init_db() 
    create_table()
    with app.app_context():
        db.create_all()
    app.run(debug=True)



   


