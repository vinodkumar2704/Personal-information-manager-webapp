

# Other modules can import this and use the functions here. 
import psycopg2

# click is a library installed as a dependency of flask which is used
# to add extra commands to the flask executable. We already have
# "flask run" but we can add more commands like "flask initdb" etc.
import click 
from flask import current_app, g
from flask.cli import with_appcontext
from faker import Faker

import datetime


def get_db():
    if 'db' not in g: 
        dbname = current_app.config['DATABASE'] 
        g.db = psycopg2.connect(f"dbname={dbname}")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    
    f = current_app.open_resource("sql/pim.sql")
    sql_code=f.read().decode("ascii")
    cursor = db.cursor()
    cursor.execute(sql_code)
    cursor.close()
    
    
    faker = Faker() # Used to create dummy date
    cur = db.cursor()
    for i in range(3):
        
        description = "hello hi good morning."
        bought = datetime.datetime.strptime(faker.date(), '%Y-%m-%d').date()
        title = "rick and morty"
        
        cur.execute("INSERT INTO notes (created_on,title,description) VALUES (%s,%s,%s)",(bought,title[i:],description[i:]))
        
        tag = "summer"
        cur.execute("INSERT INTO hashtags (tag) VALUES (%s)",(tag[i:],))
        cur.execute("insert into links (notes_id,tag_id) values (%s,%s)",(i+1,i+1))
            
    click.echo("notes added")

    click.echo("tags and links added")
    cur.close()
    db.commit()
    close_db()
    
@click.command('initdb', help="initialise the database") 
@with_appcontext
def init_db_command():
    init_db()
    click.echo('DB initialised')


def init_app(app):
    app.teardown_appcontext(close_db) 
    app.cli.add_command(init_db_command)


