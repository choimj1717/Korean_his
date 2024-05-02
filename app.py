from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///korean_history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(100), unique=True, nullable=False)
    definition = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Word('{self.term}', '{self.definition}')"

@app.route('/')
def index():
    with app.app_context():
        return render_template('index.html')

@app.route('/add_word', methods=['POST'])
def add_word():
    with app.app_context():
        term = request.form['term']
        definition = request.form['definition']
        word = Word(term=term, definition=definition)
        db.session.add(word)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    with app.app_context():
        term = request.form['term']
        word = Word.query.filter_by(term=term).first()
        if word:
            return render_template('search.html', word=word)
        else:
            return render_template('search.html', word=None)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run('0.0.0.0', port=80, debug=True)
