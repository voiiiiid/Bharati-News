from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
SECRET_KEY = os.urandom(32)


app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:void@localhost/bharati_db'

db = SQLAlchemy(app)

# models--------------------------------------------------------------------------
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    headline = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Define Form for Adding News
class AddNewsForm(FlaskForm):
    category = SelectField('Category', choices=[('politics', 'Politics'), ('technology', 'Technology'), ('sports', 'Sports'), ('entertainment', 'Entertainment'), ('business', 'Business'), ('health', 'Health')], validators=[DataRequired()])
    headline = StringField('Headline', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Image', validators=[DataRequired()])
    submit = SubmitField('Add News')

app.app_context().push()
db.create_all()


# routes------------------------------------------------

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/read_news')
def read_news():
    news = News.query.all()
    return render_template('read_news.html', news=news)

@app.route('/read_news/<category>')
def news_by_category(category):
    news_data = News.query.filter_by(category=category).all()
    return render_template('read_news.html', news=news_data)

@app.route('/premium')
def buy_premium():
    return render_template('premium.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    form = AddNewsForm()

    if form.validate_on_submit():
        category = form.category.data
        headline = form.headline.data
        description = form.description.data

        # Save the image file (simplified; you may want to handle this better)
        image = form.image.data
        image_url = f'static/{image.filename}'
        image.save(f'./static/{image.filename}')

        # Create a new news instance and add it to the database
        new_news = News(category=category, headline=headline, description=description, image_url=image_url)
        db.session.add(new_news)
        db.session.commit()

        flash('News added successfully!', 'success')
        return redirect(url_for('add_news'))

    return render_template('add_news.html', form=form)


if __name__ == '__main__':
    app.debug = True
    app.run()