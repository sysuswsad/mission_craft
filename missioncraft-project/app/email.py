from . import mail
from threading import Thread
from flask import current_app
from flask_mail import Message


def send_async(msg):
	with current_app.app_context():
		mail.send(msg)


def send_verification_code(to, code):
	message = Message('Verification from mission craft', recipients=[to])
	message.body = '''
		<h1>Dear {}</h1>
		<p>
			Here is the verification code for you:
			<b>{}</b>. 
			Please finish register in 30 minutes and don't tell this message to others for your safety.
		</p>
		<p>Thank you for your support and wish you enjoying yourself</p>
	'''.format(to, code)
	thread = Thread(target=send_async, args=[current_app, message])
	thread.start()
	return thread
