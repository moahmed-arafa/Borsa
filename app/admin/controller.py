import json
import mechanize as mechanize

__author__ = 'fantom'
from flask import Blueprint, request, jsonify, render_template
from app import db, API_KEY, API_KEY_ERROR, app
from app import models
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask.ext.api.decorators import set_renderers
from flask.ext.api.renderers import HTMLRenderer
from HTMLParser import HTMLParser

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

mod_admin = Blueprint('admin', __name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class MLStripper(HTMLParser):
    def error(self, message):
        pass

    def __init__(self):
        HTMLParser.__init__(self)
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


@mod_admin.route('/')
def summery():
    if request.headers.get('Authorization') == API_KEY:
        user = db.session.query(models.User).filter_by(id=1).first()
        print(user.is_authenticated)
        # Functions Documentation.
        return render_template('summery.html')
    return API_KEY_ERROR


@mod_admin.route('/users')
def get_users():
    if request.headers.get('Authorization') == API_KEY:
        users = db.session.query(models.User).all()
        return [i.serialize for i in users]
    return API_KEY_ERROR


@mod_admin.route('/GetAllShops/JSON')
def get_all_shops():
    if request.headers.get('Authorization') == API_KEY:
        shops = db.session.query(models.Shop).all()
        return [i.serialize for i in shops]
    return API_KEY_ERROR


@mod_admin.route('/GetCategories/JSON')
def get_all_categories():
    if request.headers.get('Authorization') == API_KEY:
        categories = db.session.query(models.Category).all()
        return [i.serialize for i in categories]
    return API_KEY_ERROR


@mod_admin.route('/GetSubCategories/JSON')
def get_sub_categories():
    if request.headers.get('Authorization') == API_KEY:
        categories = db.session.query(models.SubCategory).all()
        return [i.serialize for i in categories]
    return API_KEY_ERROR


@mod_admin.route('/Orders/JSON')
def get_orders():
    if request.headers.get('Authorization') == API_KEY:
        orders = db.session.query(models.Orders).all()
        return [i.serialize for i in orders]
    return API_KEY_ERROR


@mod_admin.route('/editOrderByID/<int:order_id>/', methods=['GET', 'POST'])
def edit_order_by_id(order_id):
    if request.headers.get('Authorization') == API_KEY:
        order = db.session.query(models.Orders).filter_by(id=order_id).one()
        shop = order.item.shop
        if request.method == 'POST':
            if request.form['shipping_address'] is not None:
                order.shipping_address = request.form['shipping_address']
            if request.form['quantity'] is not None:
                order.quantity = request.form['quantity']
            db.session.add(order)
            db.session.commit()
            return render_template('Admin/OrdersList.html', shop=shop)
        else:
            return render_template('Admin/EditOrder.html', order=order)
    return API_KEY_ERROR


@mod_admin.route('/addLocation/<int:shop_id>/<float:lon>/<float:lat>/', methods=['GET', 'POST'])
def add_location(shop_id, lon, lat):
    if request.headers.get('Authorization') == API_KEY:
        shop = db.session.query(models.Shop).filter_by(id=shop_id).one()
        shop.longitude = lat
        shop.latitude = lon
        db.session.add(shop)
        db.session.commit()
        return "Location Updated!"
    return API_KEY_ERROR


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@mod_admin.route('/uploadImage', methods=['GET', 'POST'])
@set_renderers(HTMLRenderer)
def upload_image():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                # flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                # flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                browser = mechanize.Browser()
                browser.open("http://bubble.zeowls.com/upload.php")
                # file uploading
                form = browser.form = browser.forms().next()
                form.add_file(file, filename=os.path.basename(filename))
                send_response = browser.submit()
                data = strip_tags(send_response.get_data().replace("\n", "").replace(" ", ""))
                print data
                obj = json.loads(data)
                return obj['image']
        return render_template('Admin/ImageUpload.html')
    return API_KEY_ERROR
