#! /usr/local/bin/python  -*- coding: UTF-8 -*-
import random
from datatables import ColumnDT, DataTables
from flask import Blueprint, request, render_template, flash, redirect, url_for, Response, jsonify
from app import db, models, q, client, login_manager
from flask.ext.api.decorators import set_renderers
from flask.ext.api.renderers import HTMLRenderer
from HTMLParser import HTMLParser
from werkzeug.utils import secure_filename
from flask.ext.login import login_required, login_user, logout_user, current_user
import time
# encoding=utf8
import sys
import traceback

reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'fantom'
mod_site = Blueprint('website', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_CSV = {'csv'}


@mod_site.route('/unauthorized')
@set_renderers(HTMLRenderer)
@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('login.html')


@login_manager.user_loader
def load_user(broker_id):
    print("agent_id: " + str(broker_id))
    agent = db.session.query(models.Broker).filter_by(id=broker_id).first()
    if agent:
        print("agent is_authenticated: " + str(agent.is_authenticated))
    return agent


@mod_site.route('/home')
# route for GetShopItems function here
@set_renderers(HTMLRenderer)
def home():
    if current_user.is_authenticated:
        agent = db.session.query(models.Broker).filter_by(id=int(current_user.id)).one()
        return render_template('companies_list.html', agent=agent)
    else:
        return redirect(url_for('website.unauthorized_handler'))


# somewhere to logout
@mod_site.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('website.welcome'))


@mod_site.route('/')
@set_renderers(HTMLRenderer)
def welcome():
    # Welcome.
    print("current: " + str(current_user.is_authenticated))
    if current_user.is_authenticated:
        return redirect(url_for('website.home'))
    else:
        return redirect(url_for('website.login_broker'))


@mod_site.route('/signUpBroker', methods=['GET', 'POST'])
# route for GetShopItems function here
@set_renderers(HTMLRenderer)
def sign_up_agent():
    if request.method == 'POST':
        if request.form['first_name'] and request.form['last_name']:
            new_agent = models.Broker(first_name=request.form['first_name'], last_name=request.form['last_name'],
                                      email=request.form['email'], password=request.form['passwd'])
            db.session.add(new_agent)
            new_agent.authenticated = True
            db.session.commit()
            login_user(new_agent)
            return redirect(url_for('website.home'))
    return redirect(url_for('website.login_agent'))


def update_stock():
    print("update stocks")
    stocks = db.session.query(models.Stock).all()
    if len(stocks) > 0:
        print(str(len(stocks)))
        while True:
            for stock in stocks:
                v = stock.current_value
                new_value = random.uniform(v - 10, v + 10)
                if new_value > 0:
                    stock.current_value = new_value
                    stock.last_value = v
                    sv = models.StockValues(stock_id=stock.id, value=stock.current_value)
                    db.session.add(sv)
                    print(str(stock.id) + ":" + str(v) + "/" + str(stock.current_value))
                    db.session.commit()
            time.sleep(7*60)
        return


job = q.enqueue_call(func=update_stock, args=(), result_ttl=5000)


@mod_site.route('/start_data')
def start_data():
    return jsonify(status="started")


@mod_site.route('/list_companies_data')
def list_companies_data():
    """Return server side data."""
    # defining columns
    columns = [
        ColumnDT(models.Company.id),
        ColumnDT(models.Company.symbol),
        ColumnDT(models.Company.name + "|" + models.Company.name_ar),
        ColumnDT(models.Company.phone),
        ColumnDT(models.Company.website),
        ColumnDT("<a class=\"fa fa-edit\" href=\"{{url_for('website.edit_com', tn=" + models.Company.symbol + ")}}\"></a>")
    ]

    # defining the initial query depending on your purpose
    query = db.session.query().select_from(models.Company).filter(1 == 1)
    # GET parameters
    params = request.args.to_dict()
    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(params, query, columns)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())


@mod_site.route('/list_stock_data')
def list_stock_data():
    """Return server side data."""
    # defining columns
    columns = [
        ColumnDT(models.Stock.id),
        ColumnDT(models.Stock.current_value),
        ColumnDT(models.Stock.last_value),
        ColumnDT(models.Stock.init_no),
        ColumnDT(models.Stock.curr_no),
        ColumnDT(models.Stock.type),
        ColumnDT("<a class=\"fa fa-edit\" href=\"{{url_for('website.edit_com', tn=" + models.Company.symbol + ")}}\"></a>")
    ]

    # defining the initial query depending on your purpose
    query = db.session.query().select_from(models.Stock).filter(1 == 1)
    # GET parameters
    params = request.args.to_dict()
    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(params, query, columns)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())


@mod_site.route('/select_companies_data')
def select_companies_data():
    """Return server side data."""
    companies = db.session.query(models.Company).all()
    return [item.serialize for item in companies]


@mod_site.route('/values', methods=['GET', 'POST'])
# route for deleteShopItem function here
@set_renderers(HTMLRenderer)
def get_values():
    items = db.session.query(models.StockValues).filter_by(stock_id=1).all()
    return [item.serialize for item in items]


# @mod_site.route('/', methods=['GET', 'POST'])
# # route for deleteShopItem function here
# @set_renderers(HTMLRenderer)
# def home():
#     items = db.session.query(models.Company).all()
#     return render_template('companies_list.html', items=items)


@mod_site.route('/stock_chart/<int:stock_id>', methods=['GET', 'POST'])
# route for deleteShopItem function here
@set_renderers(HTMLRenderer)
def stock_chart(stock_id):
    agent = None
    stock = db.session.query(models.Stock).filter_by(id=stock_id).one()
    items = db.session.query(models.StockValues).filter_by(stock_id=stock.id).all()
    return render_template('stock_chart.html', items=[item.serialize for item in items], agent=agent)


@mod_site.route('/add_company', methods=['GET', 'POST'])
# route for deleteShopItem function here
@set_renderers(HTMLRenderer)
def add_company():
    agent = None
    if request.method == 'POST':
        try:
            company = db.session.query(models.Company).filter_by(id=request.form.get('tax_num')).first()
            if company:
                flash('Company with same Tax Number already exists with name ' + company.name)
                return render_template('add_company.html', agent=agent)
            company = db.session.query(models.Company).filter_by(id=request.form.get('com_num')).first()
            if company:
                flash('Company with same Commercial Number already exists with name ' + company.name)
                return render_template('add_company.html', agent=agent)

            new_company_name = request.form.get('com_name')
            new_company_name_ar = request.form.get('com_name_ar')
            new_company_symbol = request.form.get('symbol')
            new_company_phone = request.form.get('phone')
            new_company_email = request.form.get('email')
            new_company_website = request.form.get('website')
            new_company_com_num = request.form.get('com_num')
            new_company_tax_num = request.form.get('tax_num')

            new_company = models.Company(name=new_company_name, name_ar=new_company_name_ar, symbol=new_company_symbol,
                                         phone=new_company_phone, email=new_company_email, website=new_company_website,
                                         com_number=new_company_com_num, tax_number=new_company_tax_num)

            print(new_company.serialize)

            db.session.add(new_company)
            db.session.flush()
            new_id = new_company.id
            db.session.commit()
            print("item added id:" + str(new_id))
            return render_template('add_company.html', agent=agent)
        except:
            traceback.print_exc()
    else:
        return render_template('add_company.html', agent=agent)


@mod_site.route('/edit_company/<string:com_id>', methods=['GET', 'POST'])
# route for deleteShopItem function here
@set_renderers(HTMLRenderer)
def edit_company(com_id):
    company = db.session.query(models.Company).filter_by(symbol=com_id).first()
    if request.method == 'POST':
        try:
            company.name = request.form.get('com_name')
            company.name_ar = request.form.get('com_name_ar')
            company.symbol = request.form.get('symbol')
            company.phone = request.form.get('phone')
            company.email = request.form.get('email')
            company.website = request.form.get('website')
            company.com_number = request.form.get('com_num')
            company.tax_number = request.form.get('tax_num')
            company.longitude = request.form.get('longitude')
            company.latitude = request.form.get('latitude')

            print(company.serialize)

            db.session.add(company)
            db.session.flush()
            new_id = company.id
            db.session.commit()
            print("item added id:" + str(new_id))
            return render_template('edit_company.html', company=company)
        except:
            traceback.print_exc()
    else:
        return render_template('edit_company.html', company=company)


@mod_site.route('/add_stock', methods=['GET', 'POST'])
# route for deleteShopItem function here
@set_renderers(HTMLRenderer)
def add_stock():
    agent = None
    if request.method == 'POST':
        try:
            stock = db.session.query(models.Stock).filter_by(company_id=request.form.get('com_id')).first()
            if stock:
                flash('Stock for same Company already exists with name ' + stock.company.name)
                return render_template('add_stock.html', agent=agent)

            company = db.session.query(models.Company).filter_by(id=request.form.get('com_id')).first()

            new_stock_init_value = request.form.get('init_value')
            new_type = request.form.get('type')
            current_value = request.form.get('current_value')

            new_stock = models.Stock(init_no=new_stock_init_value, type=new_type, company=company, current_value=current_value)

            db.session.add(new_stock)
            db.session.flush()
            new_id = new_stock.id
            db.session.commit()
            print(new_id)

            print("item added id:" + str(new_id))
            return render_template('add_stock.html', agent=agent)
        except:
            traceback.print_exc()
    else:
        return render_template('add_stock.html', agent=agent)


# add new stock
@mod_site.route('/StockRequestConfirm/<int:stock_request_id>', methods=['GET', 'POST'])
def stock_request_confirm(stock_request_id):
    if current_user.is_authenticated:
        # broker_id = cu
        stock_request = db.session.query(models.Request).filter_by(id=stock_request_id).first()
        stock = db.session.query(models.Stock).filter_by(id=stock_request.stock.id).first()
        customer_stock = db.session.query(models.CustomerStocks).filter_by(
                stock_id=stock_request.stock.id, customer_id=stock_request.customer.id).first()
        if None is customer_stock:
            customer = db.session.query(models.Customer).filter_by(id=stock_request.customer.id).first()
            customer_stock = models.CustomerStocks(stock=stock, customer=customer)
        if stock_request.no_stocks <= stock.curr_no:
            broker = db.session.query(models.Broker).filter_by(id=int(current_user.id)).first()
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
            return render_template('request_confirmed.html')
        else:
            return render_template('page_500.html')
    else:
        return redirect(url_for('website.unauthorized_handler'))


@mod_site.route('/get_companies_list')
# route for GetShopItems function here
@set_renderers(HTMLRenderer)
def get_companies():
    companies = db.session.query(models.Company).all()
    return render_template('companies_list.html', items=companies)


@mod_site.route('/get_stocks')
# route for GetShopItems function here
@set_renderers(HTMLRenderer)
def get_stocks():
    stocks = db.session.query(models.Stock).all()
    return render_template('stocks_list.html', items=stocks)


@mod_site.route('/get_stocks_requests')
# route for GetShopItems function here
@set_renderers(HTMLRenderer)
def get_stocks_requests():
    stocks = db.session.query(models.Request).all()
    return render_template('stocks_list.html', items=stocks)
