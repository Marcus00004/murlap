from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func

@app.route('/reports')
@login_required
def report_list():
    if current_user.role not in ['admin', 'manager']:
        return redirect(url_for('dashboard'))

    query = db.session.query(
        FormResponse.id,
        Partner.name.label('partner_name'),
        FormTemplate.name.label('form_name'),
        FormResponse.submitted_at,
        func.count(FormAnswer.id).label('answer_count'),
        func.avg(FormAnswer.score).label('avg_score')
    ).join(Partner, Partner.id == FormResponse.partner_id)
    query = query.join(FormTemplate, FormTemplate.id == FormResponse.template_id)
    query = query.join(FormAnswer, FormAnswer.response_id == FormResponse.id)
    query = query.group_by(FormResponse.id, Partner.name, FormTemplate.name, FormResponse.submitted_at)

    start = request.args.get('start')
    end = request.args.get('end')
    if start:
        query = query.filter(FormResponse.submitted_at >= start)
    if end:
        query = query.filter(FormResponse.submitted_at <= end)

    results = query.order_by(FormResponse.submitted_at.desc()).all()
    return render_template('reports.html', reports=results)
