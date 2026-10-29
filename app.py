from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import sqlite3, os, random
from pathlib import Path
BASE=Path(__file__).resolve().parent
DB=BASE/'traffic.db'; UPLOADS=BASE/'static'/'uploads'; UPLOADS.mkdir(parents=True,exist_ok=True)
app=Flask(__name__); app.secret_key=os.environ.get('SECRET_KEY','change-this-secret'); app.config['MAX_CONTENT_LENGTH']=8*1024*1024

def connect():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c

def init_db():
 with connect() as c:
  c.executescript('''CREATE TABLE IF NOT EXISTS cameras(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,location TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'Online',created_at TEXT NOT NULL); CREATE TABLE IF NOT EXISTS incidents(id INTEGER PRIMARY KEY AUTOINCREMENT,camera_id INTEGER,incident_type TEXT NOT NULL,severity TEXT NOT NULL,details TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'Open',created_at TEXT NOT NULL,FOREIGN KEY(camera_id) REFERENCES cameras(id)); CREATE TABLE IF NOT EXISTS uploads(id INTEGER PRIMARY KEY AUTOINCREMENT,filename TEXT NOT NULL,original_name TEXT NOT NULL,result TEXT NOT NULL,created_at TEXT NOT NULL);''')
  if c.execute('SELECT COUNT(*) FROM cameras').fetchone()[0]==0:
   now=datetime.now().isoformat(timespec='seconds'); c.executemany('INSERT INTO cameras(name,location,status,created_at) VALUES(?,?,?,?)',[('Main Junction Camera','Central Avenue','Online',now),('Market Road Camera','Market Road','Online',now),('Highway Entry Camera','NH-48 Entry','Offline',now),('School Zone Camera','Green Park School','Online',now)])
  if c.execute('SELECT COUNT(*) FROM incidents').fetchone()[0]==0:
   n=datetime.now(); c.executemany('INSERT INTO incidents(camera_id,incident_type,severity,details,status,created_at) VALUES(?,?,?,?,?,?)',[(1,'Congestion','Medium','Traffic density above demo threshold','Open',(n-timedelta(minutes=12)).isoformat(timespec='seconds')),(2,'Possible wrong-way movement','High','Requires operator verification','Open',(n-timedelta(minutes=31)).isoformat(timespec='seconds')),(4,'Stopped vehicle','Low','Possible obstruction near crossing','Resolved',(n-timedelta(hours=2)).isoformat(timespec='seconds'))])
@app.route('/')
def index():
 with connect() as c:
  cameras=c.execute('SELECT * FROM cameras ORDER BY id').fetchall(); incidents=c.execute('SELECT incidents.*,cameras.name camera_name FROM incidents LEFT JOIN cameras ON cameras.id=incidents.camera_id ORDER BY incidents.created_at DESC LIMIT 10').fetchall()
  stats={'cameras':c.execute('SELECT COUNT(*) FROM cameras').fetchone()[0],'online':c.execute("SELECT COUNT(*) FROM cameras WHERE status='Online'").fetchone()[0],'open':c.execute("SELECT COUNT(*) FROM incidents WHERE status='Open'").fetchone()[0],'high':c.execute("SELECT COUNT(*) FROM incidents WHERE severity='High' AND status='Open'").fetchone()[0]}
 return render_template('index.html',cameras=cameras,incidents=incidents,stats=stats)
@app.route('/api/traffic')
def traffic():
 n=datetime.now(); return jsonify({'mode':'simulation','updated_at':n.strftime('%H:%M:%S'),'points':[{'time':(n-timedelta(minutes=(11-i)*5)).strftime('%H:%M'),'vehicles':random.randint(18,85)} for i in range(12)]})
@app.route('/cameras',methods=['POST'])
def add_camera():
 name=request.form.get('name','').strip(); loc=request.form.get('location','').strip()
 if not name or not loc: flash('Camera name and location are required.','error')
 else:
  with connect() as c:c.execute('INSERT INTO cameras(name,location,status,created_at) VALUES(?,?,?,?)',(name,loc,'Online',datetime.now().isoformat(timespec='seconds')))
  flash('Camera added.','success')
 return redirect(url_for('index'))
@app.route('/incidents',methods=['POST'])
def add_incident():
 typ=request.form.get('incident_type','').strip(); details=request.form.get('details','').strip(); sev=request.form.get('severity','Medium'); cid=request.form.get('camera_id',type=int)
 if not typ or not details: flash('Incident type and details are required.','error')
 else:
  with connect() as c:c.execute('INSERT INTO incidents(camera_id,incident_type,severity,details,status,created_at) VALUES(?,?,?,?,?,?)',(cid,typ,sev,details,'Open',datetime.now().isoformat(timespec='seconds')))
  flash('Incident logged. Please verify it manually.','success')
 return redirect(url_for('index'))
@app.route('/incidents/<int:iid>/resolve',methods=['POST'])
def resolve(iid):
 with connect() as c:c.execute("UPDATE incidents SET status='Resolved' WHERE id=?",(iid,))
 return redirect(url_for('index'))
@app.route('/analyze',methods=['POST'])
def analyze():
 f=request.files.get('image'); allowed={'png','jpg','jpeg','webp'}
 if not f or not f.filename: flash('Choose an image first.','error'); return redirect(url_for('index'))
 ext=f.filename.rsplit('.',1)[-1].lower() if '.' in f.filename else ''
 if ext not in allowed: flash('Use PNG, JPG, JPEG or WEBP.','error'); return redirect(url_for('index'))
 original=secure_filename(f.filename); filename=datetime.now().strftime('%Y%m%d%H%M%S%f')+'_'+original; f.save(UPLOADS/filename); result='Image stored for manual review. AI vehicle detection is not configured in this demo.'
 with connect() as c:c.execute('INSERT INTO uploads(filename,original_name,result,created_at) VALUES(?,?,?,?)',(filename,original,result,datetime.now().isoformat(timespec='seconds')))
 flash(result,'success'); return redirect(url_for('index'))
@app.route('/health')
def health():return jsonify({'status':'ok','mode':'demo'})
if __name__=='__main__': init_db(); app.run(debug=True)
