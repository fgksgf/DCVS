from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class JDForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired()])
    captcha = StringField('CAPTCHA', validators=[DataRequired()])
    submit = SubmitField('开始爬取')
