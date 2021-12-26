from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import linked_list
import binary_search_tree
import random
import custom_q
import stack

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# configure sqlite3 to enforce foreign key constaints.. This is the reason why we need to import sqlalchemy (for the event)
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        
db = SQLAlchemy(app)
now = datetime.now()

# models
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    # create cascade so delete all table when linked
    posts = db.relationship("BlogPost", cascade="all, delete")
    
class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date  = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
# routes
@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(
        name = data["name"],
        email = data["email"],
        address = data["address"],
        phone = data["phone"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created!"}), 200

@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()
    
    for user in users:
        all_users_ll.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "address": user.address,
                "phone": user.phone,
                "email": user.email
            }
        )
    
    return jsonify(all_users_ll.to_list()), 200

@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()
    
    for user in users:
        all_users_ll.insert_at_end(
            {
                "id": user.id,
                "name": user.name,
                "address": user.address,
                "phone": user.phone,
                "email": user.email
            }
        )
    
    return jsonify(all_users_ll.to_list()), 200

@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    user = User.query.filter_by(id=user_id).first()
        
    return jsonify({"id": user.id,
                "name": user.name,
                "address": user.address,
                "phone": user.phone,
                "email": user.email} if user else {}), 200

@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({}), 200

@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User does not exist!"}), 400
    
    data = request.get_json()
    blog_post = BlogPost(
        title = data["title"],
        body = data["body"],
        user_id = user_id,
        date = datetime.now()
    )
    db.session.add(blog_post)
    db.session.commit()
    
    return jsonify({"message": "BlogPost created!"}), 200  

@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    blog_posts = BlogPost.query.all()
    random.shuffle(blog_posts)
    
    bst = binary_search_tree.BinarySearchTree()
    
    for post in blog_posts:
        bst.insert({
            "id": post.id,
            "title": post.title,
            "body" : post.body,
            "user_id": post.user_id
        })
    
    post = bst.search(blog_post_id)
    return jsonify(post if post else {"message": "Message does not exist!"}), 200

@app.route("/blog_post/<blog_post_id>", methods=["DELETE"])
def delete_blog_post(blog_post_id):
    blog_post = BlogPost.query.filter_by(id=blog_post_id).first()
    
    if blog_post:
        db.session.delete(blog_post)
        db.session.commit()
        
    return jsonify({}), 200

@app.route("/blog_post/numeric_body", methods=["GET"])
def get_numeric_post_bodies():
    blog_posts = BlogPost.query.all()
    
    q = custom_q.Queue()
    
    for post in blog_posts:
        q.enqueue(post)
        
    return_list = []
    
    for _ in range(len(blog_posts)):
        post = q.dequeue()
        numeric_body = 0
        for i in post.data.body:
            numeric_body += ord(i)
            
        post.data.body = numeric_body
        
        return_list.append({
            "id": post.data.id,
            "title": post.data.title,
            "body": post.data.body,
            "user_id": post.data.user_id
        })
    
    return jsonify(return_list), 200

@app.route("/blog_post/delete_last_10", methods=["DELETE"])
def delete_last_10():
    blog_posts = BlogPost.query.all()
    
    s = stack.Stack()
    
    for post in blog_posts:
        s.push(post)
    
    for i in range(10):
        popped = s.pop()
        if popped:
            db.session.delete(popped.data)
            db.session.commit()
        
    return jsonify({}), 200


if __name__ == "__main__":
    app.run(debug=True)