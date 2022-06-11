# Import some stuff needed
from flask import (Flask, jsonify, request, send_from_directory,
	render_template, session, url_for, redirect, flash)
from flask_cors import CORS
import os, i18n, requests, uuid
from settings import Config
# Import some already handled routes in for userbase
from routes import initialize_website_routes, initialize_error_handlers
# Use waitress to serve flask app
from waitress import serve
from middleware import (load_user_balance, update_user_balance,
	verify_email, get_reset_token, verify_reset_token)
from dataservice import DataService
# from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_mail import Message, Mail

# from flask_login import login_required
 
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
# MAIL_USERNAME = os.getenv('MAIL_USERNAME')
# MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_USERNAME = "slakenetofficial@gmail.com"
MAIL_PASSWORD = "Slakee404!"

app = Flask(__name__)
CORS(app)

mail = Mail()
mail.init_app(app)
# SECRET_KEY = os.urandom(32)
SECRET_KEY = str(uuid.uuid4())
# SECRET_KEY = "Slakee404!"
app.config['SECRET_KEY'] = SECRET_KEY

# No sand box available for VTU.ng
# sandbox = "optional-sandbox"

DATA_SERVICE = DataService()

# initialize pre-defined routes from routes.py
initialize_website_routes(app)
# initialize pre-defined error handlers from routes.py
initialize_error_handlers(app)

# main route for the index page
@app.route('/', methods=['GET'])
def index():
	return send_from_directory('','index.html')

# route for about section and it goes on
@app.route('/about.html', methods=['GET'])
def about():
	return send_from_directory('', 'about.html')

@app.route('/policy.html', methods = ['GET'])
def policy():
	return send_from_directory('', 'policy.html')

# buy airtime with VTU.ng's API
@app.route('/buy_airtime/<network>/<number>/<amount>', methods=['GET'])
def buy_airtime(network, number, amount):
	account_balance = load_user_balance()
	if int(account_balance) > int(amount):
		r = requests.get("https://vtu.ng/wp-json/api/v1/airtime?username=slakenet&password=Slakee404!&phone="+number+"&network_id="+network+"&amount="+amount)
		if r["code"] == "success":
			account_balance = int(account_balance)-amount
			flash(i18n.t("wallet.topup_successful"))
			return redirect(url_for("page_dashboard"))
		elif r["code"] == "failure":
			flash(i18n.t(r["message"]))
		else:
			flash(i18n.t("Something shele, but we no know wetin sup"))
	else:
		flash(i18n.t("Failed to load TopUp due to insufficient balance"))
		return redirect(url_for("page_dashboard"))

# app route to referring to where users can take the surveys
@app.route('/survey/<survey_name>', methods = ['GET', 'POST'])
def survey(survey_name):
	return send_from_directory('data', f'{survey_name}.html')

# app route to remove taken surveys from a user's list
@app.route('/done/<taken_survey>')
def update_survey(taken_survey):
	user_email = session['email']
	f = open('data/done.txt', 'r')
	data_dict = eval(f.read())
	survey_list = data_dict[user_email]
	survey_list.append(taken_survey)
	data_dict[user_email] = survey_list
	f.close()
	f = open('data/done.txt', 'w')
	f.truncate()
	f.write(str(data_dict))
	flash(i18n.t("Survey completed!"))
	return redirect(url_for("page_dashboard"))

# app route for an admin to topup the account of a user
@app.route('/deposit/<email>/<admin_password>/<amount>')
def deposit(email, admin_password, amount):
	if admin_password=="Slakee404!":
		try:
			return update_user_balance(email, amount)
		except Exception as e:
			return "email doesn't exist in database"
	else:
		return jsonify("Incorrect password")

# app route for admins to upload surveys
# In future, survey owners would be able to upload their surveys
@app.route('/upload_survey/<password>/<survey_name>/<description>/<html>')
def upload_survey(password, survey_name, description, html):
	# Would check if survey already exists, if not, create one with the params
	if password == "Slakee404!":
		if os.path.isfile(f"data/{survey_name}.txt"):
			with open(f"data/{survey_name}.txt", "w") as f:
				f.write(f"{description}")
				f.close()
			with open(f"data/{survey_name}.html", "w") as f:
				f.write(f"{html}")
				f.close()
			s = open("data/surveys.txt")
			s = eval(s.read())
			s.append(survey_name)
			with open("data/surveys.txt") as f:
				f.truncate()
				f.write(str(s))
				f.close()
			return jsonify("Successfully added survey")
		else:
			return jsonify("The name of the survey already exists.")
	else:
		return jsonify("The password is Incorrect. Don't try again")

# app route for admins to delete surveys from the general database
# This should be done when the owner of the survey has gotten the complete
# survey responses, in future versions of this code, this would be done 
# automatically by counting the number of slakenet users that take the survey
# and thee initial number of survey responses the owner paid for
# do some if else statements and do the stuff
@app.route('/delete_survey/<password>/<survey_name>')
def delete_survey(survey_name):
	if password == "Slakee404!":
		if os.path.isfile(f"data/{survey_name}.txt"):
			with open(f"data/{survey_name}.txt") as textfile:
				os.remove(textfile)
			with open(f"data/{survey_name}.html") as htmlfile:
				os.remove(htmlfile)
			s = open("data/surveys.txt")
			s = eval(s.read())
			s.pop(s.index(survey_name))
			with open("data/surveys.txt") as f:
				f.truncate()
				f.write(str(s))
				f.close()
			return jsonify("Successfully deleted survey")
		else:
			return jsonify("Couldn't delete survey, the survey doesn't exist")
	else:
		return jsonify("Couldn't delete survey, password was Incorrect")


# This is the section we're working on now
@app.route('/password_reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'GET':
        return render_template('reset.html')
    if request.method == 'POST':
        email = request.form.get('email')
        user = verify_email(email)
        flash(i18n.t(user))
        if user:
        	token = get_reset_token(email)
        	print(token)
        	msg = Message()
        	msg.subject = "Slakenet Password Reset"
        	msg.sender = "slakenetofficial@gmail.com"
        	msg.recipients = [email]
        	msg.html = render_template('reset_email.html', user = email, token=token)
        	try:
        		mail.send(msg)
        		flash(i18n.t("Check your Successfully submitted email for the password reset"))
        	except Exception as e:
        		flash(i18n.t("We couldn't send the verification email:"+str(e)+" visit the help section to get help"))
        else:
        	flash(i18n.t("The email you entered doesn't exist"))
        return redirect(url_for("page_dashboard"))

@app.route('/reset_verified', methods=['GET', 'POST'])
def reset_verified():
    user = verify_reset_token(token)
    if not user:
        flash(i18n.t('User Email not found'))
        return redirect(url_for('page_dashboard'))

    password = request.form.get('password')
    if password:
        user.set_password(password, commit=True)
        return redirect(url_for('page_dashboard'))
    return render_template('reset_verified.html')
# End of underdeveloped section
# Requires some modifications on the jwt, I'll look into it

@app.route("/<password>/request_userdata")
def request_userdata():
	# KPI is under-developed and only returns the number of users for now
	if password == "Slakee404!":
		with open("data/emails.txt") as f:
			users = eval(f.read())
			number_of_users = len(users)
			return number_of_users
	else:
		return jsonify("Incorrect password")

if __name__=='__main__':
	app.run(debug = True)
