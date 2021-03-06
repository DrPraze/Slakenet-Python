""" Defines form backends """

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email, Length, NumberRange


class SignupForm(FlaskForm):
    """ Defines the sign up form fields """

    email = StringField('Email', validators=[
        DataRequired('Your email'),
        Email('Please enter your email')])

    password = PasswordField('Password', validators=[
        DataRequired('enter your password'),
        Length(min=7, message='Password must be 7 or more characters')])

    name = StringField('Name', validators=[
        DataRequired('Please enter your user name')])

    # deposit = DecimalField('Deposit Amount', validators=[
    #     DataRequired('Please add a deposit amount'),
    #     NumberRange(min=0, message='Please enter a valid number')])
    # deposit = 0

    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    """ Defines the log in form fields """

    email = StringField('Email', validators=[
        DataRequired('Please enter your email'),
        Email('Please enter your email')])

    password = PasswordField('Password', validators=[
        DataRequired('Please enter your password'),
        Length(min=7, message='Password must be 7 or more characters')])

    submit = SubmitField('Log in')


# class AddExpenseForm(FlaskForm):
#     """ Defines the add expense form fields """

#     amount = DecimalField('Amount', validators=[
#         DataRequired('Please enter an amount'),
#         NumberRange(min=0, max=9999999999, message='Please enter a valid number')])

#     note = StringField('Note', validators=[
#         DataRequired('Please add a note')])


class TopUpForm(FlaskForm):
    """ Defines the top up form """
    # Integrate reloadly API here

    amount = DecimalField('Amount', validators=[
        DataRequired('Please enter an amount'),
        NumberRange(min=50, max=100000, message='Deposit should be between 50 and 100000')])
