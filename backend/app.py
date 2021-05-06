#Import the flask module
from flask import Flask, redirect, url_for, request, render_template

#Create a Flask constructor. It takes name of the current module as the argument
app = Flask(__name__)

#Create a route decorator to tell the application, which URL should be called for the #described function and define the function

@app.route('/')
#def index():
#   return render_template(‘hello.html’)

def tutorialspoint():
    return "Test for Flowa"

@app.route('/oslo_map')
def oslo_map():
    return "here we will put the html map built earlier"
#app.add_url_rule('/', 'oslo_map', oslo_map)

@app.route('/admin')
def hello_admin():
   return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      return redirect(url_for('hello_admin'))
   else:
      return redirect(url_for('hello_guest',guest = name))


@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name


"""
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))
"""
@app.route('/login',methods = ['POST', 'GET'])
def login():
   return render_template("login.html")

@app.route("/<usr>")
def user(usr):
   return f"<h1>{usr}</h1>"

#Create the main driver function
if __name__ == '__main__':
#call the run method
    app.run(debug = True)