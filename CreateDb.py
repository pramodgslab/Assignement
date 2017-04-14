from flask import Flask
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'microsoft'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

connection = mysql.connect()
cursor = connection.cursor()

sql_command = """
CREATE TABLE if not exists actor( 
id BIGINT PRIMARY KEY, 
login VARCHAR(1000), 
display_login VARCHAR(1000), 
gravatar_id INTEGER , 
url VARCHAR(1000),
avatar_url VARCHAR (1000)
);"""
cursor.execute(sql_command)

sql_command = """
CREATE TABLE if not exists repo( 
id BIGINT PRIMARY KEY, 
name VARCHAR(1000),  
url VARCHAR(1000)
);"""
cursor.execute(sql_command)

sql_command = """
CREATE TABLE if not exists payload( 
id BIGINT PRIMARY KEY AUTO_INCREMENT, 
ref VARCHAR(1000),  
ref_type VARCHAR(1000),
pusher_type VARCHAR (1000)
);"""
cursor.execute(sql_command)

sql_command = """
CREATE TABLE if not exists org( 
id BIGINT PRIMARY KEY, 
login VARCHAR(1000),  
url VARCHAR(1000),
avatar_url VARCHAR (1000),
gravatar_id INTEGER 
);"""
cursor.execute(sql_command)

#id,type,public,created_at_date,actor_fid,repo_fid,org_fid,ref,ref_type,pusher_type

sql_command = """
CREATE TABLE if not exists MainMaster( 
id BIGINT PRIMARY KEY, 
type VARCHAR(1000),  
public BIT ,
created_at VARCHAR(1000),
created_at_date TIMESTAMP,
actor_fid BIGINT,
repo_fid BIGINT ,
org_fid BIGINT,
ref VARCHAR (1000),
ref_type VARCHAR (1000),
pusher_type VARCHAR (1000)
);"""
cursor.execute(sql_command)