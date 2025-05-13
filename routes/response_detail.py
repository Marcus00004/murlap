from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

@app.route('/response/<int:response_id>')
@login_required
def view_response(response_id):
    response = FormResponse.query.get_or_404(response_id)

    if current_user.role not in ['admin', 'manager'] and response.user_id != current_user.id:
        return redirect(url_for('dashboard'))

    partner = Partner.query.get(response.partner_id)
    template = FormTemplate.query.get(response.template_id)
    answers = FormAnswer.query.filter_by(response_id=response.id).all()

    questions = {q.id: q.text for q in template.questions}
    return render_template('response_detail.html', response=response, partner=partner, template=template, answers=answers, questions=questions)
