from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy

# Feltételezzük, hogy db és app már létezik

class FormTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    questions = db.relationship('FormQuestion', backref='template', cascade='all, delete')

class FormQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('form_template.id'))
    text = db.Column(db.String(300), nullable=False)
    scale_min = db.Column(db.Integer, default=1)
    scale_max = db.Column(db.Integer, default=5)

@app.route('/forms')
@login_required
def list_forms():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    forms = FormTemplate.query.all()
    return render_template('forms.html', forms=forms)

@app.route('/forms/create', methods=['GET', 'POST'])
@login_required
def create_form():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        name = request.form['name']
        template = FormTemplate(name=name)
        db.session.add(template)
        db.session.commit()

        for text in request.form.getlist('question_text'):
            if text.strip():
                question = FormQuestion(template_id=template.id, text=text.strip())
                db.session.add(question)

        db.session.commit()
        return redirect(url_for('list_forms'))
    return render_template('form_create.html')

@app.route('/forms/delete/<int:form_id>')
@login_required
def delete_form(form_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    form = FormTemplate.query.get(form_id)
    if form:
        db.session.delete(form)
        db.session.commit()
    return redirect(url_for('list_forms'))
