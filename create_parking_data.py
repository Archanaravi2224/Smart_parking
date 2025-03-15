import sqlite3
def create_parking_data():
    parking_data = [
        ("KAK Parking", 11.015703591182035, 76.96737275633905, "Kavitha Theatre, Nehru St, Ram Nagar, Coimbatore, Tamil Nadu 641009", 100),
        ("Corporation Parking Lot", 11.017183486686537, 76.96565502165376, "Cross Cut Rd, Peranaidu Layout, Ram Nagar, Gandhipuram, Coimbatore, Tamil Nadu 641009", 110),
        ("Myan Parking", 11.016139953945371, 76.98002575854734, "Bharathiyar Rd, Siddhapudur, Pappanaickenpalayam, Coimbatore, Tamil Nadu 641037", 100),
        ("Coimbatore Corporation Paid Parking", 11.007364950582415, 76.96022370756067, "Puthiyavan Nagar, Sukrawar Pettai, R.S. Puram, Coimbatore, Tamil Nadu 641001", 120),
        ("Pay parking", 10.99579157163397, 76.95851693855407, "Town Hall, Coimbatore, Tamil Nadu 641001", 120),
        ("Corporation Parking Lot", 10.994535480659211, 76.96373995179958, "Town Hall, Coimbatore, Tamil Nadu 641001", 130),
        ("SKR Nagar car parking", 11.039977488780211, 76.94199662111446, "SKR Nagar Park Rd, Koundampalayam, Coimbatore, Tamil Nadu 641025", 120),
        ("Airport Parking Area", 11.031201517590013, 77.03861088063583, "Bipha Ayurveda, Airport Rd, Peelamedu, Civil Aerodrome Post, Coimbatore, Tamil Nadu 641014", 120),
        ("Parking", 10.896118172829361, 76.9957678870879, "Hindusthan College Rd, Malumichampatti, Tamil Nadu 641050", 100),
        ("SAI PARKING JKT", 10.896672561822408, 76.92293997380932, "Sai Parking, Thirumayam Palayam Rd, R.F, Ettimadai, Coimbatore, Tamil Nadu 641105", 110),
        ("Car parking", 10.941170724850577, 76.95555563439953, "BK Pudur, Sugunapuram East, Kuniyamuthur, Tamil Nadu 641008", 120),
        ("KKS CAR PARKING", 10.964765527830433, 76.97066183488775, "Sundarapuram, Coimbatore, Kurichi, Tamil Nadu", 120),
        ("Balaji or by pass parking", 10.98227081275992, 76.95252225133493, "XWPW+3J Selvapuram, Tamil Nadu", 110),
        ("Gandhipuram Bus Stand", 11.0168, 76.9676, "Central bus stand parking for commuters.", 110),
        ("Crosscut Road Parking", 11.0155, 76.9682, "Street parking in retail area.", 120),
        ("City Centre Mall", 11.0140, 76.9526, "Mall parking for visitors.", 130),
        ("Prozone Mall", 11.0756, 76.9925, "Large parking near IT parks and residents.", 120),
        ("Saravanampatti Bus Stand", 11.0956, 76.9553, "Small parking area near the stand.", 110),
        ("Keeranatham IT Park", 11.1015, 77.0189, "Parking for IT professionals.", 100),
        ("Singanallur Bus Stand", 11.0008, 77.0245, "Public parking for travelers.", 120),
        ("Tidel Park Coimbatore", 11.0284, 76.9310, "IT park parking.", 130),
        ("Fun Republic Mall", 11.0278, 76.9460, "Mall parking for visitors.", 120),
        ("Annur Town Bus Stand", 11.2366, 77.1307, "Small parking near the bus stand.", 120),
        ("Local Market Parking, Annur", 11.2370, 77.1310, "Street parking near shops.", 130),
        ("Annur Petrol Station", 11.2381, 77.1325, "Nearby lot with parking.", 120),
        ("Maruthamalai Temple Parking", 11.0596, 76.8828, "Parking near the temple.", 110),
        ("Vadavalli Market", 11.0373, 76.8971, "Local market parking.", 110),
        ("Ukkadam Bus Terminal", 10.9918, 76.9601, "Parking for bus travelers.", 100),
        ("Ukkadam Fish Market", 10.9925, 76.9612, "Street parking near market.", 110),
        ("Ukkadam Bypass Parking", 10.9890, 76.9598, "Highway-side parking.", 120),
        ("Perur Temple", 10.9865, 76.9335, "Parking for temple visitors.", 100),
        ("Perur Lake View", 10.9830, 76.9300, "Small lot near scenic area.", 110),
        ("Kovaipudur Bus Terminal", 10.9541, 76.9182, "Small parking for commuters.", 100),
        ("Community Hall Parking, Kovaipudur", 10.9520, 76.9160, "Public space parking.", 120),
        ("Madhampatti Village Square", 11.0121, 76.8484, "Parking near local businesses.", 100),
        ("Railway Station Parking", 11.0016, 76.9661, "Main station parking.", 120),
        ("Coimbatore North Railway Station", 11.0169, 76.9705, "Limited parking space.", 110),
        ("Isha Yoga Center", 11.0169, 76.8191, "Large parking for visitors.", 110),
        ("Tamil Nadu State Transport", 11.0203, 76.9522, "Parking near State Transport", 140),
        ("CBE IT Park", 11.0301, 76.9573, "Parking at CBE IT Park", 130),
        ("Ramnagar Parking", 11.0183, 76.9735, "Parking available in Ramnagar", 130),
        ("Aathupalam Parking", 11.0421, 76.9794, "Parking near Aathupalam", 120),
        ("NGM Park", 11.0143, 76.9700, "Parking at NGM Park", 130),
        ("Kothari Buildings", 11.0198, 76.9740, "Parking available at Kothari Buildings", 140),
        ("Central Bus Stand", 11.0261, 76.9550, "Parking near Central Bus Stand", 130),
        ("R.K. Shopping Centre", 11.0315, 76.9465, "Parking available at R.K. Shopping Centre", 120),
        ("Ganesh Nagar", 11.0365, 76.9599, "Parking at Ganesh Nagar", 110),
        ("Coimbatore Corporation Park", 11.0162, 76.9470, "Parking at Corporation Park", 100),
        ("SRS Mall", 11.0228, 76.9594, "Parking available at SRS Mall", 120),
        ("V.O. Chidambaram Road", 11.0190, 76.9665, "Parking on V.O. Chidambaram Road", 120),
        ("Sree Ayyappa Temple", 11.0289, 76.9709, "Parking near Sree Ayyappa Temple", 130),
        ("Codissia Trade Centre", 11.0240, 76.9705, "Parking at Codissia Trade Centre", 130),
        ("Eachanari Bus Stand", 10.9404, 76.8978, "Parking available near Eachanari Bus Stand.", 120),
        ("Eachanari Temple Parking", 10.9387, 76.8953, "Parking for temple visitors.", 140),
        ("Eachanari Market Parking", 10.9399, 76.8967, "Street parking near local shops.", 120),
        ("Kinathukadavu Railway Station", 10.7568, 77.0020, "Small parking lot for passengers.", 140),
        ("Kinathukadavu Bus Stand", 10.7550, 76.9950, "Parking near the bus stand.", 140),
        ("Kinathukadavu Market", 10.7580, 77.0045, "Available parking near the market.", 130),
        ("Alandhurai Bus Stand", 11.0314, 76.9535, "Parking available at the bus stand.", 120),
        ("Alandhurai Village Parking", 11.0325, 76.9510, "Local parking for visitors.", 100),
        ("Alandhurai Temple Parking", 11.0340, 76.9500, "Parking for temple visitors.", 100),
        ("Thudiyalur Bus Stand", 11.0325, 76.9293, "Parking available at Thudiyalur Bus Stand.", 120),
        ("Thudiyalur Market", 11.0315, 76.9299, "Street parking near local shops.", 130),
        ("Thudiyalur Park", 11.0340, 76.9330, "Public park parking.", 100),
        ("Peelamedu Market", 11.0270, 77.0203, "Street parking near market.", 120),
    ]


    with sqlite3.connect('gps_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM parking_areas')
        cursor.executemany('''
            INSERT INTO parking_areas(name, latitude, longitude, description,price)
            VALUES (?, ?, ?, ?,?)
        ''', parking_data)
        conn.commit()




if __name__ == '__main__':
    create_parking_data()


