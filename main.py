import sqlite3
from flask import Flask, request,json
from  db_utilities import *

app = Flask(__name__)

#http://localhost:5000/GetBookingList/'2017-05-08'
@app.route('/GetBookingList', methods=['GET'])
@app.route('/GetBookingList/<date>', methods=['GET'])
def Booking(date=None):
    query =''
    query +='select '
    query +=    'C.CAB_NAME,'
    query +=    'C.CAB_TYPE,'
    query +=    'B.START_DATE_TIME,'
    query +=    'B.END_DATE_TIME,'
    query +=    'B.STATUS,'
    query +=    'B.SOURCE,'
    query +=    'B.DESTINATION,'
    query +=    'U.USER_NAME,'
    query +=    'U.USER_TYPE,'
    query +=    'U.CUSTOMER_NAME,'
    query +=    'U.CUSTOMER_ADDRESS,'
    query +=    'U.CUSTOMER_PHONE'

    query += ' from '
    query +=    'BookingData as B '
    query +=    'join CabData as C using(CAB_ID) '
    query +=    'join UserData as U using(USER_ID) '

    if(date):
        query += 'where '
        query +=    "START_DATE_TIME >= "+ date

    json_output = json.dumps(run_query(query))
    return json_output, 201

#Booking
#http://localhost:5000/UpdateBooking/2017-05-13,10:00,2017-05-13,11:00,'Audi 1','',1,3,'Airport','Banaswadi'

#Blocking
#http://localhost:5000/UpdateBooking/2017-05-15,10:00,2017-05-15,11:00,'Audi%201','',2,1,'',''
@app.route('/UpdateBooking/<from_date>,<from_time>,<to_date>,<to_time>,<cab_name>,<cab_type>,<status>,<user_id>,<source>,<destination>', methods=['GET'])
def UpdateBooking(from_date,from_time,to_date,to_time,cab_name,cab_type,status,user_id,source,destination):

    cab_id = getCabID(cab_name, cab_type)
    fromD = from_date +' ' + from_time
    toD = to_date +' ' + to_time
    print(str(status))

    if (checkBookingStatus(fromD, toD,cab_id)==0):
        print('Booking or Blocking...')
        if(status=='1'):
            # Booking
            print('Booking...')
            query = ''
            query += 'INSERT INTO BookingData VALUES('
            query += str(cab_id)+','
            query += '"'+fromD+'",'
            query += '"'+toD+'",'
            query += user_id+','
            query += status+', '
            query += '"'+source+'",'
            query += '"'+destination+'")'
            flag = run_insert_query(query)
        elif(status=='2'):
            # Blocking
            print('Blocking...')
            query = ''
            query += 'INSERT INTO BookingData VALUES('
            query += str(cab_id)+','
            query += '"'+fromD+'",'
            query += '"'+toD+'",'
            query += user_id+','
            query += status+', '
            query += '"",'
            query += '"")'
            flag = run_insert_query(query)

    return 'Done', 201

def getCabID(cab_name, cab_type):
    query ='select CAB_ID from CabData where '
    if(cab_name):
        query +=    "CAB_NAME = "+ cab_name
    else:
        query +=    "CAB_TYPE = "+ cab_type


    rows = run_select_query(query)
    if(len(rows)==1):
        return rows[0][0]
    elif (len(rows) > 1):
        return rows[0][0]
    else:
        return 0


def checkBookingStatus(fromD, toD,cab_id):
    query =''
    query += 'SELECT status FROM BookingData '
    query += 'WHERE '
    query += '    cab_id = '+str(cab_id)+' and '
    query += '    START_DATE_TIME < "' + toD + '" and '
    query += '    END_DATE_TIME >  "' + fromD + '" '

    rows = run_select_query(query)
    rows_count = len(rows)
    if(rows_count==0):
        print("Available")
        return 0
    elif(rows_count==1):
        if (rows[0][0] == 1):
            print("Already Booked")
        elif (rows[0][0] == 2):
            print("Already Blocked")
        return(rows[0][0])
    else:
        return -1


@app.route('/')
def home():
    return('Hello World')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin','*')
    #response.headers.add('Access-Control-Allow-Headers','Origin,Accept,X-Requested-With','Content-Type')
    response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(host='localhost', port='5000')




