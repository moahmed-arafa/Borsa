# coding=utf-8
import json
from flask import Blueprint, request, jsonify
from sqlalchemy import desc
from app import db, API_KEY, client
from app import models

__author__ = 'fantom'

mod_mobile_user = Blueprint('mobile', __name__)


# Date handler for Create and Update Date
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


# user related functions
# 1_user login by @email and @password
@mod_mobile_user.route('/loginCustomer', methods=['GET', 'POST'])
def login_customer():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        username = req_json['email']
        password = req_json['password']
        user = db.session.query(models.Customer).filter_by(email=username).all()
        if len(user) > 0:
            if user[0].password == password:
                return {"response": user[0].id}
            else:
                # wrong password
                return {"response": -1}
        else:
            # no matching email
            return {"response": -2}
    return {"response": -400}


@mod_mobile_user.route('/loginBroker', methods=['GET', 'POST'])
def login_broker():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        username = req_json['email']
        password = req_json['password']
        user = db.session.query(models.Broker).filter_by(email=username).all()
        if len(user) > 0:
            if user[0].password == password:
                return {"response": user[0].id}
            else:
                # wrong password
                return {"response": -1}
        else:
            # no matching email
            return {"response": -2}
    return {"response": -400}


@mod_mobile_user.route('/loginCompany', methods=['GET', 'POST'])
def login_company():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        username = req_json['email']
        password = req_json['password']
        user = db.session.query(models.Company).filter_by(email=username).all()
        if len(user) > 0:
            if user[0].password == password:
                return {"response": user[0].id}
            else:
                # wrong password
                return {"response": -1}
        else:
            # no matching email
            return {"response": -2}
    return {"response": -400}


@mod_mobile_user.route('/getCustomer', methods=['GET', 'POST'])
def get_customer():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        user_id = req_json['user_id']
        user = db.session.query(models.Customer).filter_by(id=user_id).first()
        print(str(user_id))
        if user:
            print(user.serialize)
            return {"response": user.serialize}
        else:
            return {"response": -1}
    return {"response": -400}


@mod_mobile_user.route('/getCompany', methods=['GET', 'POST'])
def get_company():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        user_id = req_json['user_id']
        user = db.session.query(models.Company).filter_by(id=user_id).first()
        if user:
            return {"response": user.serialize}
        else:
            return {"response": -1}
    return {"response": -400}


@mod_mobile_user.route('/getStock', methods=['GET', 'POST'])
def get_stock():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        stock_id = req_json['stock_id']
        stock = db.session.query(models.Stock).filter_by(id=stock_id).first()
        if stock:
            print(json.dumps(stock.serialize, default=date_handler))
            return {"response": stock.serialize}
        else:
            return jsonify(response=-1)


@mod_mobile_user.route('/getBroker', methods=['GET', 'POST'])
def get_broker():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        user_id = req_json['user_id']
        user = db.session.query(models.Broker).filter_by(id=user_id).first()
        if user:
            return {"response": user.serialize}
        else:
            return {"response": -1}
    return {"response": -400}


@mod_mobile_user.route('/getAllCompanies', methods=['GET', 'POST'])
def get_all_companies():
    if request.headers.get('Authorization') == API_KEY:
        companies = db.session.query(models.Company).all()
        return [item.serialize for item in companies]
    return {"response": -400}


# sign up user by @email and @password
@mod_mobile_user.route('/signupCustomer', methods=['GET', 'POST'])
def signup_customer():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        first_name = req_json['first_name']
        last_name = req_json['last_name']
        username = req_json['email']
        password = req_json['password']
        if db.session.query(models.Customer).filter_by(email=username):
            user = db.session.query(models.Customer).filter_by(email=username).all()
            if len(user) > 0:
                if user[0].email == username:
                    # email already exist
                    return {"response": -2}
                    # if user[0].mobile == mobile:
                    #     # mobile already exist
                    #     return {"response": -3}
            else:
                user = models.Customer(first_name=first_name, last_name=last_name, email=username, password=password)
                try:
                    db.session.add(user)
                    db.session.flush()
                    new_id = user.id
                    db.session.commit()
                    # user_added = db.session.query(models.User).filter_by(email=username).all()
                    return {"response": new_id}
                except:
                    db.session.rollback()
                    raise
        else:
            # error
            return {"response": -1}
    else:
        return {"response": -400}


# sign up user by @email and @password
@mod_mobile_user.route('/signupCompany', methods=['GET', 'POST'])
def signup_company():
    global phone, address, com_number, latitude, longitude, tax_number
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        name = req_json['name']
        if req_json['phone']:
            phone = req_json['phone']
        email = req_json['email']
        if req_json['address']:
            address = req_json['address']
        password = req_json['password']
        if req_json['longitude']:
            longitude = req_json['longitude']
        if req_json['latitude']:
            latitude = req_json['latitude']
        if req_json['com_number']:
            com_number = req_json['com_number']
        if req_json['tax_number']:
            tax_number = req_json['tax_number']
        if db.session.query(models.Company).filter_by(email=email):
            user = db.session.query(models.Company).filter_by(email=email).all()
            if len(user) > 0:
                if user[0].email == email:
                    # email already exist
                    return {"response": -2}
                    # if user[0].mobile == mobile:
                    #     # mobile already exist
                    #     return {"response": -3}
            else:
                user = models.Company(name=name, phone=phone, email=email, address=address, password=password,
                                      longitude=longitude, latitude=latitude, com_number=com_number,
                                      tax_number=tax_number)
                try:
                    db.session.add(user)
                    db.session.flush()
                    new_id = user.id
                    db.session.commit()
                    # user_added = db.session.query(models.User).filter_by(email=username).all()
                    return {"response": new_id}
                except:
                    db.session.rollback()
                    raise
        else:
            # error
            return {"response": -1}
    else:
        return {"response": -400}


# sign up user by @email and @password
@mod_mobile_user.route('/signupBroker', methods=['GET', 'POST'])
def signup_broker():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        first_name = req_json['first_name']
        last_name = req_json['last_name']
        username = req_json['email']
        password = req_json['password']
        phone = req_json['phone']
        if db.session.query(models.Broker).filter_by(email=username):
            user = db.session.query(models.Broker).filter_by(email=username).all()
            if len(user) > 0:
                if user[0].email == username:
                    # email already exist
                    return {"response": -2}
                    # if user[0].mobile == mobile:
                    #     # mobile already exist
                    #     return {"response": -3}
            else:
                user = models.Broker(first_name=first_name, last_name=last_name, email=username, password=password,
                                     phone=phone)
                try:
                    db.session.add(user)
                    db.session.flush()
                    new_id = user.id
                    db.session.commit()
                    # user_added = db.session.query(models.User).filter_by(email=username).all()
                    return {"response": new_id}
                except:
                    db.session.rollback()
                    raise
        else:
            # error
            return {"response": -1}
    else:
        return {"response": -400}


# register device for push notifications
@mod_mobile_user.route('/registerDevice', methods=['GET', 'POST'])
def register_device():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        device_token = req_json['device_token']
        token = models.DeviceToken(device_token=device_token)
        print(device_token)
        client.send(device_token, "welcome To Borsa")
        db.session.add(token)
        db.session.commit()
        return {"response": device_token}
    return {"response": -400}


# add new stock
@mod_mobile_user.route('/addStock', methods=['GET', 'POST'])
def add_stock():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        company_id = req_json['company_id']
        stock_type = req_json['type']
        init_no = req_json['init_no']
        value = req_json['value']
        company = db.session.query(models.Company).filter_by(id=company_id).first()
        stock = models.Stock(company=company, type=stock_type, init_no=init_no, curr_no=init_no)
        db.session.add(stock)
        db.session.flush()
        values = models.StockValues(stock=stock, value=value)
        db.session.add(values)
        db.session.commit()
        return {"response": stock.id}
    return {"response": -400}


@mod_mobile_user.route('/getStockValues', methods=['GET', 'POST'])
def get_stock_values():
    if request.headers.get('Authorization') == API_KEY:
        # req_json = request.get_json()
        # stock_id = req_json['stock_id']
        req_json = json.loads(request.get_data(as_text=True))
        stock_id = req_json['stock_id']
        if stock_id:
            value = db.session.query(models.StockValues).filter_by(stock_id=stock_id).all()
            return [item.serialize for item in value[0, 10000]]
        else:
            return {"response": -2}
    return {"response": -400}


# add new stock
@mod_mobile_user.route('/buyStockRequest', methods=['GET', 'POST'])
def buy_stock_request():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        stock_id = req_json['stock_id']
        customer_id = req_json['customer_id']
        no_stocks = req_json['no_stocks']
        stock = db.session.query(models.Stock).filter_by(id=stock_id).first()
        print(str(stock.curr_no))
        if stock.curr_no:
            curr_no = stock.curr_no
        else:
            curr_no = stock.init_no
        print("requested stocks: " + str(curr_no) + ":" + str(no_stocks) + str(int(curr_no) >= int(no_stocks)))
        if int(curr_no) >= int(no_stocks):
            customer = db.session.query(models.Customer).filter_by(id=customer_id).first()
            value = db.session.query(models.StockValues).filter_by(stock_id=stock_id).first()
            stock_request = models.Request(type=bin(1), stock=stock, customer=customer, no_stocks=no_stocks,
                                           value=value)
            db.session.add(stock_request)
            db.session.flush()
            db.session.commit()
            return {"response": stock_request.id}
        else:
            return {"response": -2}
    return {"response": -400}


# add new stock
@mod_mobile_user.route('/sellStockRequest', methods=['GET', 'POST'])
def sell_stock_request():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        stock_id = req_json['stock_id']
        customer_id = req_json['customer_id']
        no_stocks = req_json['no_stocks']
        stock = db.session.query(models.Stock).filter_by(id=stock_id).first()
        customer = db.session.query(models.Customer).filter_by(id=customer_id).first()
        customer_stock = db.session.query(models.CustomerStocks).filter_by(stock_id=stock_id,
                                                                           customer_id=customer_id).first()
        if customer_stock:
            if customer_stock.quantity >= no_stocks:
                value = db.session.query(models.StockValues).filter_by(stock_id=stock_id).order_by(
                    desc(models.StockValues.date_add)).first()
                stock_request = models.Request(type=bin(0), stock=stock, customer=customer, no_stocks=no_stocks,
                                               value=value)
                db.session.add(stock_request)
                db.session.flush()
                db.session.commit()
                return {"response": stock_request.id}
            else:
                return {"response": -2}
        else:
            return {"response": -1}
    return {"response": -400}


# add new stock
@mod_mobile_user.route('/buyStockRequestConfirm', methods=['GET', 'POST'])
def buy_stock_request_confirm():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        stock_request_id = req_json['stock_request_id']
        broker_id = req_json['broker_id']
        stock_request = db.session.query(models.Request).filter_by(id=stock_request_id).first()
        stock = db.session.query(models.Stock).filter_by(id=stock_request.stock.id).first()
        customer_stock = db.session.query(models.CustomerStocks).filter_by(
            stock_id=stock_request.stock.id, customer_id=stock_request.customer.id).first()
        if None is customer_stock:
            customer = db.session.query(models.Customer).filter_by(id=stock_request.customer.id).first()
            customer_stock = models.CustomerStocks(stock=stock, customer=customer)
        if stock_request.no_stocks <= stock.curr_no:
            broker = db.session.query(models.Broker).filter_by(id=broker_id).first()
            stock_request.broker = broker
            stock.curr_no = stock.curr_no - stock_request.no_stocks
            if None is customer_stock.quantity:
                customer_stock.quantity = stock_request.no_stocks
            else:
                customer_stock.quantity = customer_stock.quantity + stock_request.no_stocks
            # ToDo make credit transaction and update balance
            db.session.add(stock_request)
            db.session.flush()
            db.session.commit()
            return {"response": stock_request.id}
        else:
            return {"response": -2}
    return {"response": -400}


# add new stock
@mod_mobile_user.route('/sellStockRequestConfirm', methods=['GET', 'POST'])
def sell_stock_request_confirm():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        stock_request_id = req_json['stock_request_id']
        broker_id = req_json['broker_id']
        stock_request = db.session.query(models.Request).filter_by(id=stock_request_id).first()
        stock = db.session.query(models.Stock).filter_by(id=stock_request.stock.id).first()
        customer_stock = db.session.query(models.CustomerStocks).filter_by(
            stock_id=stock_request.stock.id, customer_id=stock_request.customer.id).first()
        if stock_request.no_stocks <= customer_stock.quantity:
            broker = db.session.query(models.Broker).filter_by(id=broker_id).first()
            stock_request.broker = broker
            customer_stock.quantity = customer_stock.quantity - stock_request.no_stocks
            stock.curr_no = stock.curr_no + stock_request.no_stocks
            # ToDo make credit transaction and update balance
            db.session.add(stock)
            db.session.add(stock_request)
            db.session.flush()
            db.session.commit()
            return {"response": stock_request.id}
        else:
            return {"response": -2}
    return {"response": -400}


# add new stock
@mod_mobile_user.route('/getAllStocks', methods=['GET', 'POST'])
def get_all_stocks():
    if request.headers.get('Authorization') == API_KEY:
        stock = db.session.query(models.Stock).all()
        return [item.serialize for item in stock]
    return {"response": -400}


# add new stock
@mod_mobile_user.route('/updateStockValve', methods=['GET', 'POST'])
def update_stock_value():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        stock_id = req_json['stock_id']
        value = req_json['value']
        stock = db.session.query(models.Stock).filter_by(id=stock_id).first()
        stock_value = models.StockValues(stock=stock, value=value)
        db.session.add(stock_value)
        db.session.commit()
        return stock.serialize
    return {"response": -400}


# add new stock
@mod_mobile_user.route('/getCompanyStocks', methods=['GET', 'POST'])
def get_company_stocks():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        company_id = req_json['company_id']
        stock = db.session.query(models.Stock).filter_by(company_id=company_id).all()
        return [item.serialize for item in stock]
    return {"response": -400}


# add new stock
@mod_mobile_user.route('/getUserStocks', methods=['GET', 'POST'])
def get_user_stocks():
    if request.headers.get('Authorization') == API_KEY:
        req_json = json.loads(request.get_data(as_text=True))
        customer_id = req_json['customer_id']
        stock = db.session.query(models.CustomerStocks).filter_by(customer_id=customer_id).all()
        return [item.serialize for item in stock]
    return {"response": -400}
