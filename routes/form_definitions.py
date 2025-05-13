
from flask import request, render_template, redirect, url_for
from app import db

class FormTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

def init_form_routes(app):
    @app.route('/forms')
    def list_forms_view():
        forms = FormTemplate.query.all()
        return render_template('forms.html', forms=forms)
