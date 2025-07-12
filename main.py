from flask import Flask, render_template, request, redirect
import os
import traceback
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
TO_EMAIL = 'akinrogundej@gmail.com'  # Your receiving email
FROM_EMAIL = 'akinrogundep0@gmail.com'  # Must be a verified sender in SendGrid

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        tech_stack = request.form.getlist('tech_stack')
        tech_stack_str = ', '.join(tech_stack)

        # Compose email content
        subject = "New Tech Profile Submission"
        content = (
            f"Email: {email}\n"
            f"Name: {first_name} {last_name}\n"
            f"Tech Stack: {tech_stack_str}"
        )

        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=TO_EMAIL,
            subject=subject,
            plain_text_content=content
        )

        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            sg.send(message)
        except Exception as e:
            error_details = traceback.format_exc()
            return f"❌ Failed to send email:\n<pre>{error_details}</pre>"

        return redirect('/success')

    return render_template('forms.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
