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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def allowed_file_csv(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_CSV


login_manager.login_view = 'login_agent'


@mod_site.route('/unauthorized')
@set_renderers(HTMLRenderer)
@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('gentelella/production/login.html')


@mod_site.route('/page')
@set_renderers(HTMLRenderer)
def get_page():
    return render_template('shop/progress.html')


@mod_site.route('/progress')
def progress():
    def generate():
        x = 0
        while x < 100:
            print x
            x += 10
            time.sleep(0.2)
            yield "data:" + str(x) + "\n\n"

    return Response(generate(), mimetype='text/event-stream')


@login_manager.user_loader
def load_user(agent_id):
    print("agent_id: " + str(agent_id))
    agent = db.session.query(models.Agents).filter_by(id=agent_id).first()
    if agent:
        print("agent is_authenticated: " + str(agent.is_authenticated))
    return agent


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
        return redirect(url_for('website.login_agent'))


@mod_site.route('/signUpAgent', methods=['GET', 'POST'])
# route for GetShopItems function here
@set_renderers(HTMLRenderer)
def sign_up_agent():
    if request.method == 'POST':
        if request.form['first_name'] and request.form['last_name']:
            new_agent = models.Agents(first_name=request.form['first_name'], last_name=request.form['last_name'],
                                      email=request.form['email'], passwd=request.form['passwd'])
            db.session.add(new_agent)
            new_agent.authenticated = True
            db.session.commit()
            login_user(new_agent)
            return redirect(url_for('website.home'))
    return redirect(url_for('website.login_agent'))


@mod_site.route('/sendPush', methods=['GET', 'POST'])
# route to push notification function here
@set_renderers(HTMLRenderer)
def send_push():
    if current_user.is_authenticated:
        agent = db.session.query(models.Agents).filter_by(id=int(current_user.id)).one()
        if request.method == "POST":
            message = request.form['message']
            title = request.form['title']
            body = request.form['body']
            users = db.session.query(models.DeviceTokens).all()
            for user in users:
                if None is not user.device_token:
                    client.send(user, message, notification={'title': title, 'body': body})
            else:
                flash("Failed because of no user or no device token")
        else:
            return render_template('shop/send_push.html', agent=agent)
    else:
        return redirect(url_for('website.unauthorized_handler'))


@mod_site.route('/home')
# route for GetShopItems function here
@set_renderers(HTMLRenderer)
def home():
    if current_user.is_authenticated:
        agent = db.session.query(models.Agents).filter_by(id=int(current_user.id)).one()
        return render_template('gentelella/production/index.html', agent=agent)
    else:
        return redirect(url_for('website.unauthorized_handler'))


@mod_site.route('/data')
def data():
    """Return server side data."""
    # defining columns
    columns = [
        ColumnDT(models.Products.id),
        ColumnDT(models.Products.code),
        ColumnDT(models.Products.name),
        # ColumnDT(models.Products.description),
        # ColumnDT(models.Products.price)
    ]

    # defining the initial query depending on your purpose
    query = db.session.query().select_from(models.Products).filter(1 == 1)
    # GET parameters
    params = request.args.to_dict()
    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(params, query, columns)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())


@mod_site.route('/users_reviews_data')
def users_reviews_data():
    """Return server side data."""
    # defining columns
    columns = [
        ColumnDT(models.ProductReview.id),
        ColumnDT(models.ProductReview.id_user),
        ColumnDT(models.ProductReview.user.first_name + " " + models.ProductReview.user.last_name),
        ColumnDT(models.ProductReview.id_product),
        ColumnDT(models.ProductReview.product.name),
        ColumnDT(models.ProductReview.review),
        ColumnDT(models.ProductReview.rate)
    ]

    # defining the initial query depending on your purpose
    query = db.session.query().select_from(models.ProductReview).filter(1 == 1)
    # GET parameters
    params = request.args.to_dict()
    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(params, query, columns)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())


@mod_site.route('/GetItems')
# route for GetShopItems function here
@set_renderers(HTMLRenderer)
def get_items():
    if current_user.is_authenticated:
        agent = db.session.query(models.Agents).filter_by(id=int(current_user.id)).one()
        items = db.session.query(models.Products).all()
        return render_template('shop/ItemsList.html', agent=agent, items=items)
    else:
        return redirect(url_for('website.unauthorized_handler'))


@mod_site.route('/GetCategories')
# route for GetShopItems function here
@set_renderers(HTMLRenderer)
def get_cats():
    if current_user.is_authenticated:
        agent = db.session.query(models.Agents).filter_by(id=int(current_user.id)).one()
        items = db.session.query(models.Category).all()
        return render_template('shop/ItemsList.html', agent=agent, items=items)
    else:
        return redirect(url_for('website.unauthorized_handler'))


@mod_site.route('/usersReviews')
# route for GetShopItems function here
@set_renderers(HTMLRenderer)
def get_reviews_by_user():
    if current_user.is_authenticated:
        agent = db.session.query(models.Agents).filter_by(id=int(current_user.id)).one()
        items = db.session.query(models.ProductReview).all()
        return render_template('shop/all_users_reviews.html', agent=agent, items=items)
    else:
        return redirect(url_for('website.unauthorized_handler'))


@mod_site.route('/editMyShop/<int:agent_id>', methods=['GET', 'POST'])
# route for editMyShop function here
@set_renderers(HTMLRenderer)
def edit_agent(agent_id):
    if current_user.is_authenticated:
        shop = db.session.query(models.Shop).filter_by(id=int(current_user.id)).one()
        if request.method == 'POST':
            if request.form['owner_name']:
                shop.owner_name = request.form['owner_name']
            if request.form['owner_email']:
                shop.owner_email = request.form['owner_email']
            if request.form['shop_name']:
                shop.shop_name = request.form['shop_name']
            if request.form['description']:
                shop.description = request.form['description']
            if request.form['shop_address']:
                shop.shop_address = request.form['shop_address']
            if request.form.get('mobile'):
                shop.mobile = request.form['mobile']
            if request.form['lon']:
                longitude = request.form['lon']
                shop.longitude = longitude
            if request.form['lat']:
                latitude = request.form['lat']
                shop.latitude = latitude
            db.session.add(shop)
            db.session.commit()
            flash("shop Edited!!")
            return redirect(url_for('website.get_shop_items', shop_id=int(current_user.id)))
        else:
            return render_template('shop/EditShop.html', shop=shop)
    else:
        return redirect(url_for('website.unauthorized_handler'))


@mod_site.route('/editMyShop/uploadImage/<int:shop_id>', methods=['GET', 'POST'])
# route for editMyShop function here
@set_renderers(HTMLRenderer)
def edit_shop_image(shop_id):
    if int(current_user.id) == int(shop_id):
        shop = db.session.query(models.Shop).filter_by(id=shop_id).one()
        if request.method == 'POST':
            if request.files['file']:
                # check if the post request has the file part
                if 'file' not in request.files:
                    flash('No file part')
                file_upload = request.files['file']
                # if user does not select file, browser also
                # submit a empty part without filename
                if file_upload.filename == '':
                    flash('No selected file')
                if file_upload and allowed_file(file_upload.filename):
                    filename = secure_filename(file_upload.filename)
                    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    browser = mechanize.Browser()
                    browser.open("http://bubble.zeowls.com/upload.php")
                    # file uploading
                    form = browser.form = browser.forms().next()
                    form.add_file(file_upload, filename=os.path.basename(filename))
                    send_response = browser.submit()
                    data = strip_tags(send_response.get_data().replace("\n", "").replace(" ", ""))
                    obj = json.loads(data)
                    image_file = obj['image']
                    shop.shop_profile_pic = image_file
            db.session.add(shop)
            db.session.commit()
            flash("shop Edited!!")
            return redirect(url_for('website.edit_shop', shop_id=shop_id))
        else:
            return render_template('shop/ImageUpload.html', shop=shop)
    else:
        return redirect(url_for('website.unauthorized_handler'))


@mod_site.route('/uploadItemImage/<int:item_id>', methods=['GET', 'POST'])
# route for editMyShop function here
@set_renderers(HTMLRenderer)
def edit_item_image(agent_id, item_id):
    if current_user.is_authenticated:
        agent = db.session.query(models.Agents).filter_by(id=int(current_user.id)).one()
        item = db.session.query(models.Products).filter_by(id=item_id).one()
        if request.method == 'POST':
            if request.files['file']:
                # check if the post request has the file part
                if 'file' not in request.files:
                    flash('No file part')
                file_upload = request.files['file']
                # if user does not select file, browser also
                # submit a empty part without filename
                if file_upload.filename == '':
                    flash('No selected file')
                if file_upload and allowed_file(file_upload.filename):
                    filename = secure_filename(file_upload.filename)
                    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    browser = mechanize.Browser()
                    browser.open("http://bubble.zeowls.com/upload.php")
                    # file uploading
                    form = browser.form = browser.forms().next()
                    form.add_file(file_upload, filename=os.path.basename(filename))
                    send_response = browser.submit()
                    data = strip_tags(send_response.get_data().replace("\n", "").replace(" ", ""))
                    obj = json.loads(data)
                    image_file = obj['image']
                    item.main_image = image_file
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('website.get_items'))
        else:
            return render_template('shop/ImageUpload.html', shop=item, agent=agent)
    else:
        return redirect(url_for('website.unauthorized_handler'))


def upload_item_image(file_upload, item_id):
    item = db.session.query(models.Products).filter_by(id=item_id).one()
    filename = secure_filename(file_upload.filename)  # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    browser = mechanize.Browser()
    browser.open("http://bubble.zeowls.com/upload.php")
    # file uploading
    form = browser.form = browser.forms().next()
    form.add_file(file_upload, filename=os.path.basename(filename))
    send_response = browser.submit()
    data = strip_tags(send_response.get_data().replace("\n", "").replace(" ", ""))
    obj = json.loads(data)
    image_file = obj['image']
    item.main_image = image_file
    db.session.add(item)
    db.session.commit()


def load_data_from_csv(file_name):
    data = genfromtxt(file_name, dtype=None, delimiter=',', skip_header=0, converters={0: lambda s: str(s)})
    return data.tolist()


@mod_site.route('/uploadItemsCSV', methods=['GET', 'POST'])
# route for editMyShop function here
@set_renderers(HTMLRenderer)
def edit_items_csv():
    if current_user.is_authenticated:
        # t = time()
        agent = db.session.query(models.Agents).filter_by(id=int(current_user.id)).one()
        if request.method == 'POST':
            print('inside post')
            if request.files['file']:
                print('file exist')
                # check if the post request has the file part
                if 'file' not in request.files:
                    flash('No file part')
                file_upload = request.files['file']
                # if user does not select file, browser also
                # submit a empty part without filename
                if file_upload.filename == '':
                    flash('No selected file')
                if file_upload and allowed_file_csv(file_upload.filename):
                    session = db.session
                    print("file name: " + file_upload.filename)
                    # try:
                    data = load_data_from_csv(file_upload)
                    for index, i in enumerate(data):
                        print i
                        record = models.Products(**{
                            'name': i[0],
                            'quantity': i[1],
                            'price': i[2],
                        })
                        # session.add(record)  # Add all the records
                        # print("added: " + i[0])
                        # db.session.flush()
                        # new_id = record.id

                        # session.commit()  # Attempt to commit all the records
                        # except:
                        #     print("ERROR!!!")
                        #     session.rollback()  # Rollback the changes on error
                        # finally:
                        #     session.close()  # Close the connection
                        #     print "Time elapsed: " + str(time() - t) + " s."  # 0.091s
                        #     return redirect(url_for('website.get_items', agent_id=agent_id))
                else:
                    flash('file type not allowed')
            else:
                flash('no file selected')
            return render_template('shop/CsvUpload.html', agent=agent)
        else:
            return render_template('shop/CsvUpload.html', agent=agent)
    else:
        return redirect(url_for('website.unauthorized_handler'))


def add_cats_to_database(data):
    parent_id = 0
    print("add_cats_to_database")
    for i in data:
        print(parent_id)
        print(str(len(i[0].replace("'", ''))))
        if 2 == len(i[0].replace("'", '')):
            print "**** MAIN Cat:" + str(i[1]) + " ****"
            main_cat = db.session.query(models.MainCategory).filter_by(code=i[0]).first()
            if main_cat:
                main_cat.name = i[1].replace("'", '')
            else:
                main_cat = models.MainCategory(**{
                    'code': i[0].replace("'", ''),
                    'name': i[1].replace("'", '')
                })
            db.session.add(main_cat)  # Add all the records
            db.session.flush()
            parent_id = main_cat.id
            db.session.commit()
            # print("added: " + str(i[1]))
        else:

            cat = db.session.query(models.Category).filter_by(code=i[0]).first()
            pcat = db.session.query(models.MainCategory).filter_by(id=parent_id).first()
            if cat:
                cat.name = i[1].replace("'", '')
                print "SUB Cat:" + str(i[1]) + " ___ Updated"
            else:
                cat = models.Category(**{
                    'code': str(i[0].replace("'", '')),
                    'name': i[1].replace("'", ''),
                    'id_parent': parent_id,
                    'parent': pcat
                })
                print "SUB Cat:" + str(i[1]) + " ___ Created"
            # yield "data:" + str(index / total) + "\n\n"
            db.session.add(cat)  # Add all the records
            # print("added: " + str(i[1]) + "___ Parent: " + str(parent_id))
            db.session.commit()  # Attempt to commit all the records
    return


def add_products_to_database(data):
    print("add_products_to_database")
    for i in data:
        try:
            if 5 < len(i[1]):
                print "**** Cat:" + str(i[1][1:6]) + " ****"
                cat = db.session.query(models.Category).filter_by(code=i[1][1:6]).first()
                main_cat = db.session.query(models.MainCategory).filter_by(id=cat.id_parent).first()
                if cat:
                    print(cat.name)
                    record = db.session.query(models.Products).filter_by(code=i[1]).first()
                    if record:
                        record.name = i[0].replace("'", '').decode('utf-8')
                        record.code = i[1].replace("'", '')
                        record.quantity = i[2]
                        record.main_category = main_cat
                        print "**** product:" + str(i[0]) + " **** Updated"
                    else:
                        record = models.Products(**{
                            'name': i[0].replace("'", '').decode('utf-8'),
                            'id_manufacturer': i[1][1:6].replace("'", ''),
                            'code': i[1].replace("'", ''),
                            'quantity': i[2],
                            'category': cat,
                            'main_category': main_cat
                        })
                        print "**** product:" + str(i[0]) + " **** Created"
                    db.session.add(record)  # Add all the records
                    db.session.commit()  # Attempt to commit all the records
        except:
            traceback.print_exc()
            # db.session.rollback()  # Rollback the changes on error
        finally:
            db.session.close()  # Close the connection
            # return redirect(url_for('website.get_items', agent_id=agent_id))

    return


@mod_site.route('/uploadCatsCSV', methods=['GET', 'POST'])
# route for editMyShop function here
@set_renderers(HTMLRenderer)
def edit_cats_csv():
    if current_user:
        if current_user.is_authenticated:
            agent = db.session.query(models.Agents).filter_by(id=int(current_user.id)).one()
            if request.method == 'POST':
                print('inside post')
                if request.files['file']:
                    print('file exist')
                    # check if the post request has the file part
                    if 'file' not in request.files:
                        flash('No file part')
                    file_upload = request.files['file']
                    # if user does not select file, browser also
                    # submit a empty part without filename
                    if file_upload.filename == '':
                        flash('No selected file')
                    if file_upload and allowed_file_csv(file_upload.filename):
                        print("file name: " + file_upload.filename)
                        # try:
                        data = load_data_from_csv(file_upload)
                        job = q.enqueue_call(func=add_cats_to_database, args=(data,), result_ttl=5000)
                    else:
                        flash('file type not allowed')
                else:
                    flash('no file selected')
                return render_template('shop/CsvUpload.html', agent=agent)
            else:
                return render_template('shop/CsvUpload.html', agent=agent)
        else:
            return redirect(url_for('website.unauthorized_handler'))
    else:
        return redirect(url_for('website.unauthorized_handler'))


@mod_site.route('/uploadProductsCSV', methods=['GET', 'POST'])
# route for editMyShop function here
@set_renderers(HTMLRenderer)
def edit_products_csv():
    if current_user.is_authenticated:
        agent = db.session.query(models.Agents).filter_by(id=int(current_user.id)).one()
        if request.method == 'POST':
            print('inside post')
            if request.files['file']:
                print('file exist')
                # check if the post request has the file part
                if 'file' not in request.files:
                    flash('No file part')
                file_upload = request.files['file']
                # if user does not select file, browser also
                # submit a empty part without filename
                if file_upload.filename == '':
                    flash('No selected file')
                if file_upload and allowed_file_csv(file_upload.filename):
                    print("file name: " + file_upload.filename)
                    # try:
                    data = load_data_from_csv(file_upload)
                    job = q.enqueue_call(func=add_products_to_database, args=(data,), result_ttl=5000)
                else:
                    flash('file type not allowed')
            else:
                flash('no file selected')
            return render_template('shop/CsvProductUpload.html', agent=agent)
        else:
            return render_template('shop/CsvProductUpload.html', agent=agent)
    else:
        return redirect(url_for('website.unauthorized_handler'))


@mod_site.route('/newItem', methods=['GET', 'POST'])
@login_required
# route for newShopItem function here
@set_renderers(HTMLRenderer)
def new_item():
    if current_user.is_authenticated:
        agent = db.session.query(models.Agents).filter_by(id=int(current_user.id)).one()
        main_cats = db.session.query(models.Category).all()
        if request.method == 'POST':
            if request.form['name'] and request.form['quantity']:
                newitem = models.Products(name=request.form['name'], quantity=request.form['quantity'],
                                          id_category=request.form.get('cat_id'), price=request.form['price'],
                                          description=request.form['description'])
                db.session.add(newitem)
                db.session.flush()
                new_id = newitem.id
                db.session.commit()
                print("item added id:" + str(new_id))
                return redirect(url_for('website.edit_item_image', item_id=new_id))
        else:
            return render_template('shop/new_item.html', agent=agent, main_cats=main_cats)
    else:
        return redirect(url_for('website.unauthorized_handler'))


@mod_site.route('/editShopItem/<int:item_id>/', methods=['GET', 'POST'])
@login_required
# route for editShopItem function here
@set_renderers(HTMLRenderer)
def edit_shop_item(item_id):
    if current_user.is_authenticated:
        agent = db.session.query(models.Agents).filter_by(id=int(current_user.id)).one()
        item = db.session.query(models.Products).filter_by(id=item_id).one()
        main_cats = db.session.query(models.Category).all()
        # sub_cat = {}
        # for cat in main_cats:
        #     print(cat.name)
        #     sub_cat[cat.id] = db.session.query(models.SubCategory).filter_by(parentCat=cat.id)
        if request.method == 'POST':
            if request.form['name']:
                item.name = request.form['name']
            if request.form['description']:
                item.description = request.form['description']
            if request.form['quantity']:
                item.quantity = request.form['quantity']
            if request.form['price']:
                item.price = request.form['price']
            if request.form.get('cat_id'):
                print('category', request.form.get('cat_id'))
                item.cat_id = request.form['cat_id']
            if request.form['image']:
                image_file = request.form['image']
                item.image = image_file
            # item.images = [{"id": 1, "url": "570269c0f2302.png"}, {"id": 2, "url": "570269c0f2302.png"},
            #                {"id": 3, "url": "570269c0f2302.png"}, {"id": 4, "url": "570269c0f2302.png"},
            #                {"id": 5, "url": "570269c0f2302.png"}, ]
            db.session.add(item)
            db.session.commit()
            flash("New Item Edited!!")
            return redirect(url_for('website.get_items'))
        else:
            return render_template('shop/EditItem.html', agent=agent, item=item, main_cats=main_cats)
    else:
        return redirect(url_for('website.unauthorized_handler'))


@mod_site.route('/editItem/<int:item_id>/', methods=['GET', 'POST'])
@login_required
# route for editShopItem function here
@set_renderers(HTMLRenderer)
def edit_item(item_id):
    # if int(current_user.id) == int(shop_id):
    #     shop = db.session.query(models.Shop).filter_by(id=shop_id).one()
    item = db.session.query(models.Products).filter_by(id=item_id).one()
    main_cats = db.session.query(models.Category).all()
    # sub_cat = {}
    # for cat in main_cats:
    #     print(cat.name)
    #     sub_cat[cat.id] = db.session.query(models.SubCategory).filter_by(parentCat=cat.id)
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['quantity']:
            item.quantity = request.form['quantity']
        if request.form['price']:
            item.price = request.form['price']
        if request.form.get('cat_id'):
            print('category', request.form.get('cat_id'))
            item.cat_id = request.form['cat_id']
        if request.form['image']:
            image_file = request.form['image']
            item.image = image_file
        # item.images = [{"id": 1, "url": "570269c0f2302.png"}, {"id": 2, "url": "570269c0f2302.png"},
        #                {"id": 3, "url": "570269c0f2302.png"}, {"id": 4, "url": "570269c0f2302.png"},
        #                {"id": 5, "url": "570269c0f2302.png"}, ]
        db.session.add(item)
        db.session.commit()
        flash("New Item Edited!!")
        # return redirect(url_for('mobile.get_item_json'))
    else:
        return render_template('shop/EditItem.html', item=item, main_cats=main_cats)
        # else:
        #     return render_template('gentelella/production/login.html')


@mod_site.route('/deleteShopItem/<int:shop_id>/<int:item_id>/', methods=['GET', 'POST'])
@login_required
# route for deleteShopItem function here
@set_renderers(HTMLRenderer)
def delete_shop_item(shop_id, item_id):
    shop = db.session.query(models.Shop).filter_by(id=shop_id).one()
    item = db.session.query(models.Items).filter_by(id=item_id, shop_id=shop_id).one()
    if int(current_user.id) == int(shop_id):
        if request.method == 'POST':
            db.session.delete(item)
            db.session.commit()
            flash("New Item DELETED!!")
            return redirect(url_for('website.get_shop_items', shop_id=shop_id))
        else:
            return render_template('shop/DeleteItem.html', shop=shop, item=item)
    return redirect(url_for('website.unauthorized_handler'))


@mod_site.route('/stock', methods=['GET', 'POST'])
# route for deleteShopItem function here
@set_renderers(HTMLRenderer)
def stock_chart():
    agent = None
    stock = db.session.query(models.Stock).filter_by(id=1).one()
    items = db.session.query(models.StockValues).filter_by(stock_id=stock.id).all()
    return render_template('shop/stock_chart.html', items=[item.serialize for item in items], agent=agent)


@mod_site.route('/myOrders/<int:shop_id>', methods=['GET', 'POST'])
@login_required
# route for myOrders function here
@set_renderers(HTMLRenderer)
def get_shop_orders(shop_id):
    shop = db.session.query(models.Shop).filter_by(id=shop_id).one()
    if int(current_user.id) == int(shop_id):
        orders = db.session.query(models.Orders).join(models.Items).filter(models.Items.shop_id == shop_id)
        return render_template('shop/OrdersList.html', shop=shop, orders=orders)
    return redirect(url_for('website.unauthorized_handler'))


@mod_site.route("/login_agent", methods=["GET", "POST"])
@set_renderers(HTMLRenderer)
def login_agent():
    if request.method == 'POST':
        print("POST")
        errors = []
        username = request.form.get('username')
        password = request.form.get('password')
        print(username + ":" + password)
        agent = db.session.query(models.Agents).filter_by(email=username, passwd=password).first()
        if agent is None:
            # flash('Username or Password is invalid', 'error')
            errors.append("Username or Password is invalid")
            return redirect(url_for('login'))
        else:
            login_user(agent)
            # flash('Logged in successfully')
            return redirect(request.args.get('next') or url_for('website.welcome'))
    else:
        return render_template('gentelella/production/login.html')
