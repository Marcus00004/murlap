from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

class FormResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    partner_id = db.Column(db.Integer)
    template_id = db.Column(db.Integer)
    submitted_at = db.Column(db.DateTime, default=db.func.now())
    answers = db.relationship('FormAnswer', backref='response', cascade='all, delete')

class FormAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.Integer, db.ForeignKey('form_response.id'))
    question_id = db.Column(db.Integer)
    score = db.Column(db.Integer)
    comment = db.Column(db.String(500))

@app.route('/fill_form', methods=['GET', 'POST'])
@login_required
def fill_form():
    if request.method == 'POST':
        partner_id = request.form['partner_id']
        template_id = request.form['template_id']
        response = FormResponse(user_id=current_user.id, partner_id=partner_id, template_id=template_id)
        db.session.add(response)
        db.session.commit()

        for key in request.form:
            if key.startswith('q_'):
                qid = int(key.split('_')[1])
                score = int(request.form.get(f'q_{qid}', 0))
                comment = request.form.get(f'c_{qid}', '')
                answer = FormAnswer(response_id=response.id, question_id=qid, score=score, comment=comment)
                db.session.add(answer)

        db.session.commit()
        return redirect(url_for('dashboard'))

    partners = Partner.query.all()
    templates = FormTemplate.query.all()
    return render_template('fill_form.html', partners=partners, templates=templates)

@app.route('/form/<int:template_id>/render')
@login_required
def render_template_questions(template_id):
    template = FormTemplate.query.get(template_id)
    if not template:
        return redirect(url_for('fill_form'))
    return render_template('form_questions.html', template=template)
