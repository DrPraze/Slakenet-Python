# Import some stuff needed
from flask import Flask, jsonify, request, send_from_directory, render_template, session, url_for, redirect
from flask_cors import CORS
import os
from settings import Config
# Import some already handled routes in for userbase
from routes import initialize_website_routes, initialize_error_handlers
# Use waitress to serve flask app
from waitress import serve
# import stripe
# from africastalking.AfricasTalkingGateway import AfricasTalkingGateway

app = Flask(__name__)
CORS(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Africastalking is used to communcaite with an API Called Africa's Talking
# It is an API for crediting phone numbers with airtime
# Username for using Africa'sTalkingGateway
username = "Slakenet"
# Africa's talking api key
apikey = "some-api-key"
# AFrica's talking slakenet sandbox
sandbox = "optional-sandbox"

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

@app.route('/buy.html', methods = ['GET'])
def buy_data():
    return send_from_directory('', 'buy.html')

@app.route('/policy.html', methods = ['GET'])
def policy():
	return send_from_directory('', 'policy.html')

# communicatqe with africa's talking api by collecting the phone number
# and amount params, parse it and credit the number
@app.route('/buy_airtime/<number>/<amount>', methods = ['GET', 'POST'])
def buy_airtime():
	# Specify an array of dicts to hold the recipients and the amount to send
	recipients = [{"phoneNumber" : f"{number}", 
			   "amount"      : f"NGN {amount}"}]
	# Create a new instance of our awesome gateway class
	gateway = AfricasTalkingGateway(username, apikey)
	try:
		# That's it, hit send and we'll take care of the rest. 
		responses = gateway.sendAirtime(recipients)
		for response in responses:
			print ("phoneNumber=%s; amount=%s; status=%s; discount=%s; requestId=%s" %(response['phoneNumber'],
				response['amount'],
				response['status'],
				response['discount'],
				response['requestId']))
	except AfricasTalkingGatewayException as e:
		print ('Encountered an error while sending airtime: %s' % str(e))
	# We specify the recipients as a List of Dictionary objects; 
	# recipients = [{"phoneNumber" : "+2547XXYYYZZZ", 
	# 			"amount"      : "KES XX"}]
	recipients = [{"phoneNumber" : f"{number}",
	"amount" : f"NGN {amount}"}]
	return recipients

# app route to referring to where users can take the surveys
@app.route('/survey/<survey_name>', methods = ['GET', 'POST'])
def survey(survey_name):
	return send_from_directory('data', f'{survey_name}.html')

if __name__=='__main__':
	app.run(debug = True)