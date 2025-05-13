from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(200))
    contact = db.Column(db.String(100))

@app.route('/partners')
@login_required
def list_partners():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    partners = Partner.query.all()
    return render_template('partners.html', partners=partners)

@app.route('/partners/add', methods=['POST'])
@login_required
def add_partner():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    name = request.form['name']
    address = request.form['address']
    contact = request.form['contact']
    new_partner = Partner(name=name, address=address, contact=contact)
    db.session.add(new_partner)
    db.session.commit()
    return redirect(url_for('list_partners'))

@app.route('/partners/delete/<int:partner_id>')
@login_required
def delete_partner(partner_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    partner = Partner.query.get(partner_id)
    if partner:
        db.session.delete(partner)
        db.session.commit()
    return redirect(url_for('list_partners'))

@app.route('/partners/update/<int:partner_id>', methods=['POST'])
@login_required
def update_partner(partner_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    partner = Partner.query.get(partner_id)
    if partner:
        partner.name = request.form['name']
        partner.address = request.form['address']
        partner.contact = request.form['contact']
        db.session.commit()
    return redirect(url_for('list_partners'))
