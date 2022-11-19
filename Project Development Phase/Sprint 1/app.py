from flask import Flask, render_template, request, redirect, url_for, session, flash
import ibm_db
from markupsafe import escape
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


app = Flask(__name__)
app.secret_key = 'your secret key'


conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32716;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=rdb98826;PWD=8RbXIwMNNwOtDRaA;", "", "")
print(conn)
print("connection successful...")
@app.route('/agent',methods=['POST', 'GET'])
def agent():
      return render_template('agentlogin.html')

@app.route('/new',methods=['POST', 'GET'])
def new():
      return render_template('userlogin.html')



@app.route('/logagent',methods=['POST', 'GET'])
def logagent():
       if request.method == 'POST':
            try:
              id = request.form['name']
              password = request.form['password']

              sql = f"select * from agent where name='{escape(id)}' and passsword='{escape(password)}'"
              stmt = ibm_db.exec_immediate(conn, sql)
              data = ibm_db.fetch_both(stmt)
              print(data)
              if data:
                session["name"] = escape(id)
                session["password"] = escape(password)
                return redirect(url_for("agenthome",name=id))

              else:
                    flash("Mismatch in credetials", "danger")
            except:
              
              flash("Error in Insertion operation", "danger")

            return render_template("agentlogin.html")


@app.route('/agenthome/<name>',methods=['POST', 'GET'])
def agenthome(name):
      com = []
      sql =f"SELECT complaint_id,customer_name,complaint,complaint_detail FROM complaint where status='no'and agent='{escape(name)}'"
      stmt = ibm_db.exec_immediate(conn, sql)
      dictionary = ibm_db.fetch_both(stmt)
      while dictionary != False:
            com.append(dictionary)
            dictionary = ibm_db.fetch_both(stmt)
      return render_template('agenthome.html',comp=com , name=name)
@app.route('/addsoluin',methods=['POST', 'GET'])
def addsoluin():
        if request.method =='POST':
             try:
               nam=request.form['gname']
               solu = request.form['solution']
               cid = request.form['cid']
               sql=f"UPDATE COMPLAINT SET solution='{escape(solu)}',status='yes' WHERE COMPLAINT_ID='{escape(cid)}';"
               ibm_db.exec_immediate(conn, sql)
             except:
               flash("Error in Insertion operation", "danger")
             finally:
               flash('Solution Send Successfully')
               return redirect(url_for('agenthome',name=nam))
      



@app.route('/userhome/<name>')
def userhome(name):
       return render_template('userhome.html',name=name)

@app.route('/file_complaint/<name>',methods=['POST', 'GET'])
def file_complaint(name):
       return render_template('filecomplaint.html',nam=name)
@app.route('/view_status/<name>',methods=['POST', 'GET'])
def view_status(name):
      com = []
      sql =f"SELECT complaint_id,customer_name,complaint,complaint_detail,agent,solution FROM complaint where customer_name='{escape(name)}'"
      stmt = ibm_db.exec_immediate(conn, sql)
      dictionary = ibm_db.fetch_both(stmt)
      while dictionary != False:
            com.append(dictionary)
            dictionary = ibm_db.fetch_both(stmt)
      return render_template('view_status.html',comp=com,nam=name)
      
       

@app.route('/')
def home():
       return render_template('index.html')

@app.route('/agentadd')
def agentadd():
       return render_template('agentadd.html')
@app.route('/addagent',methods=['POST', 'GET'])
def addagent():
       if request.method =='POST':
             try:
               agent= request.form['agentname']
               mail= request.form['agentmail']
               password=request.form['password']
               sql=f"INSERT INTO agent (name,email, passsword )VALUES ('{escape(agent)}', '{escape(mail)}', '{escape(password)}');"
               ibm_db.exec_immediate(conn, sql)
             except:
               flash("Error in Insertion operation", "danger")
             finally:
               flash('Agent added successfully')
               return render_template('adminhome.html') 
@app.route('/assignagent')
def assignagent():
        com = []
        sql =f"SELECT complaint_id,customer_name,complaint,complaint_detail FROM complaint where agent='Pending...'"
        stmt = ibm_db.exec_immediate(conn, sql)
        dictionary = ibm_db.fetch_both(stmt)
        while dictionary != False:
             com.append(dictionary)
             dictionary = ibm_db.fetch_both(stmt)

        agent=[]    
        sql1 = f"SELECT agent_id,name FROM agent"
        stmt1 = ibm_db.exec_immediate(conn, sql1)
        dictionary1 = ibm_db.fetch_both(stmt1)
        print(dictionary1)
        while dictionary1 != False:
             agent.append(dictionary1)
             dictionary1= ibm_db.fetch_both(stmt1)
        return render_template('assignagent.html',data=com,a=agent)   
@app.route('/addagentin',methods=['POST', 'GET'])
def addagentin():
      
      if request.method =='POST':
             try:
               aid = request.form['agent']
               cid = request.form['cid']
               sql=f"UPDATE COMPLAINT SET AGENT='{escape(aid)}'WHERE COMPLAINT_ID='{escape(cid)}';"
               ibm_db.exec_immediate(conn, sql)
             except:
               flash("Error in Insertion operation", "danger")
             finally:
               flash("Agent Assigned Successfully")
               return redirect(url_for('assignagent'))
      

@app.route('/logadmin',methods=['POST', 'GET'])
def logadmin():
      if request.method == 'POST':
             try:
              id = request.form['name']
              password = request.form['password']
              if id==admin and password=="admin":
                    return render_template('adminhome.html')
             except:
              flash("Error in Insertion operation", "danger")
             finally:
              flash("Admin login Successfully")
              return render_template('adminhome.html') 
                    

      

@app.route('/admin')
def admin():
       return render_template('adminlog.html')   


@app.route('/userlogin')
def userlogin():
      
      return render_template('userlogin1.html')


@app.route('/addcomplaint', methods=['POST', 'GET'])
def addcomplaint():
       if request.method =='POST':
             try:
               cus= request.form['customer']
               complaint= request.form['complaint']
               detail= request.form['detail']
               sql1=f"SELECT COUNT(complaint)FROM complaint";
               f=ibm_db.exec_immediate(conn, sql1)
               data = ibm_db.fetch_both(f)
               s="COMP#220"+str(data[0]+1)
               sql=f"INSERT INTO complaint (complaint_id,customer_name,complaint,complaint_detail,agent,solution,status)VALUES ('{escape(s)}','{escape(cus)}','{escape(complaint)}', '{escape(detail)}', 'Pending...','Pending...','no');"
               ibm_db.exec_immediate(conn, sql)
             except:
               flash("Error in Insertion operation", "danger")
             finally:
               flash('Complaint successfully registered')
               return redirect(url_for('userhome',name=cus))
       



@app.route('/adduser', methods=['POST', 'GET'])
def adduser():
       if request.method =='POST':
             try:
               name= request.form['name']
               mail= request.form['mail']
               password= request.form['password']
               sql=f"INSERT INTO users (name,email, password)VALUES ('{escape(name)}', '{escape(mail)}', '{escape(password)}');"
               ibm_db.exec_immediate(conn, sql)
               
             except:
               flash("Error in Insertion operation", "danger")
             finally:
               flash('User Added Successfully')
               return redirect(url_for('userhome',name=name))
               
@app.route('/loguser', methods=['POST', 'GET'])
def loguser():
       if request.method == 'POST':
            try:
              id = request.form['name']
              password = request.form['password']

              sql = f"select * from users where name='{escape(id)}' and password='{escape(password)}'"
              stmt = ibm_db.exec_immediate(conn, sql)
              data = ibm_db.fetch_both(stmt)
              print(data)
              if data:
                session["name"] = escape(id)
                session["password"] = escape(password)
            
                flash('You were successfully logged in')
                return redirect(url_for("userhome",name=id))

              else:
                    flash("Mismatch in credetials", "danger")
            except:
              
              flash("Error in Insertion operation", "danger")

            return render_template("userlogin1.html")
               


if __name__ == '__main__':
   app.run(debug = True)