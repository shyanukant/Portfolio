from flask import Flask, render_template, request, flash, redirect,session
from datetime import datetime
# from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_mail import Mail   # send mail using flsk mail for more https://pythonhosted.org/Flask-Mail/
from dotenv import load_dotenv
from pathlib import Path
import json
import os 

env_path = Path('.', '.env')
load_dotenv(dotenv_path=env_path)

# add database 
with open('config.json', 'r') as f:   # open config.json in readind mode
    params = json.load(f)["parameter"]
local_server = 'prod'
app = Flask(__name__, template_folder='template')
# set secret key
app.secret_key = os.getenv("APP_SECRET_KEY")
# configuring flask mail
app.config.update(
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = "465",
    MAIL_USE_SSL = True,
    MAIL_ASCII_ATTACHMENTS = True,
    MAIL_USERNAME = os.getenv("GMAIL_USER"),
    MAIL_PASSWORD = os.getenv("GMAIL_PASS")
)
mail = Mail(app)
if(local_server=='dev'):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
else:
    prodURI = os.getenv("DATABASE_URL")
    prodURI = prodURI.replace("postgres://", "postgresql://")
    app.config['SQLALCHEMY_DATABASE_URI'] = prodURI
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False


###################################### database table  #################################################

# connect with database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# contact form table data
class Contact(db.Model):
    Sno = db.Column (db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(300),  nullable=True)
    file = db.Column(db.String(500),  nullable=True)
    date = db.Column(db.DateTime )

# post table data
class project_post(db.Model):
    Sno = db.Column (db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False, nullable=False)
    slug = db.Column(db.String(30), unique=True, nullable=False)
    img_file = db.Column(db.String(500), unique=False, nullable=False)
    content = db.Column(db.Text(),  nullable=False)
    project_link = db.Column(db.String(50),  nullable=True)
    date = db.Column(db.DateTime )

###################################### pages  #################################################

###################################### ##########  #################################################
###################################### main pages  #################################################

@app.route("/")
def index():
    title = "Home"
    projects = project_post.query.filter_by().all()[0:params['no-of-project']]
    return render_template("index.html", title=title, params = params, projects = projects)


 # project post code
@app.route("/project/<string:project_slug>", methods=['GET'])  # url with variable with type
def project_route(project_slug = None):
    project = project_post.query.filter_by(slug = project_slug).first_or_404(description='There is no data with {}'.format(project_slug))  # fetch project post from database
    return render_template("project.html", params = params, project = project)

@app.route("/contact", methods= ['GET','POST'])  #post for add data in database
def Contact_view():
    title = "Contact"
    if(request.method == 'POST'):
        # add entry to the database
        Name = request.form.get('name')
        Email = request.form.get('email')
        Phone = request.form.get('phone')
        Message = request.form.get('message')       
        File = request.form.get('file')
        
        flash('Thanks For Contacting Me, I will Get Back to You Soon.', 'success')

        entry = Contact(name = Name, email = Email, phone = Phone, message = Message, file = File,  date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        
        mail.send_message('New massage from ' +Name,
                            sender = Email,
                            recipients = [os.getenv("GMAIL_USER")],  # Recieve mail after submit contact form
                            body = Message + "\n" + Phone +"\n" + Email + "\n" + File
                            
                        ) 
        
                        
        return redirect('/contact')
              
    return render_template("contact.html", title=title, params= params)

###################################### ###############  #################################################
###################################### admin pages  #################################################


@app.route("/edit/<string:sno>", methods = ['GET', 'POST'])
def edit(sno):
    if 'user' in session and session['user'] == os.getenv("ADMIN_USER"):
        if request.method == 'POST':
            title = request.form.get('title')
            slug = request.form.get('slug')
            content = request.form.get('content')
            link = request.form.get('prodLink')
            image = request.form.get('image')
            date = datetime.now()

            if sno == '0' : #if serial no is 0 then Add new post
                project = project_post(title = title, slug = slug, content = content, project_link=link, img_file = image, date = date)
                db.session.add(project)
                db.session.commit()

            else:
                project = project_post.query.filter_by(Sno = sno).first()
                project.title = title
                project.slug = slug
                project.content = content
                project.project_link = link
                project.img_file = image
                project.date = date

                db.session.commit()
                return redirect('/edit/'+sno)
        project = project_post.query.filter_by(Sno = sno).first()
        return render_template('edit.html', params=params, project = project, sno = sno)

# @app.route("/uploader", methods = ['GET', 'POST'])
# def uploader():
#     if 'user' in session and session['user']== os.getenv("ADMIN_USER"):
#         if request.method == 'POST':
#             f = request.files['file']
#             f.save(os.path.join(app.config['UPLOAD_FOLDER2'], secure_filename(f.filename) )) # save upload file in location with file name
#             # flash('Upload Succesfully, file= {}'.format(f), 'success')
#             return redirect("/admin")

@app.route("/admin", methods = ['GET', 'POST'])
def admin():
    # if user already login
    if 'user' in session and session['user'] == os.getenv("ADMIN_USER"):
        projects = project_post.query.all() #show all post in admin
        return render_template('admin.html', params=params, projects = projects)

    if request.method == 'POST':  #post request from user for enter in admin panel
        #REDIRECT TO ADMIN PANNEL and check username and password 
        username = request.form.get('username')
        userpass = request.form.get('userpass')

        if (username == os.getenv("ADMIN_USER") and userpass == os.getenv("ADMIN_PASSWORD")):
            # set the session variable here
            session['user'] = username
            projects = project_post.query.all()
            return render_template('admin.html', params= params, projects = projects)
    else:
        return render_template("login.html", params = params)

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/admin')

@app.route("/delete/<string:sno>", methods = ['GET', 'POST'])
def delete(sno):
    if 'user' in session and session['user'] == os.getenv("ADMIN_USER"):
        project = project_post.query.filter_by(Sno = sno).first()
        db.session.delete(project) # delete project
        db.session.commit()
    return redirect('/admin')

if __name__ == "__main__":
    app.run(port=8000)
    # app.run(debug=True, port=8000)