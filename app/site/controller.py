#! /usr/local/bin/python  -*- coding: UTF-8 -*-
import json
from string import upper
from datatables import ColumnDT, DataTables
import os
from flask.ext.restplus import abort
import mechanize
from flask import Blueprint, request, render_template, flash, redirect, url_for, Response, jsonify
from flask.ext.login import login_required, login_user, logout_user, current_user
from numpy import genfromtxt
from app import db, login_manager, models, q, client
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
    agent = None
    stock = db.session.query(models.Stock).filter_by(id=1).one()
    items = db.session.query(models.StockValues).filter_by(stock_id=stock.id).all()
    return render_template('stock_chart.html', items=[item.serialize for item in items], agent=agent)
