'''
Author: Kaleem Ullah (k.ullah@uva.nl)
This program serves as a template for a Flask app to track two variables: 
(1) time spent on a specified page & (2) whether a specified button clicked or not. 
Consult ReadMe.pdf for more information.
'''

from flask import Flask, request, session, render_template, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask import redirect, url_for
import traceback

# Configure app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Configure flask session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database and database models
db = SQLAlchemy(app)

# Database model for the continuous variable: time spent
class PageView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.String(10))
    page = db.Column(db.String(255))
    time_spent = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)

# Database model for the binary variable: button click
class Button(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.String(10))
    button = db.Column(db.Boolean)
    name = db.Column(db.String(50))

# Create all the tables for the databases
with app.app_context():
    db.create_all()

# Function to log data: this function saves the time spent on the previous page in the database. Unit of time is seconds. 
def log_data():
    try:
        time_spent = (datetime.now() - start_time).total_seconds()

        # 0 seconds is the threshold to save the time spent in the database. It is to eliminate recording repetitive page requests/reloads. 
        if time_spent > 0:
            page_view = PageView(
                visitor_id=session.get('visitor_id'),
                page=previous_path,
                time_spent=time_spent,
                start_time=start_time)
            db.session.add(page_view)
            db.session.commit()
    except:
        pass

##################################################################################
#
# After Each Request...
#
##################################################################################

# after_request decorator of Flask defines actions to be performed after each request coming from the client-side. 
@app.after_request
def track_time(response):
    global start_time
    global previous_path

    # Every time the user requests default route (/), time spent in the previous path is recorded in the database with log_data(). 
    if request.path == '/':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'HomePage'

    # Every time the user requests /learn_more route, time spent in the previous path is recorded in the database with log_data(). 
    if request.path == '/About_OpenKAT':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'About OpenKAT'

    if request.path == '/Experiences':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'Experiences'

    # Every time the user requests  /confirmation route, time spent in the previous path is recorded in the database with log_data(). 
    if request.path == '/Contact':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'Contact'

    if request.path == '/OpenKAT_website':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'OpenKAT.nl'
    
    if request.path == '/Government_website':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'government.nl'
    
    if request.path == '/Kennisnet_website':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'kennisnet.nl'
    
    if request.path == '/BDO_website':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'bdo.nl'

    if request.path == '/Bravis_website':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'bravisziekenhuis.nl'

    if request.path == '/Catharina_website':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'catharinaziekenhuis.nl'
    
    if request.path == '/SDB_website':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'sdbgroep.nl'

    if request.path == '/linkedin_group':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'LinkedIn Group'

    if request.path == '/github':
        log_data()
        # Update start_time and previous_path
        start_time = datetime.now()
        previous_path = 'GitHub'
    
    return response

##################################################################################
#
# Routes
#
##################################################################################

def index():
    # Getting the unique id from the home page URL. The unique URL will be generated by Qualtrics for each visitor. 
    visitor_id = request.args.get('uid')
    # Add visitor_id to the session
    if visitor_id:
        session["visitor_id"] = visitor_id
    
    return render_template('index.html')

@app.route('/')
def homepage():

    try:
        button_click = Button(
            visitor_id=session.get('visitor_id'),
            button=True, name='Home navbar')
        
        db.session.add(button_click)
        db.session.commit()
    except:
        pass  
    
    return render_template('index.html')

@app.route('/About_OpenKAT', methods=['GET'])
def learn_more():
    but_type = request.args.get('but_type','Learn More')
    try:
        button_click = Button(
            visitor_id=session.get('visitor_id'),
            button=True, name = but_type)
        db.session.add(button_click)
        db.session.commit()
    except:
        pass
    return render_template('aboutopenkat.html')


@app.route('/Experiences')
def exp():

    try:
        button_click = Button(
            visitor_id=session.get('visitor_id'),
            button=True, name='Experiences navbar')
        
        db.session.add(button_click)
        db.session.commit()
    except:
        pass  
    
    return render_template('Experiences.html')

@app.route('/Contact', methods=['GET'])
def get_in_touch():
    but_type = request.args.get('but_type','Get in Touch')
    try:
        button_click = Button(
            visitor_id=session.get('visitor_id'),
            button=True, name = but_type)
        db.session.add(button_click)
        db.session.commit()
    except:
        pass
    return render_template('Contact.html') 

@app.route('/OpenKAT_website')
def track_opekatnl():

    try:
        button_click = Button(
            visitor_id=session.get('visitor_id'),
            button=True, name='OpenKAT.nl')
        
        db.session.add(button_click)
        db.session.commit()
    except: pass        

    return redirect('https://openkat.nl')

@app.route('/Government_website')
def track_governmentnl():

    try:
        button_click = Button(
            visitor_id=session.get('visitor_id'),
            button=True, name='government.nl')
        
        db.session.add(button_click)
        db.session.commit()
    except: pass        

    return redirect('https://www.government.nl/ministries/ministry-of-health-welfare-and-sport')

@app.route('/Kennisnet_website')
def track_kennisnetnl():

    try:
        button_click = Button(
            visitor_id=session.get('visitor_id'),
            button=True, name='kennisnet.nl')
        
        db.session.add(button_click)
        db.session.commit()
    except: pass        

    return redirect('https://www.kennisnet.nl')

@app.route('/BDO_website')
def track_bdonl():

    try:
        button_click = Button(
            visitor_id=session.get('visitor_id'),
            button=True, name='bdo.nl')
        
        db.session.add(button_click)
        db.session.commit()
    except: pass        

    return redirect('https://www.bdo.nl/en-gb/bdo-netherlands')

@app.route('/Bravis_website')
def track_bravisnl():

    try:
        button_click = Button(
            visitor_id=session.get('visitor_id'),
            button=True, name='bravisziekenhuis.nl')
        
        db.session.add(button_click)
        db.session.commit()
    except: pass        

    return redirect('https://www.bravisziekenhuis.nl')

@app.route('/Catharina_website')
def track_catharinanl():

    try:
        button_click = Button(
            visitor_id=session.get('visitor_id'),
            button=True, name='catharinaziekenhuis.nl')
        
        db.session.add(button_click)
        db.session.commit()
    except: pass        

    return redirect('https://www.catharinaziekenhuis.nl')

@app.route('/SDB_website')
def track_sdbnl():

    try:
        button_click = Button(
            visitor_id=session.get('visitor_id'),
            button=True, name='sdbgroep.nl')
        
        db.session.add(button_click)
        db.session.commit()
    except: pass        

    return redirect('https://www.sdbgroep.nl')

@app.route('/linkedin_group')
def track_linkedin():

    try:
        button_click = Button(
            visitor_id=session.get('visitor_id'),
            button=True, name='LinkedIn Group')
        
        db.session.add(button_click)
        db.session.commit()
    except: pass        

    return redirect('https://www.linkedin.com/groups/12594016/')

@app.route('/github')
def track_github():

    try:
        button_click = Button(
            visitor_id=session.get('visitor_id'),
            button=True, name='GitHub')
        
        db.session.add(button_click)
        db.session.commit()
    except: pass        

    return redirect('https://github.com/minvws/nl-kat-coordination')




if __name__ == '__main__':
    app.run(port=3000, debug=True)