# Import the app variable from the init
from flask_nza import app, db

# Import specific packages from flask
from flask import render_template,request,redirect,url_for

#Import Our Form(s)
from flask_nza.forms import UserInfoForm, LoginForm, CnForm

# Import of our Model(s) for the Database
from flask_nza.models import User,Cn,check_password_hash 

# Import for Flask Login funcitons - login_recheck_password_hashquired
#  login_user, current_user, logout_user
from flask_login import login_required,login_user,current_user,logout_user

# Default Home Route
# routes are the traffic cop telling people where to go
@app.route('/')
def home():
    # The following line is selecting all the information from post and displaying at home page
    cns = Cn.query.all()
    return render_template('home.html',user_cns = cns)

@app.route('/indexpage1')
def indexpage1():
    return render_template('indexpage1.html',user_cns = cns)

@app.route('/indexpage2')
def indexpage2():
    return render_template('indexpage2.html',user_cns = cns)

@app.route('/indexpage3')
def indexpage3():
    return render_template('indexpage3.html',user_cns = cns)


@app.route('/register', methods = ['GET', 'POST'])
# GET information then 
# POST send Information
def register():
    # Init our Form - INSTANTIATING HERE
    form = UserInfoForm()
    
    #now sending form information instead of just text (i.e. names)
    if request.method == 'POST' and form.validate():
        #Get Information from the form
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # print the data to the server that comes form the form 
        print(username,email,password)

        # Creation/Init of our User Class (aka Model)  -- INSTANTIATING HERE
        user = User(username,email,password)

        # Open a connection to the database
        db.session.add(user)

        # Commit all data to the database
        db.session.commit()

    return render_template('register.html', user_form = form)
     
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        # Saving the logged in user to a variable
        logged_user = User.query.filter(User.email == email).first()
        #check the password of the newly found user
        #and validate the password against the hash value
        #inside of the database
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            # TODO Redirected user
            return redirect(url_for('home'))
        else:
            # TODO Redirect User to login route
            return redirect(url_for('login'))
    return render_template('login.html', login_form = form)

# Creation of logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Creation of cns route
@app.route('/cns', methods = ['GET','POST'])
@login_required
def cns():
    form = CnForm()
    if request.method == 'POST' and form.validate():
        title = form.title.data
        client = form.client.data
        content = form.content.data
        user_id = current_user.id
        cn = Cn(title,client,content,user_id)
        
        db.session.add(cn)

        db.session.commit()
        return redirect(url_for('home'))
    return render_template('cns.html', cn_form = form)

# post detail route to display info about a post
@app.route('/cns/<int:cn_id>')
@login_required
def cn_detail(cn_id):
    cn = Cn.query.get_or_404(cn_id)
    return render_template('cn_detail.html', cn = cn)

@app.route('/cns/update/<int:cn_id>',methods = ['GET','POST'])
@login_required
def cn_update(cn_id):
    # get the link (using link:post_id) check the form, once its validated, commit changes, return redirct to home to see changes
    cn = Cn.query.get_or_404(cn_id)
    form = CnForm()

    if request.method == 'POST' and form.validate():
        title = form.title.data
        client = form.client.data
        content = form.content.data
        user_id = current_user.id

        # Update the Database with the new Info
        cn.title = title
        cn.client = client
        cn.content = content
        cn.user_id = user_id

        # Commit the changes to the database
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('cn_update.html', update_form = form)

@app.route('/cns/delete/<int:cn_id>',methods = ['GET','POST','DELETE'])
@login_required
def cn_delete(cn_id):
    cn = Cn.query.get_or_404(cn_id)
    db.session.delete(cn)
    db.session.commit()
    return redirect(url_for('home'))