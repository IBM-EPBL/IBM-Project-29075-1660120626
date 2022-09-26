 from flask import Flask, render_template
 
 app = Flask(__name__)
 
 
 @app.route("/")
 def index():
     return render_template('home.html')
 
 
 @app.route("/blog")
 def blog():
     return render_template('blog.html')
 
 @app.route("/about")
 def about():
     return render_template('about.html')
 
 @app.route("/signup")
 def signup():
     return render_template('signup.html')
 
 @app.route("/signin")
 def signin():
     return render_template("signin.html")

 
 # @app.route("/blog/<id>")
 # def blog_id(id):
 #     return f"id : {id}"
 
 # @app.route("/profiles/<username>")
 # def profiles(username):
