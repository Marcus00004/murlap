from flask import send_file, redirect, url_for
from io import BytesIO
import pandas as pd

@app.route('/export/excel/<int:response_id>')
@login_required
def export_excel(response_id):
    response = FormResponse.query.get_or_404(response_id)

    if current_user.role not in ['admin', 'manager'] and response.user_id != current_user.id:
        return redirect(url_for('dashboard'))

    template = FormTemplate.query.get(response.template_id)
    partner = Partner.query.get(response.partner_id)
    answers = FormAnswer.query.filter_by(response_id=response.id).all()
    questions = {q.id: q.text for q in template.questions}

    data = []
    for a in answers:
        data.append({
            'Kérdés': questions[a.question_id],
            'Pontszám': a.score,
            'Megjegyzés': a.comment
        })

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Valaszok')
        ws = writer.sheets['Valaszok']
        ws.write(0, 4, 'Partner: ' + partner.name)
        ws.write(1, 4, 'Űrlap: ' + template.name)
        ws.write(2, 4, 'Dátum: ' + response.submitted_at.strftime('%Y.%m.%d %H:%M'))

    output.seek(0)
    filename = f"urlap_{response.id}.xlsx"
    return send_file(output, download_name=filename, as_attachment=True)
