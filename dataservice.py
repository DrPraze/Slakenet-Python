""" Defines data layer wrapper """
import i18n
# from models import User, Expense
from models import User


# Add locales folder to translation path
i18n.load_path.append('locales')

class DataService:
	""" Provides data to the rest of the app """
	USERS = eval(open('data/emails.txt', 'r').read())
	done = eval(open('data/done.txt', 'r').read())
	def __init__(self):
		""" Initializes data service """
		pass

	def create_account(self, email, password, name, deposit=0):
		""" Adds user to data store """
		if email not in self.USERS:
			new_user = User(email, password, name, deposit)
			# self.USERS[email] = new_user
			self.USERS[email] = [email, password, name, deposit]
			with open('data/emails.txt', 'w') as f:
				f.truncate()
				f.write(str(self.USERS))
			self.done[email] = []
			with open('data/done.txt', 'w') as f:
				f.truncate()
				f.write(str(self.done))
			return str(new_user.id)
			# return True
		else:
			return False

	def login(self, email, password):
		""" Authenticates user """
		if email in self.USERS:
			user = self.USERS[email]
			# if user.check_password(password):
			if user[1] == password:
				# return user
				return [True, user[2]]
		# return None
		return [False]

	def load_user_balance(self, email):
		""" Gets user account balance """
		if email in self.USERS:
			# return self.USERS[email].get_balance()
			return self.USERS[email][3]

		return i18n.t('wallet.wallet_not_found')

	def get_account_details(self, email):
		""" Gets user account details """
		if email in self.USERS:
			return self.USERS[email]

	def update_balance(self, email, amount):
		if email in self.USERS:
			self.USERS[email][3] = int(self.USERS[email][3])+int(amount)
			with open('data/emails.txt', 'w') as f:
				f.truncate()
				f.write(str(self.USERS))
			self.USERS = eval(open('data/emails.txt', 'r').read())
			return self.USERS[email][3] 

	def topup_account(self, email, amount):
		""" Tops up user account with specified amount """
		if email in self.USERS:
			if self.USERS[email].topup(amount):
				return i18n.t('wallet.topup_successful')

			return i18n.t('wallet.topup_unsuccessful')
