#from flask import Flask,render_template
from flask import Flask, render_template, session, redirect, url_for
#from flask.ext.wtf import Form
#from flask.ext.bootstrap import Bootstrap
from flask_wtf import Form
import flask_def2
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField
from wtforms.validators import Required
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'



class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('hello2',fillname=session['name']))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/hello2?fillname=<fillname>')
def hello2(fillname):
    name = fillname
    app_id = int(fillname)
    score=flask_def2.get_score(app_id)
    return render_template('index2.html', name=fillname,score0 = score[0],score1 = score[1],score2 = score[2],score3 = score[3],score4 = score[4])

if __name__ == '__main__':
    app.run(debug=True)

