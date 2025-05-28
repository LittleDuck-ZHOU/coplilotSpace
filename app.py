from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
import csv
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nippou.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

class Nippou(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.Date, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def is_today(self):
        return self.report_date == date.today()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    today = date.today()
    if Nippou.query.filter_by(report_date=today).first():
        flash('本日の日報は既に登録されています。編集してください。')
        return redirect(url_for('index'))
    nippou = Nippou(report_date=today, content=content)
    db.session.add(nippou)
    db.session.commit()
    flash('日報を登録しました。')
    return redirect(url_for('index'))

@app.route('/list')
def list_nippou():
    search_date = request.args.get('search_date')
    week_offset = int(request.args.get('week_offset', 0))
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=6)
    if search_date:
        nippous = Nippou.query.filter_by(report_date=search_date).all()
    else:
        nippous = Nippou.query.filter(Nippou.report_date >= start_of_week, Nippou.report_date <= end_of_week).order_by(Nippou.report_date).all()
    return render_template('list.html', nippous=nippous, search_date=search_date or '', week_offset=week_offset)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    nippou = Nippou.query.get_or_404(id)
    if not nippou.is_today():
        flash('当日以外の日報は編集できません。')
        return redirect(url_for('list_nippou'))
    if request.method == 'POST':
        nippou.content = request.form['content']
        db.session.commit()
        flash('日報を更新しました。')
        return redirect(url_for('list_nippou'))
    return render_template('edit.html', nippou=nippou)

@app.route('/delete/<int:id>')
def delete(id):
    nippou = Nippou.query.get_or_404(id)
    if not nippou.is_today():
        flash('当日以外の日報は削除できません。')
        return redirect(url_for('list_nippou'))
    db.session.delete(nippou)
    db.session.commit()
    flash('日報を削除しました。')
    return redirect(url_for('list_nippou'))

@app.route('/download')
def download():
    week_offset = int(request.args.get('week_offset', 0))
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=6)
    nippous = Nippou.query.filter(Nippou.report_date >= start_of_week, Nippou.report_date <= end_of_week).order_by(Nippou.report_date).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['日付', '内容'])
    for n in nippous:
        writer.writerow([n.report_date.strftime('%Y-%m-%d'), n.content])
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode('utf-8-sig')), mimetype='text/csv', as_attachment=True, download_name='nippou.csv')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8080)
