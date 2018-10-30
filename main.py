from flask import Flask, request, redirect, render_template, session, flash

from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:endofchapter2@localhost:8889/blogz'

app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

app.secret_key = 'y337kGcys&zP3B'







class Blog(db.Model):



    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(120))

    body = db.Column(db.String(120))

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))



    def __init__(self, title,body,owner):

        self.title = title

        self.body = body

        self.owner_id = owner



class User(db.Model):



    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(120), unique=True)

    password = db.Column(db.String(120))

    blogs = db.relationship('Blog', backref='owner')



    def __init__(self, username, password):

        self.username = username

        self.password = password





allowed_routes = ['login','signup','blog','index','logout']



@app.before_request

def require_login():

    #allowed_routes = ['login','signup','blog','index','logout']

    #if request.endpoint not in allowed_routes and 'username' not in session:

    if not ('username' in session or request.endpoint in allowed_routes):

        return redirect('/login')  



@app.route('/login', methods=['POST', 'GET'])

def login():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:

            session['username'] = username

            flash("Logged in")

            return render_template('newpost.html',title="Blogz!")

        else:

            flash('User password incorrect, or user does not exist')



    return render_template('login.html')



#Start of Signup

@app.route('/signup', methods=['POST', 'GET'])

def signup():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        verify = request.form['verify']

    

        #empty entry validation

        #if len(username) == 0 or len(password) == 0:

            #flash('Entries are invalid!')

    

        #Username validation

        if len(username) < 3:

            flash("Invalid User Name!")

                   

        #Password validation

        elif len(password) < 3:

            flash("Invalid Password!")

           

        #Password verification

        elif  password != verify:

            flash('Password not matching!')

             

        else:

            existing_user = User.query.filter_by(username=username).first()

            if not existing_user:

                new_user = User(username, password)

                db.session.add(new_user)

                db.session.commit()

                session['username'] = username

                # return render_template('newpost.html',title="Blogz!")
                return redirect('/newpost')
            else:

                flash('Username already exists!')

            

    return render_template('signup.html',title="Blogz!")



@app.route('/logout')

def logout():

    if 'username' in session['username']:

        del session['username']

    return redirect('/')           



@app.route('/newpost', methods=['POST', 'GET'])

def newpost():

    

    if request.method == 'POST':

        title = request.form['blog']

        body = request.form['body']

        owner = User.query.filter_by(username=session['username']).first()



        if len(title) == 0 or len(body) == 0:

            flash("Entry can't be empty")

        else:

            new_blog = Blog(title,body,owner.id)

            #new_blog = Blog(title,body)

            db.session.add(new_blog)

            db.session.commit()

            return render_template('ind_blog.html',title="Blogz!", 

            blog=new_blog)

                

    return render_template('newpost.html',title="Blogz!")

  



@app.route('/blog', methods=['POST', 'GET'])

def blog():



    if (request.args.get('id')):

        x = int(request.args.get('id'))

        blog = Blog.query.get(x)

        return render_template('ind_blog.html',title="Blogz!", 

        blog=blog)

    elif (request.args.get('user')):

        y = int(request.args.get('user'))

        blogs = Blog.query.filter_by(owner_id=y).all()

        return render_template('blog.html',title="Blogz!", 

        blogs=blogs)

    else:

        blogs = Blog.query.all()

        return render_template('blog.html',title="Blogz!", 

        blogs=blogs)





@app.route('/', methods=['POST', 'GET'])

def index():

    users = User.query.all()

    return render_template('index.html',title="Blogz!",users=users)



 



if __name__ == '__main__':

    app.run()