import pymysql
# connect to mysql 
conn = pymysql.connect(host="localhost",user="root",passwd='28315179',db="dd",use_unicode=True, charset="utf8")
cur = conn.cursor()             
print("mysql connected successfully!")