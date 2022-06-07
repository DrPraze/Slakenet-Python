""" Routes data requests """

from flask import render_template, redirect, url_for, flash, session, request, jsonify
import i18n

# from forms import SignupForm, LoginForm, AddExpenseForm, TopUpForm
from forms import SignupForm, LoginForm, TopUpForm
from dataservice import DataService

# Add locales folder to translation path
i18n.load_path.append('locales')

# Initialize Data Service
DATA_SERVICE = DataService()


def is_logged_in():
    """ Returns true if logged in """
    if 'email' in session:
        return True
    else:
        return False


def create_account():
    """ Creates new user account from signup form data """

    form = SignupForm()

    if form.validate():
        # new_user_id = DATA_SERVICE.create_account(
        #     form.email.data, form.password.data,
        #     form.name.data, form.deposit.data)
        new_user_id = DATA_SERVICE.create_account(
            form.email.data, form.password.data, form.name.data)

        if new_user_id:
            # Create new session and redirect to dashboard
            flash(i18n.t('wallet.signup_successful',
                         name=form.name.data), "success")
            session['email'] = form.email.data
            return redirect(url_for('page_dashboard'))

    flash(i18n.t('wallet.signup_invalid'), "error")
    return render_template('home.html', signup_form=form, login_form=LoginForm())


def login():
    """ Authenticates users based on login form data """

    form = LoginForm()

    if form.validate():
        authenticated_user = DATA_SERVICE.login(
            form.email.data, form.password.data)

        if authenticated_user[0]:
            # Create new session and redirect to dashboard
            flash(i18n.t('wallet.login_successful',
                         name=authenticated_user[1]), "success")
            session['email'] = form.email.data
            return redirect(url_for('page_dashboard'))

        flash(i18n.t('wallet.login_failed'), "error")
        return render_template('home.html', login_form=form, signup_form=SignupForm())

    flash(i18n.t('wallet.login_invalid'), "error")
    return render_template('home.html', login_form=form, signup_form=SignupForm())


def logout():
    """ Clears user session and redirects to index page """
    session.pop('email', None)
    flash(i18n.t('wallet.logged_out'), "success")
    return redirect(url_for('page_index'))


def load_user_balance():
    """ Gets user account balance """
    account_balance = DATA_SERVICE.load_user_balance(session['email'])
    return account_balance

def update_user_balance(email, amount):
    account_balance = DATA_SERVICE.update_balance(email, amount)
    return jsonify(account_balance)

def get_account_details():
    """ Gets account details based on an ID """
    account_details = DATA_SERVICE.get_account_details(session['email'])
    return account_details


def topup():
    """ Tops up user account with specified amount """
    if not is_logged_in():
        return redirect(url_for('page_index'))

    form = TopUpForm()

    if form.validate():
        status = DATA_SERVICE.topup_account(session['email'], form.amount.data)
        flash(status, "success")
        return redirect(url_for('page_profile'))

    flash(i18n.t('wallet.topup_invalid'), "error")
    account_details = get_account_details()
    return render_template('profile.html', logged_in=True, account=account_details, topup_form=TopUpForm())

# def verify_email():DATA_SERVICE.verify_email(session['email'])
def verify_email(email):return DATA_SERVICE.verify_email(email)

def get_reset_token(email):DATA_SERVICE.get_reset_token(email)

def verify_reset_token():DATA_SERVICE.verify_reset_token(get_reset_token())

