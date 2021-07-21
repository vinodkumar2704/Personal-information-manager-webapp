

from flask import Blueprint
from flask import render_template,request

from flask import g
from . import db


bp = Blueprint("notes","pim_app",url_prefix="")

@bp.route("/")
def dashboard():
    dbconn = db.get_db()
    cursor = dbconn.cursor()
    oby = request.args.get("order_by","date")
    order = request.args.get("order","asc")
    cursor.execute("select created_on,title from notes")
    n_lists=cursor.fetchall()
    
    dbconn.commit()
    
    return render_template("notes.html",notes=n_lists)

