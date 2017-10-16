from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    body = db.Column(db.String(100000))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        
#def blog_list():
#    return Blog.query.all()

@app.route('/', methods=['GET'])
def index():
    blog_list = (reversed(Blog.query.all()))
    return render_template('blog.html', head="Blogz!", blog_list=blog_list )


@app.route('/newpost', methods=['POST', 'GET'])
def newblog():
    title = ''
    body = ''
    title_error = ''
    body_error = ''
    error = False
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title.strip() == '':
            title_error = "Try harder"
            error = True
        if body.strip() == '':
            body_error = "Try Harder"
            error = True
        if error is False:
            blog = Blog(title, body)
            db.session.add(blog)
            db.session.commit()
            blog_id = str(blog.id)    
            return redirect('/blogpost?id='+blog_id)
    
    return render_template('newpost.html', title=title, head="New Blog",
    body=body, title_error=title_error, body_error=body_error)


@app.route('/blogpost', methods=['GET'])
def blogpost():
    id = request.args['id']
    #return id
    blog = Blog.query.filter_by(id=id).first()
    #blog = db.session.query(Blog).filter(Blog.id == id).first()
    return render_template('blogpost.html', head="Blog Post!", blog=blog)

if __name__ == '__main__':
    app.run()