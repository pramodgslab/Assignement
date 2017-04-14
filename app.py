from flask import Flask, render_template, json, request,url_for
import urllib2
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'microsoft'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
url = "https://api.github.com/orgs/microsoft/events"

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/setMainMasters')
def setMainMasters():
    #data = json.loads("""[{    "id": "5659998110",    "type": "DeleteEvent",    "actor": {      "id": 2082726,      "login": "raaaar",      "display_login": "raaaar",      "gravatar_id": "",      "url": "https://api.github.com/users/raaaar",      "avatar_url": "https://avatars.githubusercontent.com/u/2082726?"    },    "repo": {      "id": 46918116,      "name": "Microsoft/CNTK",      "url": "https://api.github.com/repos/Microsoft/CNTK"    },    "payload": {      "ref": "alrezni/quick_fix",      "ref_type": "branch",      "pusher_type": "user"    },    "public": true,    "created_at": "2017-04-10T14:14:44Z",    "org": {      "id": 6154722,      "login": "Microsoft",      "gravatar_id": "",      "url": "https://api.github.com/orgs/Microsoft",      "avatar_url": "https://avatars.githubusercontent.com/u/6154722?"    }  }]""");
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    conn = mysql.connect()
    cursor = conn.cursor()
    for obj in data:
            try:
                cursor.execute("""replace into actor(id,login,display_login,url,avatar_url) values (%s,%s,%s,%s,%s)""", (obj["actor"]["id"],obj["actor"]["login"],obj["actor"]["display_login"],obj["actor"]["url"],obj["actor"]["avatar_url"]))
                conn.commit()
            except IOError as err:
                print err.read();
                conn.rollback()
            try:
                cursor.execute("""replace into repo(id,name,url) values(%s,%s,%s)""",
                               (obj["repo"]["id"], obj["repo"]["name"], obj["repo"]["url"]))
                conn.commit()
            except IOError as err:
                print err.read();
                conn.rollback()
            try:
                cursor.execute("""replace into org(id,login,url,avatar_url) values (%s,%s,%s,%s)""", (obj["org"]["id"],obj["org"]["login"],obj["org"]["url"],obj["org"]["avatar_url"]))
                conn.commit()
            except IOError as err:
                print err.read();
                conn.rollback()

            try:
                dateStr = str(obj["created_at"]).replace("Z", "").replace("T", " ");
                if obj["type"] == "DeleteEvent":
                    cursor.execute("""replace into MainMaster(id,type,public,created_at,created_at_date,actor_fid,repo_fid,org_fid,ref,ref_type,pusher_type) values(%s,%s,1,%s,%s,%s,%s,%s,%s,%s,%s)""",
                               (obj["id"], obj["type"], obj["created_at"], dateStr,obj["actor"]["id"],obj["repo"]["id"],obj["org"]["id"],obj["payload"]["ref"],obj["payload"]["ref_type"],obj["payload"]["pusher_type"]))
                if obj["type"] != "DeleteEvent":
                    cursor.execute(
                        """replace into MainMaster(id,type,public,created_at,created_at_date,actor_fid,repo_fid,org_fid) values(%s,%s,1,%s,%s,%s,%s,%s)""",
                        (obj["id"], obj["type"], obj["created_at"], dateStr, obj["actor"]["id"], obj["repo"]["id"],
                         obj["org"]["id"]))
                conn.commit()
            except IOError as err:
                print err.read();
                conn.rollback()

    cursor.execute("select * from actor")
    a = cursor.fetchall()
    cursor.execute("select * from repo")
    r = cursor.fetchall()
    cursor.execute("select * from org")
    o = cursor.fetchall()
    conn.close()
    return "actors:"+str(a.__len__())+",repo:"+str(r.__len__())+",org:"+str(o.__len__())+"";

@app.route('/getMainMasters')
def getMainMasters():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""select id,type,cast(public as unsigned) public,created_at_date,concat('<a href=/getActor?id=',actor_fid,'>',actor_fid,'</a>') actor_fid,repo_fid,org_fid,ref,ref_type,pusher_type from MainMaster""")
        data1 = cursor.fetchall();
        conn.commit()
    except IOError as err:
        print err.read();
        conn.rollback()

    conn.close()
    return json.dumps(data1)

@app.route('/getActors')
def getActors():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""select * from Actor""")
        data1 = cursor.fetchall();
        conn.commit()
    except IOError as err:
        print err.read();
        conn.rollback()
    conn.close()
    return json.dumps(data1)

@app.route('/getActor/<int:id>',methods=["GET"])
def getActor(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""select * from Actor where id="+id+""")
        data1 = cursor.fetchall();
        conn.commit()
    except IOError as err:
        print err.read();
        conn.rollback()
    conn.close()
    return json.dumps(data1)


if __name__ == "__main__":
    app.run(port=5002)
