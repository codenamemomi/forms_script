from flask import Flask, render_template, request, redirect
import pandas as pd
import os

app = Flask(__name__)

# Excel file path
EXCEL_FILE = 'user_tech_profiles.xlsx'

# Ensure the Excel file exists
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=['Email', 'Full Name', 'Tech Stack'])
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        tech_stack = request.form.getlist('tech_stack')  # Get multiple selections
        tech_stack_str = ', '.join(tech_stack)  # Convert list to string

        # Append to Excel
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, pd.DataFrame([{
            'Email': email,
            'Full Name': f"{first_name} {last_name}",
            'Tech Stack': tech_stack_str
        }])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)

        return redirect('/success')

    return render_template('forms.html')

@app.route('/success')
def success():
    return "✅ Data submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)
