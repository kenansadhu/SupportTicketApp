from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Email

class TicketForm(FlaskForm):
    user_category = SelectField('User Category', validators=[DataRequired()], choices=[
        ('Student', 'Student'),
        ('Staff', 'Staff'),
        ('External', 'External')
    ])
    user_email = StringField('User Email', validators=[DataRequired(), Email()])
    problem_type = SelectField('Problem Type', validators=[DataRequired()], choices=[
        ('Moodle Issue', 'Moodle Issue'),
        ('Internet Issue', 'Internet Issue'),
        ('Plugins Issue', 'Plugins Issue')
    ])
    description = TextAreaField('Problem Description', validators=[DataRequired()])
    submit = SubmitField('Submit Ticket')

class ExportForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Export as CSV')
