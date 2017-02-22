#! /usr/local/bin/python  -*- coding: UTF-8 -*-
import random
from datatables import ColumnDT, DataTables
from flask import Blueprint, request, render_template, flash, redirect, url_for, Response, jsonify
from app import db, models, q, client
from flask.ext.api.decorators import set_renderers
from flask.ext.api.renderers import HTMLRenderer
from HTMLParser import HTMLParser
from werkzeug.utils import secure_filename
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


job = q.enqueue_call(func=update_stock)


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
        # ColumnDT("<a class=\"fa fa-edit\" href=\"{{url_for('website.edit_com', tn=" + models.Company.id + ")}}\"></a>")
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
        # ColumnDT("<a class=\"fa fa-edit\" href=\"{{url_for('website.edit_com', tn=" + models.Company.id + ")}}\"></a>")
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


@mod_site.route('/', methods=['GET', 'POST'])
# route for deleteShopItem function here
@set_renderers(HTMLRenderer)
def home():
    items = db.session.query(models.Company).all()
    return render_template('companies_list.html', items=items)


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


@mod_site.route('/edit_company/<int:com_id>', methods=['GET', 'POST'])
# route for deleteShopItem function here
@set_renderers(HTMLRenderer)
def edit_company(com_id):
    company = db.session.query(models.Company).filter_by(id=com_id).first()
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
