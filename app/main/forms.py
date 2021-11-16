from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField, validators
from wtforms.validators import Required
from ..models import Post, Comment

class  PostForm(FlaskForm):
  title = StringField('Blog title', validators=[Required()])
  post = TextAreaField('Blog')
  submit = SubmitField('Post')
  
class CommentForm(FlaskForm):
  comment = TextAreaField('Leave a comment', validators=[Required()])
  submit = SubmitField('Add')
  
class UpdateProfile(FlaskForm):
  gender = SelectField('Gender', choices=[('Male','Male'),('Female','Female')])
  bio = TextAreaField('Tell us more about yourself', validators=[Required()])
  submit = SubmitField('Submit')
