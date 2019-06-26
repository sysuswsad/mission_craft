from app import mail
from threading import Thread
from flask import current_app
from flask_mail import Message


def send_async(app, msg):
	with app.app_context():
		mail.send(msg)


def send_verification_code(to, code):
	message = Message('Verification from mission craft', recipients=[to])
	message.body = '''
		Dear {}
			Here is the verification code for you:
				{}
			Please finish register in 30 minutes and don't tell this message to others for your safety.
			Thank you for your support and wish you enjoying yourself
	'''.format(to, code)
	app = current_app._get_current_object()
	thread = Thread(target=send_async, args=[app, message])
	thread.start()
	return thread
