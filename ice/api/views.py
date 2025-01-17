#!venv/bin/python
from flask import request, jsonify, url_for, abort, g
from ..__init__ import app, auth
from ..models import *

@app.route('/')
@app.route('/index')
def index():
    return "Hello World!"


@app.route('/resource')
@app.route('/resource/')
@auth.login_required
def get_resource():
    return jsonify({'data': "Hello, %s!" % g.user.username})


@app.route('/token')
@app.route('/token/')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })


@app.route('/users', methods=['GET','POST'])
@app.route('/users/', methods=['GET','POST'])
def users():
    if request.method == 'GET':
        lim = request.args.get('limit', 10)
        off = request.args.get('offset', 0)
        users = UserDB.query.limit(lim).offset(off).all()
        json_users = map(get_user_json, users)
        return jsonify(users=json_users)
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')
        name = request.json.get('name')
        if username is None or password is None:
            abort(400) # missing arguments
        if UserDB.query.filter_by(username=username).first() is not None:
            print "User", username, "exists in the database"
            abort(400) # ^
        user = UserDB(username=username, email=email, name=name)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'username': user.username}), 201, {'Location': \
                url_for('user', username=user.username, _external=True)}


# Get a single user by username
@app.route('/users/<username>', methods=['GET'])
@app.route('/users/<username>/', methods=['GET'])
def user(username):
    if request.method == 'GET':
        user = UserDB.query.filter_by(username=username).first()
        return jsonify(user=get_user_json(user))


@app.route('/events', methods=['GET','POST'])
@app.route('/events/', methods=['GET','POST'])
def events():
    if request.method == 'GET':
        min = int(request.args.get('min', 0))
        max = int(request.args.get('max', 9001))
        events = EventDB.query.all()
        json_events = map(get_event_json, filter(lambda x: x.price in range(min,max+1), events))
        return jsonify(events=json_events)


# Get a single user by username
@app.route('/events/<event_id>', methods=['GET'])
@app.route('/events/<event_id>/', methods=['GET'])
def event(event_id):
    if request.method == 'GET':
        event = EventDB.query.filter_by(id=event_id).first()
        return jsonify(event=get_event_json(event))


@app.route('/addresses', methods=['GET', 'POST'])
@app.route('/addresses/', methods=['GET', 'POST'])
def address():
    if request.method == 'GET':
        lim = request.args.get('limit', 10)
        off = request.args.get('offset', 0)
        address = AddressDB.query.limit(lim).offset(off).all()
        json_addresses = map(get_address_json, address)
        return jsonify(addresses=json_address)


@app.route('/contacts', methods=['GET', 'POST'])
@app.route('/contacts/', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        lim = request.args.get('limit', 10)
        off = request.args.get('offset', 0)
        contact = ContactDB.query.limit(lim).offset(off).all()
        json_contacts = map(get_contact_json, contact)
        return jsonify(contacts=json_contact)


@app.route('/event_schedules', methods=['GET', 'POST'])
@app.route('/event_schedules/', methods=['GET', 'POST'])
def event_schedule():
    if request.method == 'GET':
        lim = request.args.get('limit', 10)
        off = request.args.get('offset', 0)
        event_schedule = EventScheduleDB.query.limit(lim).offset(off).all()
        json_event_schedules = map(get_event_schedule_json, event_schedule)
        return jsonify(event_schedules=json_event_schedule)


@app.route('/locations', methods=['GET', 'POST'])
@app.route('/locations/', methods=['GET', 'POST'])
def location():
    if request.method == 'GET':
        lim = request.args.get('limit', 10)
        off = request.args.get('offset', 0)
        location = LocationDB.query.limit(lim).offset(off).all()
        json_locations = map(get_location_json, location)
        return jsonify(locations=json_location)

@app.route('/roles', methods=['GET', 'POST'])
@app.route('/roles/', methods=['GET', 'POST'])
def role():
    if request.method == 'GET':
        lim = request.args.get('limit', 10)
        off = request.args.get('offset', 0)
        role = RoleDB.query.limit(lim).offset(off).all()
        json_roles = map(get_role_json, role)
        return jsonify(roles=json_role)




def get_event_json(event):
    if event is None:
        return None
    return {'id': event.id,
            'organizer_id': event.organizer_id,
            'location_id': event.location_id,
            'name': event.name,
            'price': event.price,
            'start_date': event.start_date }


def get_user_json(user):
    if user is None:
        return None
    return {'username': user.username,
            'email': user.email,
            'name': user.name }


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = UserDB.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = UserDB.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
