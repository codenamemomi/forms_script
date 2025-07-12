from flask import Flask, render_template, request, redirect
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
TO_EMAIL = 'akinrogundej@gmail.com'  

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        tech_stack = request.form.getlist('tech_stack')
        tech_stack_str = ', '.join(tech_stack)

        # Compose email
        subject = "New Tech Profile Submission"
        content = f"""
        Email: {email}
        Name: {first_name} {last_name}
        Tech Stack: {tech_stack_str}
        """

        message = Mail(
            from_email=email,
            to_emails=TO_EMAIL,
            subject=subject,
            plain_text_content=content
        )

        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            sg.send(message)
        except Exception as e:
            return f"❌ Failed to send email: {e}"

        return redirect('/success')

    return render_template('forms.html')

@app.route('/success')
def success():
    return "✅ Data submitted and emailed successfully!"

if __name__ == '__main__':
    app.run(debug=True)
