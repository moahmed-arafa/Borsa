from app import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import desc, asc

Base = declarative_base()
Base.query = db.session.query_property()


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    address = db.Column(db.String)
    password = db.Column(db.String)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    com_number = db.Column(db.Integer)
    tax_number = db.Column(db.Integer)
    date_add = db.Column(db.DateTime, server_default=db.func.now())
    date_upd = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    @property
    def serialize(self):
        # Returns object data in easily serialized format
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'com_number': self.com_number,
            'tax_number': self.tax_number,
            'date_add': self.date_add,
            'date_upd': self.date_upd
        }

        # @property
        # def query_sub(self):
        #     # Returns object data in easily serialized format
        #     subs = db.session.query(Cart).filter_by(id_order=self.id).all()
        #     address = db.session.query(Address).filter_by(id=self.id_address).first()
        #     phone = db.session.query(Phone).filter_by(id=self.id_phone).first()
        #     status = db.session.query(OrderStatus).filter_by(id=self.id_current_state).first()
        #     return {
        #         'id': self.id,
        #         'id_user': self.id_user,
        #         'current_state': None if status is None else status.serialize,
        #         'address': None if address is None else address.serialize,
        #         'phone': None if phone is None else phone.serialize,
        #         'active': self.active,
        #         'date_add': self.date_add,
        #         'date_upd': self.date_upd,
        #         'cart': [item.serialize for item in subs]
        #     }


class Stock(db.Model):
    __tablename__ = 'stock'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship(Company)
    current_value = db.Column(db.Float)
    last_value = db.Column(db.Float)
    type = db.Column(db.Binary)
    init_no = db.Column(db.Integer)
    curr_no = db.Column(db.Integer)
    date_add = db.Column(db.DateTime, server_default=db.func.now())
    date_upd = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    @property
    def serialize(self):
        # Returns object data in easily serialized format
        current_values = db.session.query(StockValues).filter_by(stock_id=self.id)\
            .order_by(desc(StockValues.date_add)).first()
        last_values = db.session.query(StockValues).filter_by(stock_id=self.id)\
            .order_by(asc(StockValues.date_add)).first()
        return {
            'id': self.id,
            'company_id': self.company_id,
            'current_value': None if current_values is None else current_values.value,
            'last_value': None if last_values is None else last_values.value,
            'type': self.type,
            'init_no': self.init_no,
            'curr_no': self.curr_no,
            'date_add': self.date_add,
            'date_upd': self.date_upd
        }


class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    password = db.Column(db.String)
    date_add = db.Column(db.DateTime, server_default=db.func.now())
    date_upd = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    @property
    def serialize(self):
        # Returns object data in easily serialized format
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'date_add': self.date_add,
            'date_upd': self.date_upd
        }


class Broker(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    password = db.Column(db.String)
    date_add = db.Column(db.DateTime, server_default=db.func.now())
    date_upd = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    @property
    def serialize(self):
        # Returns object data in easily serialized format
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'date_add': self.date_add,
            'date_upd': self.date_upd
        }


class CompanyCredit(db.Model):
    __tablename__ = 'company_credit'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship(Company)
    owner_name = db.Column(db.String)
    type = db.Column(db.String)
    number = db.Column(db.Integer)
    ex_date = db.Column(db.DateTime)
    csv = db.Column(db.Integer)
    date_add = db.Column(db.DateTime, server_default=db.func.now())
    date_upd = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    @property
    def serialize(self):
        # Returns object data in easily serialized format
        return {
            'id': self.id,
            'company_id': self.company_id,
            'owner_name': self.owner_name,
            'type': self.type,
            'number': self.number,
            'ex_date': self.ex_date,
            'csv': self.csv,
            'date_add': self.date_add,
            'date_upd': self.date_upd
        }


class BrokerCredit(db.Model):
    __tablename__ = 'broker_credit'

    id = db.Column(db.Integer, primary_key=True)
    broker_id = db.Column(db.Integer, db.ForeignKey('broker.id'))
    broker = db.relationship(Broker)
    owner_name = db.Column(db.String)
    type = db.Column(db.String)
    number = db.Column(db.Integer)
    ex_date = db.Column(db.DateTime)
    csv = db.Column(db.Integer)
    date_add = db.Column(db.DateTime, server_default=db.func.now())
    date_upd = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    @property
    def serialize(self):
        # Returns object data in easily serialized format
        return {
            'id': self.id,
            'broker': self.broker.serialize,
            'owner_name': self.owner_name,
            'type': self.type,
            'number': self.number,
            'ex_date': self.ex_date,
            'csv': self.csv,
            'date_add': self.date_add,
            'date_upd': self.date_upd
        }


class CustomerCredit(db.Model):
    __tablename__ = 'customer_credit'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship(Customer)
    owner_name = db.Column(db.String)
    type = db.Column(db.String)
    number = db.Column(db.Integer)
    ex_date = db.Column(db.DateTime)
    csv = db.Column(db.Integer)
    date_add = db.Column(db.DateTime, server_default=db.func.now())
    date_upd = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    @property
    def serialize(self):
        # Returns object data in easily serialized format
        return {
            'id': self.id,
            'company': self.company.serialize,
            'owner_name': self.owner_name,
            'type': self.type,
            'number': self.number,
            'ex_date': self.ex_date,
            'csv': self.csv,
            'date_add': self.date_add,
            'date_upd': self.date_upd
        }


class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
    stock = db.relationship(Stock)
    broker_id = db.Column(db.Integer, db.ForeignKey('broker.id'))
    broker = db.relationship(Broker)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship(Customer)
    quantity = db.Column(db.Integer)
    buy_value = db.Column(db.Float)
    sell_value = db.Column(db.Float)
    date_add = db.Column(db.DateTime, server_default=db.func.now())
    date_upd = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    @property
    def serialize(self):
        # Returns object data in easily serialized format
        return {
            'id': self.id,
            'stock': self.stock.serialize,
            'broker': self.broker.serialize,
            'customer': self.customer.serialize,
            'company': self.stock.company.serialize,
            'quantity': self.quantity,
            'buy_value': self.buy_value,
            'sell_value': self.sell_value,
            'date_add': self.date_add,
            'date_upd': self.date_upd
        }


class StockValues(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer)
    value = db.Column(db.Float)
    date_add = db.Column(db.DateTime, server_default=db.func.now())
    date_upd = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    @property
    def serialize(self):
        # Returns object data in easily serialized format
        return {
            'id': self.id,
            'stock_id': self.stock_id,
            'value': self.value,
            'date_add': self.date_add,
            'date_upd': self.date_upd
        }


class Request(db.Model):
    __tablename__ = 'request'

    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
    stock = db.relationship(Stock)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship(Customer)
    broker_id = db.Column(db.Integer, db.ForeignKey('broker.id'))
    broker = db.relationship(Broker)
    no_stocks = db.Column(db.Integer)
    active = db.Column(db.Boolean, server_default='true')
    date_add = db.Column(db.DateTime, server_default=db.func.now())
    date_upd = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    @property
    def serialize(self):
        # Returns object data in easily serialized format
        return {
            'id': self.id,
            'stock': self.stock.serialize,
            'customer_id': self.customer.serialize,
            'broker': self.broker.serialize,
            'no_stocks': self.no_stocks,
            'active': self.active,
            'date_add': self.date_add,
            'date_upd': self.date_upd
        }

    @property
    def serialize_many2many(self):
        """
        Return object's relations in easily serializeable format.
        NB! Calls many2many's serialize property.
        """
        return [item.serialize for item in self.parent]

