# Import some stuff needed
from flask import (Flask, jsonify, request, send_from_directory,
	render_template, session, url_for, redirect, flash)
from flask_cors import CORS
import os, i18n, requests
from settings import Config
# Import some already handled routes in for userbase
from routes import initialize_website_routes, initialize_error_handlers
# Use waitress to serve flask app
from waitress import serve
from middleware import load_user_balance, update_user_balance
from dataservice import DataService

app = Flask(__name__)
CORS(app)

SECRET_KEY = os.urandom(32)
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
			flash(i18n.t("Successfully loaded TopUp. Enjoy!"))
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

@app.route('/deposit/<email>/<admin_password>/<amount>')
def deposit(email, admin_password, amount):
	if admin_password=="Slakee404!":
		try:
			return update_user_balance(email, amount)
		except Exception as e:
			# return "email doesn't exist in database"
			return e
	else:
		return jsonify("Incorrect password")

@app.route('/upload_survey/<password>/<survey_name>/<description>/<html>')
def upload_survey(password, survey_name, description, html):
	# Would check if survey already exists, if not, create one with the params
	if password == "Slakee404!":
		with open(f"data/{survey_name}.txt", "w") as f:
			f.write(f"{description}")
			f.close()
		with open(f"data/{survey_name}.html", "w") as f:
			f.write(f"{html}")
			f.close()
		s = open("data/surveys.txt")
		s = eval(s.read())
		s.insert(survey_name)
		with open("data/surveys.txt") as f:
			f.truncate()
			f.write(str(s))
			f.close()
		return jsonify("Successfully added survey")
	return jsonify("Couldn't add survey, Something went wrong")

@app.route('/delete_survey/<password>/<survey_name>')
def delete_survey(survey_name):
	if password == "Slakee404!":
		with open(f"data/{survey_name}.txt") as textfile:
			os.remove(textfile)
		with open(f"data/{survey_name}.html") as htmlfile:
			os.remove(htmlfile)
		s = open("data/surves.txt")
		s = eval(s.read())
		s.pop(s.index(survey_name))
		with open("data/surveys.txt") as f:
			f.truncate()
			f.write(str(s))
			f.close()
		return jsonify("Successfully deleted survey")
	return jsonify("Couldn't delete survey, something went wrong")


if __name__=='__main__':
	app.run(debug = True)
