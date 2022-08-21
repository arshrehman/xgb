import os
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import FileField, SubmitField, StringField, PasswordField, BooleanField
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, url_for, flash, redirect, send_file
from wtforms.validators import InputRequired, Length
import pandas as pd
import numpy as np
from datetime import datetime
from flask_login import UserMixin, login_user, login_manager, login_required, logout_user, current_user, LoginManager
from flask_bootstrap import Bootstrap
import pickle
import warnings
warnings.filterwarnings('ignore')
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
with open('pipe_xgb.pkl', 'rb') as f:
    pipe_xgb = pickle.load(f)

app = Flask(__name__)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '@fzal&(1990)'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

ALLOWED_EXTENSIONS = set(['xlsx', 'xls'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('username',validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators = [InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    highest_education = db.Column(db.String(100), nullable=False)
    subject_ = db.Column(db.String(100), nullable=False)
    renowned_institute = db.Column(db.String(100), nullable=False)
    highest_education_city_type = db.Column(db.String(100), nullable=False)
    native_city_type = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    total_no_of_years_of_experience = db.Column(db.Integer, nullable=False)
    no_of_years_of_dubai_experiece = db.Column(db.Integer, nullable=False)
    years_of_direct_sales_experience_in_banks_tp_dsas_in_dubai = db.Column(db.Integer, nullable=False)
    how_much_direct_sales_experience = db.Column(db.Integer, nullable=False)
    manager_asst_manager = db.Column(db.String(100), nullable=False)
    sales_achievements = db.Column(db.String(100), nullable=False)
    employers_in_home_country_type = db.Column(db.String(100), nullable=False)
    last_employer_location = db.Column(db.String(100), nullable=False)
    marital_status = db.Column(db.String(100), nullable=False)
    religion = db.Column(db.String(100), nullable=False)
    currently_pursuing_any_education = db.Column(db.String(100), nullable=False)
    stability = db.Column(db.Integer, nullable=False)

class MainData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    highest_education = db.Column(db.String(100), nullable=False)
    subject_ = db.Column(db.String(100), nullable=False)
    renowned_institute = db.Column(db.String(100), nullable=False)
    highest_education_city_type = db.Column(db.String(100), nullable=False)
    native_city_type = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    total_no_of_years_of_experience = db.Column(db.Float, nullable=False)
    no_of_years_of_dubai_experiece = db.Column(db.Float, nullable=False)
    years_of_direct_sales_experience_in_banks_tp_dsas_in_dubai = db.Column(db.Integer, nullable=False)
    how_much_direct_sales_experience = db.Column(db.Float, nullable=False)
    manager_asst_manager = db.Column(db.String(100), nullable=False)
    sales_achievements = db.Column(db.String(100), nullable=False)
    employers_in_home_country_type = db.Column(db.String(100), nullable=False)
    last_employer_location = db.Column(db.String(100), nullable=False)
    marital_status = db.Column(db.String(100), nullable=False)
    religion = db.Column(db.String(100), nullable=False)
    currently_pursuing_any_education = db.Column(db.String(100), nullable=False)
    stability = db.Column(db.Float, nullable=False)

class RawData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    name = db.Column(db.String(100), nullable=False, )
    gender = db.Column(db.String(100), nullable=False)
    highest_education = db.Column(db.String(100), nullable=False)
    subject_ = db.Column(db.String(100), nullable=False)
    renowned_institute = db.Column(db.String(100), nullable=False)
    highest_education_city_type = db.Column(db.String(100), nullable=False)
    native_city_type = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    total_no_of_years_of_experience = db.Column(db.Float, nullable=False)
    no_of_years_of_dubai_experiece = db.Column(db.Float, nullable=False)
    years_of_direct_sales_experience_in_banks_tp_dsas_in_dubai = db.Column(db.Integer, nullable=False)
    how_much_direct_sales_experience = db.Column(db.Float, nullable=False)
    manager_asst_manager = db.Column(db.String(100), nullable=False)
    sales_achievements = db.Column(db.String(100), nullable=False)
    employers_in_home_country_type = db.Column(db.String(100), nullable=False)
    last_employer_location = db.Column(db.String(100), nullable=False)
    marital_status = db.Column(db.String(100), nullable=False)
    religion = db.Column(db.String(100), nullable=False)
    currently_pursuing_any_education = db.Column(db.String(100), nullable=False)
    stability = db.Column(db.Float, nullable=False)
    decision = db.relationship('Decision', backref='raw_data', lazy='select', uselist=False)

class Predictions(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key = True)
    prediction_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(200), nullable=False)
    decision_function = db.Column(db.Integer, nullable=False)

class Decision(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key = True)
    prediction_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(200), nullable=False)
    decision_function = db.Column(db.Float, nullable=False)
    raw_data_id = db.Column(db.Integer, db.ForeignKey('raw_data.id'))

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        g = generate_password_hash(user.password,method='pbkdf2:sha1', salt_length=8)
        if user:
            if check_password_hash(g, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('upload'))
        return '<h1>Invalid username or password</h1>'
    return render_template('login.html', form=form)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        if file and allowed_file(file.filename):
            data = pd.read_excel(file)
            lst = list(data.columns)
            lst = [x.lower().strip() for x in lst]
            data.columns = lst
            data2 = data.copy()
            data2.dropna(how='any',inplace=True)
            feature_list = ['name', 'gender', 'highest_education', 'subject_', 'renowned_institute?',
                            'highest_education_city_type',
                            'native_city_type', 'nationality', 'total_no._of_years_of_experience',
                            'no._of_years_of_dubai_experiece',
                            'years_of_direct_sales_experience_in_banks/_tp_dsas_in_dubai',
                            'how_much_direct_sales_experience',
                            'manager/_asst._manager?', 'sales_achievements', 'employers_in_home_country_type',
                            'last_employer_location_(uae/outside)',
                            'marital_status', 'religion', 'currently_pursuing_any_education?', 'stability']
            count = 0
            inv_feature = []
            for item in list(data2.columns):
                if item.lower().strip() in feature_list:
                    count += 1
                else:
                    inv_feature.append(item)

            if count == 20:
                data2.rename(columns={'renowned_institute?':'renowned_institute',
                                     'total_no._of_years_of_experience':'total_no_of_years_of_experience',
                                     'no._of_years_of_dubai_experiece':'no_of_years_of_dubai_experiece',
                                     'years_of_direct_sales_experience_in_banks/_tp_dsas_in_dubai':'years_of_direct_sales_experience_in_banks_tp_dsas_in_dubai',
                                     'manager/_asst._manager?':'manager_asst_manager',
                                     'last_employer_location_(uae/outside)':'last_employer_location',
                                     'currently_pursuing_any_education?':'currently_pursuing_any_education'}, inplace=True)
                data2['total_no_of_years_of_experience'] =data2['total_no_of_years_of_experience'].astype(float)
                data2['no_of_years_of_dubai_experiece']=data2['no_of_years_of_dubai_experiece'].astype(float)
                data2['years_of_direct_sales_experience_in_banks_tp_dsas_in_dubai'] = data2['years_of_direct_sales_experience_in_banks_tp_dsas_in_dubai'].astype(float)
                data2['how_much_direct_sales_experience']=data2['how_much_direct_sales_experience'].astype(float)
                data2['stability']=data2['stability'].astype(float)
                for col in data.columns:
                    if isinstance(data[col][0], str):
                        data[col] = data[col].str.strip().str.upper()
                g_c = ['MALE', 'FEMALE']
                h_ec = ['BACHELORS','BACHELORS (FAV.)', 'CLASS X', 'CLASS XII', 'DIPLOMA', 'MASTERS', 'MBA']
                m_c = ['UNMARRIED', 'MARRIED']
                s_c = ['ARTS','BUSINESS','COMMERCE', 'COMPUTER SCIENCE', 'ENGINEERING', 'HOSPITALITY', 'OTHER','SCIENCE']
                r_c = ['ISLAM', 'HINDU', 'CHRISTIAN','NOT DECLARED']
                n_c = ['INDIA', 'PAKISTANI', 'FILIPINO', 'OTHER']
                eh_c = ['NON SALES NON BANKING', 'SALES NON BANKING', 'SALES BANKING', 'NON SALES BANKING']
                c_c = ['METRO', 'TIER3', 'TIER2']

                for i in range(len(data2)):
                    raw_data = RawData(name=data.iloc[i, 0], gender=data.iloc[i, 1], highest_education=data.iloc[i,2], subject_=data.iloc[1,3],
                                    renowned_institute=data.iloc[i,4], highest_education_city_type=data.iloc[i,5],
                                    native_city_type=data.iloc[i,6], nationality=data.iloc[i,7], total_no_of_years_of_experience=data.iloc[i,8],
                                    no_of_years_of_dubai_experiece=data.iloc[i,9], years_of_direct_sales_experience_in_banks_tp_dsas_in_dubai=data.iloc[i,10],
                                    how_much_direct_sales_experience=data.iloc[i,11], manager_asst_manager=data.iloc[i,12], sales_achievements=data.iloc[i,13],
                                    employers_in_home_country_type=data.iloc[i,14], last_employer_location=data.iloc[i,15],
                                    marital_status=data.iloc[i,16],religion=data.iloc[i,17], currently_pursuing_any_education=data.iloc[i,18],
                                    stability=data.iloc[i,19])
                    db.session.add(raw_data)
                    db.session.commit()
                X = data.drop('name', axis=1)
                y = pipe_xgb.predict_proba(X)[:,1]
                global df
                df= pd.DataFrame({"Name":data['name'], "Decision_Function":pd.Series(y)})
                for i in range(len(df)):
                    decision = Decision(name = df.iloc[i,0], decision_function=df.iloc[i,1])
                    raw_data.decision=decision
                    db.session.add(decision)
                    db.session.commit()
                return render_template("ExcelFile.html", data=df.to_html(index=False))

            else:
                flash('These feature name is not as per the feature name model knows {}'.format(inv_feature), 'error')

        else:
            flash('You can only upload xlsx or xls file', 'error')
    return render_template('upload.html', form=form)

@app.route('/return-files/')
@login_required
def return_files_tut():
    try:
        df2 = df.to_excel('static/filesXGB_predictions.xlsx')
        return send_file('static/filesXGB_predictions.xlsx', download_name='Xgb_predictions.xlsx')
    except Exception as e:
        return str(e)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)