# app.py
from flask import Flask, render_template, redirect, url_for, request, send_file, flash
from datetime import datetime
import csv
import io
import os

# Import the db instance from extensions
from extensions import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this!
# This path will create tickets.db in your project root; adjust as needed.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tickets.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db with the app
db.init_app(app)

# Import models after db is initialized
from models import Ticket, Category, ProblemType
from forms import TicketForm, ExportForm

@app.route('/')
def index():
    return redirect(url_for('new_ticket'))

# New Ticket Page
@app.route('/new_ticket', methods=['GET', 'POST'])
def new_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            user_category=form.user_category.data,
            user_email=form.user_email.data,
            problem_type=form.problem_type.data,
            description=form.description.data,
            timestamp=datetime.utcnow()
        )
        db.session.add(ticket)
        db.session.commit()
        flash("Ticket logged successfully!", "success")
        return redirect(url_for('new_ticket'))
    return render_template('new_ticket.html', form=form)

# History Page: List tickets and allow filtering
@app.route('/history', methods=['GET'])
def history():
    # Basic filter: you could expand this later
    tickets = Ticket.query.order_by(Ticket.timestamp.desc()).all()
    return render_template('history.html', tickets=tickets)

from datetime import datetime, time

@app.route('/export', methods=['GET', 'POST'])
def export():
    form = ExportForm()
    if form.validate_on_submit():
        start_date = form.start_date.data  # e.g. 2025-02-13 (a date object)
        end_date = form.end_date.data      # e.g. 2025-02-13

        # Convert to datetime for the entire day
        start_datetime = datetime.combine(start_date, time.min)
        end_datetime = datetime.combine(end_date, time.max)

        tickets = Ticket.query.filter(
            Ticket.timestamp.between(start_datetime, end_datetime)
        ).all()

        # Build CSV
        si = io.StringIO()
        cw = csv.writer(si)
        cw.writerow(['ID', 'User Category', 'User Email', 'Problem Type', 'Description', 'Timestamp'])
        for ticket in tickets:
            cw.writerow([
                ticket.id,
                ticket.user_category,
                ticket.user_email,
                ticket.problem_type,
                ticket.description,
                ticket.timestamp
            ])
        output = io.BytesIO()
        output.write(si.getvalue().encode('utf-8'))
        output.seek(0)
        return send_file(output, mimetype='text/csv', as_attachment=True, download_name='tickets.csv')
    
    return render_template('export.html', form=form)





# Admin Page (For managing categories and problem types) -- simplified for now
@app.route('/admin')
def admin():
    # For simplicity, this page just shows current categories and problem types.
    categories = Category.query.all()
    problem_types = ProblemType.query.all()
    return render_template('admin.html', categories=categories, problem_types=problem_types)

if __name__ == '__main__':
    app.run(debug=True)
