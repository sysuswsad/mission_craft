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
		<h1>Dear {}</h1>
		<p>
			Here is the verification code for you:
			<b>{}</b>. 
			Please finish register in 30 minutes and don't tell this message to others for your safety.
		</p>
		<p>Thank you for your support and wish you enjoying yourself</p>
	'''.format(to, code)
	app = current_app._get_current_object()
	thread = Thread(target=send_async, args=[app, message])
	thread.start()
	return thread
