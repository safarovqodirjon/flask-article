from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///any.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    intro = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Articles %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    articles = Articles.query.order_by(Articles.date.desc()).all()
    return render_template('index.html', articles=articles)



@app.route('/create_article', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Articles(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "Something went wrong!"
    else:
        return render_template('create_article.html')


@app.route('/article/<int:id>')
def article(id):
    my_article = Articles.query.get(id)
    return render_template('article.html', my_article=my_article)


@app.route('/delete/<int:id>')
def delete(id):
    my_data = Articles.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    return redirect('/')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    my_data = Articles.query.get(id)

    if request.method == 'POST':
        my_data.title = request.form['title']
        my_data.intro = request.form['intro']
        my_data.text = request.form['text']
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "Something went wrong!"
    else:
        return render_template('edit.html', my_data=my_data)


if __name__ == '__main__':
    app.run(debug=True)
