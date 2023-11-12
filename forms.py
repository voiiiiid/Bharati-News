from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Length

class AddNewsForm(FlaskForm):
    category = SelectField('Category', choices=[('politics', 'Politics'), ('technology', 'Technology'), ('sports', 'Sports'), ('entertainment', 'Entertainment'), ('business', 'Business'), ('health', 'Health')], validators=[DataRequired()])
    headline = StringField('Headline', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Image', validators=[DataRequired()])
    submit = SubmitField('Add News')
