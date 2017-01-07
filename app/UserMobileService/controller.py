# coding=utf-8
from _ast import mod
from flask.ext.login import login_required
import json
import pandas
from flask import Blueprint, request, jsonify, render_template, url_for, Response, flash, send_from_directory, redirect
from app import db, API_KEY, API_KEY_ERROR, client, APP_ROOT
from app import models
from marshmallow import Schema, fields, pprint

__author__ = 'fantom'

mod_mobile_user = Blueprint('mobile', __name__)


# Date handler for Create and Update Date
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


# user related functions
# 1_user login by @email and @password
@mod_mobile_user.route('/loginCustomer', methods=['GET', 'POST'])
def login():
    if request.headers.get('Authorization') == API_KEY:
        req_json = request.get_json()
        username = req_json['email']
        password = req_json['password']
        user = db.session.query(models.Customer).filter_by(email=username).all()
        if len(user) > 0:
            if user[0].password == password:
                return user[0].serialize
            else:
                # wrong password
                return jsonify(response=-1)
        else:
            # no matching email
            return jsonify(response=-2)
    return API_KEY_ERROR


@mod_mobile_user.route('/loginBroker', methods=['GET', 'POST'])
def login():
    if request.headers.get('Authorization') == API_KEY:
        req_json = request.get_json()
        username = req_json['email']
        password = req_json['password']
        user = db.session.query(models.Broker).filter_by(email=username).all()
        if len(user) > 0:
            if user[0].password == password:
                return user[0].serialize
            else:
                # wrong password
                return jsonify(response=-1)
        else:
            # no matching email
            return jsonify(response=-2)
    return API_KEY_ERROR


@mod_mobile_user.route('/loginCompany', methods=['GET', 'POST'])
def login():
    if request.headers.get('Authorization') == API_KEY:
        req_json = request.get_json()
        username = req_json['email']
        password = req_json['password']
        user = db.session.query(models.Company).filter_by(email=username).all()
        if len(user) > 0:
            if user[0].password == password:
                return user[0].serialize
            else:
                # wrong password
                return jsonify(response=-1)
        else:
            # no matching email
            return jsonify(response=-2)
    return API_KEY_ERROR


@mod_mobile_user.route('/resetPass', methods=['GET', 'POST'])
def reset_password():
    if request.headers.get('Authorization') == API_KEY:
        req_json = request.get_json()
        user_id = req_json['user_id']
        user = db.session.query(models.Users).filter_by(id=user_id).first()
        if user:
            user.passwd = req_json['password']
            db.session.add(user)
            db.session.commit()
            return jsonify(response=1)
        else:
            return jsonify(response=-2)
    return API_KEY_ERROR


# sign up user by @email and @password
@mod_mobile_user.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.headers.get('Authorization') == API_KEY:
        req_json = request.get_json()
        first_name = req_json['first_name']
        last_name = req_json['last_name']
        username = req_json['email']
        password = req_json['password']
        gender = req_json['gender']
        birthday = req_json['birthday']
        if db.session.query(models.Users).filter_by(email=username):
            user = db.session.query(models.Users).filter_by(email=username).all()
            if len(user) > 0:
                if user[0].email == username:
                    # email already exist
                    return {"response": -2}
                    # if user[0].mobile == mobile:
                    #     # mobile already exist
                    #     return {"response": -3}
            else:
                user = models.Users(first_name=first_name, last_name=last_name, email=username, passwd=password,
                                    gender=gender, birthday=birthday)
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
            return jsonify(response=-1)
    else:
        return API_KEY_ERROR


# register device for push notifications
@mod_mobile_user.route('/registerDevice', methods=['GET', 'POST'])
def register_device():
    if request.headers.get('Authorization') == API_KEY:
        req_json = request.get_json()
        user_id = req_json['user_id']
        device_token = req_json['device_token']
        user = db.session.query(models.Users).filter_by(id=user_id).one()
        user.device_token = device_token
        print(device_token)
        client.send(device_token, "welcome To HyperTechno")
        client.send(device_token, "مرحبا بكم في هايبرتكنو")
        db.session.add(user)
        db.session.commit()
        return jsonify(response=device_token)
    return API_KEY_ERROR


# register device for push notifications
@mod_mobile_user.route('/registerDeviceAnonymous', methods=['GET', 'POST'])
def register_device_anonymous():
    if request.headers.get('Authorization') == API_KEY:
        req_json = request.get_json()
        token = req_json['device_token']
        device_token = models.DeviceTokens(device_token=req_json['device_token'])
        # user = db.session.query(models.Users).filter_by(id=user_id).one()
        # user.device_token = device_token
        print(token)
        client.send(token, "welcome To HyperTechno")
        client.send(token, "مرحبا بكم في هايبرتكنو")
        db.session.add(device_token)
        db.session.commit()
        return device_token.serialize
    return API_KEY_ERROR


# Home page display 4 items from all categories
@mod_mobile_user.route('/HomePage', defaults={'page': 1})
@mod_mobile_user.route('/HomePage/page/<int:page>')
def home_page(page):
    if request.headers.get('Authorization') == API_KEY:
        out_put = []
        categories = models.MainCategory.query.paginate(page, 4, False).items
        for category in categories[:4]:
            items = db.session.query(models.Products).filter_by(id_main_category=category.id)
            sub_cat_array = {'category': category.serialize, 'Products': [i.serialize for i in items[:4]]}
            out_put.append(sub_cat_array)
        return out_put
    return API_KEY_ERROR


# display item detail by @item_id
@mod_mobile_user.route('/GetItem', methods=['GET', 'POST'])
def get_item_json():
    if request.headers.get('Authorization') == API_KEY:
        req_json = request.get_json()
        item_id = req_json['item_id']
        print item_id
        items = db.session.query(models.Products).filter_by(id=item_id)
        return [i.serialize for i in items]
    return API_KEY_ERROR


# display items in category by @cat_id
@mod_mobile_user.route('/GetItemByCategory', methods=['GET', 'POST'])
def get_item_by_cat_json():
    if request.headers.get('Authorization') == API_KEY:
        print(request)
        req_json = request.get_json()
        cat_id = req_json['cat_id']
        items = db.session.query(models.Products).filter_by(id_category=cat_id)
        return [i.serialize for i in items]
    return API_KEY_ERROR


# @mod_mobile_user.route('/GetSubCategoriesById/<int:cat_id>/JSON')
# def get_sub_categories_by_id(cat_id):
#     if request.headers.get('Authorization') == API_KEY:
#         categories = db.session.query(models.Category).filter_by(parentCat=cat_id)
#         return [i.serialize for i in categories]
#     return API_KEY_ERROR


# display category details by id
@mod_mobile_user.route('/GetCategoryById', methods=['GET', 'POST'])
def get_category_by_id():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            cat_id = req_json['cat_id']
            category = db.session.query(models.Category).filter_by(id=cat_id)
            return [i.serialize for i in category]
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR


# display all categories details
@mod_mobile_user.route('/GetAllCategories/', defaults={'page': 1})
@mod_mobile_user.route('/GetAllCategories/page/<int:page>')
def get_all_cat_json(page):
    if request.headers.get('Authorization') == API_KEY:
        cats = models.MainCategory.query.paginate(page, 1, False)
        print(cats)
        if not cats and page != 1:
            return 404
        return [i.query_sub for i in cats.items]
    return API_KEY_ERROR


# @mod_mobile_user.route('/makeOrder/<int:item_id>/<int:user_id>')
# def make_order_temp(item_id, user_id):
#     if request.headers.get('Authorization') == API_KEY:
#         item = db.session.query(models.Items).filter_by(id=item_id).one()
#         user = db.session.query(models.User).filter_by(id=user_id).one()
#         order = models.Orders(user=user, item=item, quantity=1)
#         db.session.add(order)
#         db.session.commit()
#         orders = db.session.query(models.Orders).all()
#         return jsonify(orders=[i.serialize for i in orders])
#     return API_KEY_ERROR


# @mod_mobile_user.route('/GetProduct/<int:product_id>/JSON')
# def get_shop(product_id):
#     if request.headers.get('Authorization') == API_KEY:
#         shops = db.session.query(models.Products).filter_by(id=product_id)
#         return [i.serialize for i in shops]
#     return API_KEY_ERROR


# @mod_mobile_user.route('/GetShopItems/<int:shop_id>/JSON')
# def get_shop_items_json(shop_id):
#     if request.headers.get('Authorization') == API_KEY:
#         items = db.session.query(models.Items).filter_by(shop_id=shop_id)
#         return [i.serialize for i in items]
#     return API_KEY_ERROR

@mod_mobile_user.route('/AddItemImage', methods=['GET', 'POST'])
def add_item_image_json():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            item_id = req_json['item_id']
            image_url = req_json['image_url']
            image = models.Images(url=image_url)
            db.session.add(image)
            db.session.flush()
            image_id = image.id
            print item_id
            item = db.session.query(models.Products).filter_by(id=item_id)
            item_image = models.ProductImages(id_product=item.id, id_image=image_id)
            db.session.add(item_image)
            db.session.commit()
            return [i.serialize for i in item]
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR


@mod_mobile_user.route('/AddReview', methods=['GET', 'POST'])
def add_item_review():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            user_id = req_json['user_id']
            item_id = req_json['item_id']
            rate = req_json['rate']
            review = req_json['review']
            user = db.session.query(models.Users).filter_by(id=user_id).first()
            product = db.session.query(models.Products).filter_by(id=item_id).first()
            if user:
                if product:
                    review = models.ProductReview(user=user, product=product, rate=rate, review=review)
                    db.session.add(review)
                    db.session.flush()
                    review_id = review.id
                    db.session.commit()
                    return jsonify(response=review_id)
                else:
                    return jsonify(response=-2)
            else:
                return jsonify(response=-3)
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR


@mod_mobile_user.route('/GetItemReview', methods=['GET', 'POST'])
def get_item_review():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            item_id = req_json['item_id']
            review = db.session.query(models.ProductReview).filter_by(id_product=item_id)
            return [i.serialize for i in review]
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR


@mod_mobile_user.route('/GetUserReview', methods=['GET', 'POST'])
def get_user_review():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            user_id = req_json['user_id']
            review = db.session.query(models.ProductReview).filter_by(id_user=user_id)
            return [i.serialize for i in review]
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR


@mod_mobile_user.route('/AddItemMainImage', methods=['GET', 'POST'])
def add_item_main_image_json():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            item_id = req_json['item_id']
            image_url = req_json['image_url']
            print item_id
            item = db.session.query(models.Products).filter_by(id=item_id)
            item.main_image = image_url
            db.session.add(item)
            db.session.commit()
            return [i.serialize for i in item]
        else:
            return {'error': 'POST request is REQUIRED!!'}
    return API_KEY_ERROR


# @mod_mobile_user.route('/ClearAllProducts', methods=['GET', 'POST'])
# def delete_all_cat_json():
#     if request.headers.get('Authorization') == API_KEY:
#         try:
#             products_deleted = db.session.query(models.Products).delete()
#             cats_deleted = db.session.query(models.Category).delete()
#             db.session.commit()
#             return "No of Products: " + products_deleted + " \nNo of Cat: " + cats_deleted
#         except:
#             db.session.rollback()
#             return "Nothing to delete"
#     return API_KEY_ERROR


@mod_mobile_user.route('/ClearAll', methods=['GET', 'POST'])
def delete_all_cat_json():
    if request.headers.get('Authorization') == API_KEY:
        try:
            products_deleted = db.session.query(models.Products).delete()
            main_cats_deleted = db.session.query(models.Category).delete()
            cats_deleted = db.session.query(models.MainCategory).delete()
            db.session.commit()
            return "No of Products: " + products_deleted + " \nNo of Cat: " \
                   + cats_deleted + " \nNo of main: " + main_cats_deleted
        except:
            db.session.rollback()
            return "Nothing to delete"
    return API_KEY_ERROR


# @mod_mobile_user.route('/newShopItem', methods=['GET', 'POST'])
# # Task 1: Create route for newShopItem function here
# def new_shop_item():
#     req_json = request.get_json()
#     shop_id = req_json['shop_id']
#     name = req_json['name']
#     quantity = req_json['quantity']
#     price = req_json['price']
#     description = req_json['description']
#     # short_description = req_json['short_description']
#     image = req_json['image']
#     cat_id = req_json['cat_id']
#     global new_item
#     shop = db.session.query(models.Shop).filter_by(id=shop_id).one()
#     if request.method == 'POST':
#         category = db.session.query(models.SubCategory).filter_by(id=cat_id).one()
#         new_item = models.Items(name=name, quantity=quantity, shop=shop, SubCategory=category,
#                                 # short_description=short_description,
#                                 price=price, description=description, image=image)
#         try:
#             db.session.add(new_item)
#             db.session.flush()
#             new_id = new_item.id
#             db.session.commit()
#         except:
#             db.session.rollback()
#             raise
#         return {"response": new_id}
#     else:
#         return {"response": -1}


# @mod_mobile_user.route('/editShopItem', methods=['GET', 'POST'])
# # Task 2: Create route for editShopItem function here
# def edit_shop_item():
#     if request.headers.get('Authorization') == API_KEY:
#         req_json = request.get_json()
#         shop_id = req_json['shop_id']
#         item_id = req_json['item_id']
#         shop = db.session.query(models.Shop).filter_by(id=shop_id).one()
#         categories = db.session.query(models.SubCategory).all()
#         item = db.session.query(models.Items).filter_by(id=item_id, shop_id=shop_id).one()
#         if request.method == 'POST':
#             if not (req_json['name'] is None):
#                 item.name = req_json['name']
#             if not (req_json['description'] is None):
#                 item.description = req_json['description']
#             # if not (req_json['short_description'] is None):
#             #     item.description = req_json['short_description']
#             if not (req_json['quantity'] is None):
#                 item.quantity = req_json['quantity']
#             if not (req_json['price'] is None):
#                 item.price = req_json['price']
#             if not (req_json['cat_id'] is None):
#                 item.category = db.session.query(models.SubCategory).filter_by(id=req_json['cat_id']).one()
#                 item.cat_id = req_json['cat_id']
#             if not (req_json['image'] is None):
#                 # filename = secure_filename(image_file.filename)
#                 item.image = req_json['image']
#             db.session.add(item)
#             db.session.commit()
#             # flash("New Item Edited!!")
#             return {"response": 1}
#         else:
#             return render_template('editMenuItem.html', shop=shop, item=item, categories=categories)
#     return API_KEY_ERROR


# @mod_mobile_user.route('/deleteShopItem/<int:shop_id>/<int:item_id>/', methods=['GET', 'POST'])
# # Task 3: Create route for deleteShopItem function here
# def delete_shop_item(shop_id, item_id):
#     shop = db.session.query(models.Shop).filter_by(id=shop_id).one()
#     item = db.session.query(models.Items).filter_by(id=item_id, shop_id=shop_id).one()
#     if request.method == 'POST':
#         db.session.delete(item)
#         db.session.commit()
#         # flash("New Item DELETED!!")
#         return redirect(url_for('get_shop_items_json', shop_id=shop_id))
#     else:
#         return render_template('deleteMenuItem.html', shop=shop, item=item)


# @mod_mobile_user.route('/signupShop', methods=['GET', 'POST'])
# def signup_shop():
#     if request.headers.get('Authorization') == API_KEY:
#         req_json = request.get_json()
#         # shop_name = req_json['shop_name']
#         # shop_profile_pic = req_json['shop_profile_pic']
#         # shop_cover_pic = req_json['shop_cover_pic']
#         mobile = req_json['mobile']
#         # short_description = req_json['short_description']
#         # description = req_json['description']
#         # longitude = req_json['longitude']
#         # latitude = req_json['latitude']
#         # shop_address = req_json['shop_address']
#         owner_name = req_json['owner_name']
#         owner_email = req_json['owner_email']
#         password = req_json['password']
#         if db.session.query(models.Shop).filter_by(owner_email=owner_email):
#             shop = db.session.query(models.Shop).filter_by(owner_email=owner_email).all()
#             if len(shop) > 0:
#                 if shop[0].owner_email == owner_email:
#                     # name already exist
#                     return {"response": shop[0].id}
#             else:
#                 shop = models.Shop(owner_name=owner_name, owner_email=owner_email, password=password, mobile=mobile)
#                 try:
#                     db.session.add(shop)
#                     db.session.flush()
#                     new_id = shop.id
#                     db.session.commit()
#                 except:
#                     db.session.rollback()
#                     raise
#                 return {"response": new_id}
#         else:
#             return {"response": -1}
#     return API_KEY_ERROR


# @mod_mobile_user.route('/loginShop', methods=['GET', 'POST'])
# def login_shop():
#     if request.headers.get('Authorization') == API_KEY:
#         req_json = request.get_json()
#         username = req_json['email']
#         password = req_json['password']
#         user = db.session.query(models.Shop).filter_by(owner_email=username).all()
#         if len(user) > 0:
#             if user[0].password == password:
#                 return {"response": user[0].id}
#             else:
#                 # wrong password
#                 return {"response": -1}
#         else:
#             # no matching email
#             return {"response": -2}
#     return API_KEY_ERROR


# # ToDo
# @mod_mobile_user.route('/addToCart', methods=['GET', 'POST'])
# def add_to_cart():
#     if request.headers.get('Authorization') == API_KEY:
#         user = db.session.query(models.Users).filter_by(id=user_id).one()
#         item = db.session.query(models.Products).filter_by(id=item_id).one()
#         db.session.merge(models.Cart(user=user, item=item))
#         db.session.commit()
#         return redirect(url_for('get_user_shop_cart', user_id=user_id))
#     return API_KEY_ERROR


@mod_mobile_user.route('/newOrder/<int:user_id>', methods=['GET', 'POST'])
def add_to_shop_cart(user_id, item_id):
    if request.headers.get('Authorization') == API_KEY:
        user = db.session.query(models.Users).filter_by(id=user_id).one()
        item = db.session.query(models.Products).filter_by(id=item_id).one()
        db.session.merge(models.Cart(user=user, item=item))
        db.session.commit()
        return redirect(url_for('get_user_shop_cart', user_id=user_id))
    return API_KEY_ERROR


# ToDo
@mod_mobile_user.route('/removeFromShopCart/<int:user_id>/<int:item_id>', methods=['GET', 'POST'])
def remove_from_shop_cart(user_id, item_id):
    if request.headers.get('Authorization') == API_KEY:
        user = db.session.query(models.Users).filter_by(id=user_id).one()
        item = db.session.query(models.Products).filter_by(id=item_id).one()
        if db.session.query(models.Cart).filter_by(user=user, item=item):
            db.session.query(models.Cart).filter_by(user=user, item=item).one()
            db.session.delete(item)
            db.session.commit()
            return redirect(url_for('get_user_shop_cart', user_id=user_id))
        return redirect(url_for('get_user_shop_cart', user_id=user_id))
    return API_KEY_ERROR


@mod_mobile_user.route('/getUserShopCart/<int:user_id>/', methods=['GET', 'POST'])
def get_user_shop_cart(user_id):
    if request.headers.get('Authorization') == API_KEY:
        cart_items = db.session.query(models.ShoppingCart).filter_by(user_id=user_id).all()
        return [i.serialize for i in cart_items]
    return API_KEY_ERROR


@mod_mobile_user.route('/registerShopDevice', methods=['GET', 'POST'])
def register_shop_device():
    if request.headers.get('Authorization') == API_KEY:
        req_json = request.get_json()
        shop_id = req_json['shop_id']
        device_token = req_json['device_token']
        shop = db.session.query(models.Shop).filter_by(id=shop_id).one()
        shop.device_token = device_token
        print(device_token)
        # client.send(device_token, "welcome To Bubble!!")
        db.session.add(shop)
        db.session.commit()
        return {"response": device_token}
    return API_KEY_ERROR


@mod_mobile_user.route('/sendPushAll', methods=['GET', 'POST'])
# @set_renderers(HTMLRenderer)
def send_push_all():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == "POST":
            users = db.session.query(models.User).all()
            message = request.form['message']
            title = request.form['title']
            body = request.form['body']
            icon = request.form['icon']
            for user in users:
                if None is not user.device_token:
                    client.send(user.device_token, message,
                                notification={'title': title, 'body': body, 'icon': icon})
                    flash("Sent To" + user.name)
        else:
            return '''
        <form action="" method="post">
            <p><input type=text name=message>
            <p><input type=text name=title>
            <p><input type=text name=body>
            <p><input type=text name=icon>
            <p><input type=submit value=Send>
        </form>
        '''
    return API_KEY_ERROR


@mod_mobile_user.route('/getOrdersByShopID', methods=['GET', 'POST'])
# @login_required
# Task 3: Create route for deleteShopItem function here
def get_shop_orders():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            shop_id = int(request.data.get('shop_id', ''))
            orders = db.session.query(models.Orders).join(models.Items).filter(models.Items.shop_id == shop_id)
            return [i.serialize for i in orders]
    return API_KEY_ERROR


@mod_mobile_user.route("/export", methods=['GET'])
@login_required
def doexport():
    orders = db.session.query(models.Orders).all()
    data = [i.serialize for i in orders]
    print(data)
    json_data = json.dumps(data, default=date_handler)
    pandas.read_json(json_data).to_excel("output.xlsx")
    return send_from_directory(directory=APP_ROOT, filename="output.xlsx")


@mod_mobile_user.route('/editUser', methods=['GET', 'POST'])
def edit_user():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            user_id = req_json['user_id']
            name = req_json['name']
            email = req_json['email']
            gender = req_json['gender']
            password = req_json['password']
            birthday = req_json['birthday']
            profile_pic = req_json['profile_pic']
            user = db.session.query(models.Users).filter_by(id=user_id).one()
            if not (name is None):
                user.name = name
            if not (email is None):
                user.email = email
            if not (gender is None):
                user.gender = gender
            if not (password is None):
                user.password = password
            # if not (mobile is None):
            #     user.mobile = mobile
            if not (profile_pic is None):
                user.profile_pic = profile_pic
            if not (birthday is None):
                user.birthday = birthday
            db.session.add(user)
            db.session.commit()
            # flash("New Item Added!!")
            return jsonify(response=1)
        else:
            return jsonify(response=-1)
    else:
        return API_KEY_ERROR


@mod_mobile_user.route('/editCategory', methods=['GET', 'POST'])
def edit_category():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            cat_id = req_json['cat_id']
            name = req_json['name']
            has_sub = req_json['hasSub']
            cat = db.session.query(models.Category).filter_by(id=cat_id).one()
            if not (name is None):
                cat.name = name
            if not (has_sub is None):
                cat.hasSub = has_sub
            db.session.add(cat)
            db.session.commit()
            # flash("New Item Added!!")
            return "Success"
    return API_KEY_ERROR


@mod_mobile_user.route('/newCategory', methods=['GET', 'POST'])
def new_category():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            if request.form['name'] and request.form['hasSub']:
                new_cat = models.Category(name=request.form['name'], hasSub=request.form['hasSub'])
                db.session.add(new_cat)
                db.session.commit()
            # flash("New Item Added!!")
            return redirect(url_for('get_all_categories'))
        else:
            return render_template('newCategory.html')
    return API_KEY_ERROR


@mod_mobile_user.route('/newSubCategory', methods=['GET', 'POST'])
def new_sub_category():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            cat_id = req_json['cat_id']
            name = req_json['name']
            cat = db.session.query(models.Category).filter_by(id=cat_id).one()
            if not (name is None):
                new_cat = models.SubCategory(name=name, category=cat)
                db.session.add(new_cat)
                db.session.commit()
            # flash("New Item Added!!")
            return 1
    return API_KEY_ERROR


@mod_mobile_user.route('/editSubCategory', methods=['GET', 'POST'])
def edit_sub_category():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            cat_id = req_json['cat_id']
            name = req_json['name']
            parent_id = req_json['parent_id']
            cat = db.session.query(models.SubCategory).filter_by(id=cat_id).one()
            if not (name is None):
                cat.name = name
            if not (parent_id is None):
                cat.category = db.session.query(models.Category).filter_by(id=parent_id).one()
            db.session.add(cat)
            db.session.commit()
            # flash("New Item Added!!")
            return 1
    return API_KEY_ERROR


@mod_mobile_user.route('/addAddress', methods=['GET', 'POST'])
def add_address():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            user_id = req_json['user_id']
            user = db.session.query(models.Users).filter_by(id=user_id).one()
            floor_num = req_json['floor_num']
            building_num = req_json['building_num']
            street_name = req_json['street_name']
            longitude = req_json['longitude']
            latitude = req_json['latitude']
            if 'description' in req_json.keys():
                description = req_json['description']
                address = models.Address(user=user, floor_num=floor_num, building_num=building_num, longitude=longitude,
                                         street_name=street_name, description=description, latitude=latitude)
            else:
                address = models.Address(user=user, floor_num=floor_num, building_num=building_num, longitude=longitude,
                                         street_name=street_name, latitude=latitude)
            db.session.add(address)
            db.session.flush()
            db.session.commit()
            return jsonify(response=address.id)
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR


@mod_mobile_user.route('/getUserAddress', methods=['GET', 'POST'])
def get_addresses_user():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            user_id = req_json['user_id']
            address = db.session.query(models.Address).filter_by(id_user=user_id).all()
            return [i.serialize for i in address]
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR


@mod_mobile_user.route('/addPhone', methods=['GET', 'POST'])
def add_phone():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            user_id = req_json['user_id']
            code = req_json['code']
            number = req_json['number']
            user = db.session.query(models.Users).filter_by(id=user_id).first()
            phone = models.Phone(user=user, code=code, number=number)
            db.session.add(phone)
            db.session.flush()
            db.session.commit()
            return jsonify(response=phone.id)
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR


@mod_mobile_user.route('/getUserPhones', methods=['GET', 'POST'])
def get_phones_user():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            user_id = req_json['user_id']
            phone = db.session.query(models.Phone).filter_by(id_user=user_id).all()
            return [i.serialize for i in phone]
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR


@mod_mobile_user.route('/makeOrder', methods=['GET', 'POST'])
def make_order():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            user_id = req_json['user_id']
            items = req_json['items']
            user = db.session.query(models.Users).filter_by(id=user_id).one()
            status = db.session.query(models.OrderStatus).filter_by(id=1).one()
            order = models.Orders(user=user, status=status)
            db.session.add(order)
            db.session.commit()
            for item in items:
                product = db.session.query(models.Products).filter_by(id=item['item_id']).first()
                cart_item = models.Cart(product=product, quantity=item['quantity'], user=user, order=order)
                db.session.add(cart_item)
                db.session.commit()
            return order.query_sub
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR


@mod_mobile_user.route('/getOrdersByUser', methods=['GET', 'POST'])
def get_orders_by_user():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            user_id = req_json['user_id']
            orders = db.session.query(models.Orders).filter_by(id_user=user_id)
            return [i.serialize for i in orders]
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR


@mod_mobile_user.route('/getOrder', methods=['GET', 'POST'])
def get_order():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            order_id = req_json['order_id']
            order = db.session.query(models.Orders).filter_by(id=order_id)
            return order.query_sub
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR


@mod_mobile_user.route('/setOrderAddress', methods=['GET', 'POST'])
def set_order_address():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            order_id = req_json['order_id']
            address_id = req_json['address_id']
            address = db.session.query(models.Address).filter_by(id=address_id)
            order = db.session.query(models.Orders).filter_by(id=order_id)
            order.address = address
            return jsonify(response=1)
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR


@mod_mobile_user.route('/setOrderPhone', methods=['GET', 'POST'])
def set_order_phone():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            order_id = req_json['order_id']
            phone_id = req_json['phone_id']
            phone = db.session.query(models.Phone).filter_by(id=phone_id)
            order = db.session.query(models.Orders).filter_by(id=order_id)
            order.phone = phone
            return jsonify(response=1)
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR


@mod_mobile_user.route('/setOrderStatus', methods=['GET', 'POST'])
def set_order_status():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            order_id = req_json['order_id']
            status_id = req_json['status_id']
            order = db.session.query(models.Orders).filter_by(id=order_id)
            status = db.session.query(models.OrderStatus).filter_by(id=status_id)
            order.status = status
            return jsonify(response=1)
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR


@mod_mobile_user.route('/editOrdersByUser', methods=['GET', 'POST'])
def edit_orders_by_user():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            order_id = req_json['order_id']
            order = db.session.query(models.Orders).filter_by(id=order_id).one()
            if req_json['address_id'] is not None:
                order.shipping_address = db.session.query(models.Address).filter_by(id=req_json['shipping_address'])
            if req_json['phone_id'] is not None:
                order.phone = db.session.query(models.Phone).filter_by(id=req_json['phone_id'])
            db.session.add(order)
            db.session.commit()
            # return jsonify(orders=[i.serialize for i in orders])
            return jsonify(response=1)
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR


@mod_mobile_user.route('/getUser', methods=['GET', 'POST'])
def get_user():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            user_id = req_json['user_id']
            user = db.session.query(models.Users).filter_by(id=user_id)
            return [i.serialize for i in user]
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR


@mod_mobile_user.route('/editShop', methods=['GET', 'POST'])
# Task 1: Create route for newShopItem function here
def edit_shop():
    if request.headers.get('Authorization') == API_KEY:
        if request.method == 'POST':
            req_json = request.get_json()
            shop_id = req_json['shop_id']
            owner_name = req_json['owner_name']
            owner_email = req_json['owner_email']
            gender = req_json['gender']
            owner_date_of_birth = req_json['owner_date_of_birth']
            owner_profile_pic = req_json['owner_profile_pic']
            shop_name = req_json['shop_name']
            shop_profile_pic = req_json['shop_profile_pic']
            shop_cover_pic = req_json['shop_cover_pic']
            mobile = req_json['mobile']
            # short_description = req_json['short_description']
            description = req_json['description']
            longitude = req_json['longitude']
            latitude = req_json['latitude']
            shop_address = req_json['shop_address']
            shop = db.session.query(models.Shop).filter_by(id=shop_id).one()
            if not (owner_name is None):
                shop.owner_name = owner_name
            if not (owner_email is None):
                shop.owner_email = owner_email
            if not (gender is None):
                shop.gender = gender
            if not (owner_date_of_birth is None):
                shop.owner_date_of_birth = owner_date_of_birth
            if not (owner_profile_pic is None):
                shop.owner_profile_pic = owner_profile_pic
            if not (shop_name is None):
                shop.shop_name = shop_name
            if not (shop_profile_pic is None):
                shop.shop_profile_pic = shop_profile_pic
            if not (shop_cover_pic is None):
                shop.shop_cover_pic = shop_cover_pic
            if not (mobile is None):
                shop.mobile = mobile
            # if not (short_description is None):
            #     shop.short_description = short_description
            if not (description is None):
                shop.description = description
            if not (longitude is None):
                shop.longitude = longitude
            if not (latitude is None):
                shop.latitude = latitude
            if not (shop_address is None):
                shop.shop_address = shop_address
            db.session.add(shop)
            db.session.commit()
            # flash("New Item Added!!")
            return jsonify(response=1)
        else:
            return jsonify(response=-1)
    return API_KEY_ERROR
