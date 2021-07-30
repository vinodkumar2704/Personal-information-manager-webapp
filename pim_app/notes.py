

from flask import Blueprint
from flask import render_template,request,jsonify,redirect,url_for
import psycopg2
from flask import g
from . import db
from datetime import date


bp = Blueprint("notes","pim_app",url_prefix="")

@bp.route("/",methods = ["GET","POST",])
def dashboard():
    dbconn = db.get_db()
    cursor = dbconn.cursor()
    if request.method == "GET":
        oby = request.args.get("order_by","date")
        order = request.args.get("order","desc")
        if order == "asc":
            cursor.execute("select id,created_on,title from notes order by created_on")
        else:
            
            cursor.execute("select id,created_on,title from notes order by created_on desc")
        n_lists=cursor.fetchall()
        
        dbconn.commit()
        
        return render_template("notes.html",notes=n_lists,order = "desc" if order=="asc" else "asc")
    elif request.method == "POST":
         search = request.form.get("search")
         print(search)
         if search:
            oby = request.args.get("order_by","date")
            order = request.args.get("order","desc")
            search = '%'+search+'%'
            if order == "asc":
                cursor.execute("select id,created_on,title from notes where title like (%s) order by created_on",(search,))
            else:
                
                cursor.execute("select id,created_on,title from notes where title like (%s) order by created_on desc",(search,))
            n_lists=cursor.fetchall()
            dbconn.commit()
            print(n_lists)
            return render_template("notes.html",notes=n_lists,order = "desc" if order=="asc" else "asc")
            
         else:
            return redirect(url_for("notes.dashboard"), 302)


@bp.route("/<tid>/info" ,  methods=["GET", "POST",])
def notes_info(tid): 
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select created_on,title,description from notes where id = %s",(tid,))
    notes_info = cursor.fetchone()
    if request.method == 'GET':
        if not notes_info :
            return render_template("notes_info.html"),404
            
        cursor.execute("select t.tag from notes n,hashtags t,links l where n.id = %s and l.notes_id = %s and t.id = l.tag_id", (tid,tid))
        tags = (x[0] for x in cursor.fetchall())
        date, title, description = notes_info 
        data = dict(tid = tid,
                    name = title,
                    date = date,
                    description = description, 
                    tags = tags)
        return render_template("notes_info.html", **data)
    elif request.method == 'POST':
        return 'success'
    
    
    
@bp.route("/new" ,  methods=["GET", "POST",])
def new_notes():
    if request.method == "GET":return render_template("new_notes.html")
    elif request.method == "POST":
        title = request.form.get("title")
        description=request.form.get("description")
        hashtags=request.form.get("hashtags")
        tags = hashtags.splitlines()
        
        today = date.today()
        
        dbconn = db.get_db()
        cursor = dbconn.cursor()
        cursor.execute("INSERT INTO notes (created_on,title,description) VALUES (%s,%s,%s)",(today,title,description))
        cursor.execute("select id from notes where title = (%s)",(title,))
        title_id = int(cursor.fetchone()[0])
        
        for tag in tags:
            cursor.execute("INSERT INTO hashtags (tag) VALUES (%s) ON CONFLICT DO NOTHING",(tag,))
            cursor.execute("select id from hashtags where tag = (%s) ",(tag,))
            tag_id = int(cursor.fetchone()[0])
            cursor.execute("INSERT INTO links (notes_id,tag_id) values (%s,%s) ON CONFLICT (notes_id,tag_id) DO NOTHING",(title_id,tag_id))
        cursor.close()
        dbconn.commit()
 
  
    return redirect(url_for("notes.dashboard"), 302)
    
    
    

@bp.route("/<tid>/edit" ,  methods=["GET", "POST",])
def edit(tid):
    dbconn = db.get_db()
    cursor = dbconn.cursor()
    if request.method == "GET":
        cursor.execute("select title,description from notes where id = %s",(tid,))
        notes_info = cursor.fetchone()
        
        cursor.execute("select t.tag from notes n,hashtags t,links l where n.id = %s and l.notes_id = %s and t.id = l.tag_id", (tid,tid))
        tags = (x[0] for x in cursor.fetchall())
        tags = "\r\n".join(tags)
        title, description = notes_info 
        data = dict(tid = tid,
                    title = title,
                    description = description, 
                    hashtags = tags)
        return render_template("notes_edit.html", **data)
        
    elif request.method == "POST":
        title = request.form.get("title")
        description=request.form.get("description")
        hashtags=request.form.get("hashtags")
        tags = hashtags.splitlines()
        
        cursor.execute("update notes set title=(%s),description = (%s) where id = (%s)" ,(title,description,tid))
        for tag in tags:
            cursor.execute("INSERT INTO hashtags (tag) VALUES (%s) ON CONFLICT DO NOTHING",(tag,))
            cursor.execute("select id from hashtags where tag = (%s)",(tag,))
            tag_id = int(cursor.fetchone()[0])
            cursor.execute("INSERT INTO links (notes_id,tag_id) values (%s,%s) ON CONFLICT DO NOTHING",(tid,tag_id))
        cursor.close()
        dbconn.commit()
  
    return redirect(url_for("notes.notes_info",tid = tid), 302)
    
    

@bp.route("/<tag>/list")
def taglist(tag):
    dbconn = db.get_db()
    cursor = dbconn.cursor()
    oby = request.args.get("order_by","date")
    order = request.args.get("order","desc")
    tag = tag
    cursor.execute("select tag from hashtags")
    all_tags = cursor.fetchall()
    print(all_tags)
    if order == "asc":
        cursor.execute("select n.id,n.created_on,n.title from notes n ,hashtags t,links l where n.id = l.notes_id and t.id = l.tag_id and t.tag = (%s) order by n.created_on",(tag,))
    else:
        
        cursor.execute("select n.id,n.created_on,n.title from notes n ,hashtags t,links l where n.id = l.notes_id and t.id = l.tag_id and t.tag = (%s) order by n.created_on desc",(tag,))
    n_lists=cursor.fetchall()
    dbconn.commit()
    print(n_lists)
    return render_template("tagsearch.html",notes=n_lists,tag=tag,all_tags=all_tags,order = "desc" if order=="asc" else "asc")
    




















    
