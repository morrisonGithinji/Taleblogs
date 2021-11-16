from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from  ..models import User,Post, Comment,Quotes
from .. import db,photos
from . forms import UpdateProfile, CommentForm, PostForm
from ..request import  get_quotes
from werkzeug.contrib.atom import AtomFeed
from urllib.parse import urljoin

def get_abs_url(url):
    """ Returns absolute url by joining post url with base url """
    return urljoin(request.url_root, url)

@main.route('/')
def index():
  
  return render_template('index.html')

@main.route('/user/<username>')
def profile(username):
  user = User.query.filter_by(username=username).first()
  
  if user is None:
    abort(404)
    
  return render_template("profile/profile.html", user = user)  

@main.route('/user/<username>/update',methods = ['GET','POST'])
@login_required 
def update_profile(username):
  user = User.query.filter_by(username=username).first()
  
  if user is None:
    abort(404)
    
  form = UpdateProfile()
  
  if form.validate_on_submit():
    user.bio=form.bio.data
    user.gender=form.gender.data
    
    db.session.add(user)
    db.session.commit()
    
    return redirect(url_for('.profile',username=user.username))
  return render_template('profile/update.html',form=form)

@main.route('/user/<username>/update/pic',methods=['POST'])
@login_required
def update_pic(username):
  user = User.query.filter_by(username=username).first()
  if 'photo' in request.files:
    filename = photos.save(request.files['photo'])
    path =f'photos/{filename}'
    user.profile_pic_path = path
    db.session.commit()
  return redirect(url_for('main.profile', username=username))  
    
    
@main.route('/blogs/new_post', methods=['GET','POST'])
@login_required
def new_post():
  form = PostForm()
  if form.validate_on_submit():
    title = form.title.data
    post=form.post.data
    
    
    new_post=Post(title=title,post=post, author=current_user.id)
    
    new_post.save_post()
    return redirect(url_for('.all_posts'))
  
  
  return render_template('new_blog.html',post_form=form, legend='New_Post' )

@main.route('/blogs')
def all_posts():
  posts = Post.query.all()
  user = current_user
  user = User.query.filter_by(username='username').first()
  quote = get_quotes()
  
  return render_template('blog.html', posts=posts,user=user,quote = quote)

@main.route('/blogs/comment/<int:post_id>',methods = ['GET','POST'])
@login_required
def new_comment(post_id):
    form = CommentForm()
    comments = Comment.get_comments(post_id)
    
    if form.validate_on_submit():
        comment = form.comment.data
        post_id = post_id
        new_comment = Comment(comment = comment, post_id=post_id)
        
        
        new_comment.save_comment()
        return redirect(url_for('.index',form =form,post_id =post_id))
      
      
    
    return render_template('comments.html', comment_form =form, comments = comments, post_id =post_id)



@main.route('/blog/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_post(post_id):
  posts = Post.query.all()
  post = Post.query.get(post_id)
  quote = get_quotes()
  if post.author != current_user.id:
    abort(403)
    
  form = PostForm()
  if form.validate_on_submit():
    post.title = form.title.data
    post.post=form.post.data
    db.session.commit()
    
    return redirect(url_for('.all_posts',id=post.id))
  if request.method == 'GET':
    form.title.data = post.title
    form.post.data = post.post
      
  return render_template('new_blog.html',post_form=form,posts=posts,quote=quote, legend = 'Post Update')    
        

@main.route('/blogs/<int:post_id>/delete')
@login_required 
def delete_blog(post_id):
  posts = Post.query.all() 
  single_post = Post.query.get(post_id)
  quote = get_quotes()
  if single_post.author != current_user.id:
    abort(403)
  
  db.session.delete(single_post)
  db.session.commit()
  return redirect(url_for('.all_posts',posts=posts,quote=quote,))

@main.route('/blogs/<int:comment_id>/delete', methods =['POST'])
@login_required 
def delete_comment(comment_id):

  posts = Post.query.all() 
  
  all_comments = Comment.query.all()
  single_comment = Comment.query.get(comment_id)
  
  # if single_comment.input != current_user.id:
  #   abort(403)
    
  
  db.session.delete(single_comment)
  db.session.commit()
  return redirect(url_for('.all_posts', all_comments=all_comments, single_comment =single_comment, posts=posts))


@main.route('/subscribe')
@login_required
def subscribe():
  
  return render_template('subscribe.html')
     
@main.route('/feeds')
def feeds():
    feed = AtomFeed(title='Latest Posts from My Blog',
                    feed_url=request.url, url=request.url_root)
    # Sort post by created date
    blogs = Post.query.all()
    for post in blogs:
        feed.add(post.title, post.posted,
                 content_type='html',
                 id = post.id,
                 author= post.user.username,
                 published=post.posted,
                 updated=post.posted)
    return feed.get_response()  
  