from flask import Flask,request,url_for,redirect,render_template
import numpy as np
import sqlite3
import joblib
#from sklearn.externals import joblib
app = Flask(__name__)
app.secret_key = "happy landing@125 55023"


#############_______________############
@app.route('/')
def default():
	return render_template('landing.html')

@app.route("/signin")
def signin():
	return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        rd = validUser(request.form['Username'], request.form['Password'])
        if rd:
            return render_template('page2.html')
        else:
            return "Invalid Details"

#  Validating data in database (LOGIN)
# =====================================
def validUser(Username, Password):
	with sqlite3.connect("employee.db") as con:
		cur = con.cursor()
		cur.execute("SELECT Name,Password FROM student where Name = '%s' and Password = '%s' " % (Username, Password))
		data = cur.fetchall()
		return data
		#con.close()

##########______________############

@app.route("/register")
def register():
	return render_template("signup.html")

@app.route("/register1")
def register1():
	return render_template("signup.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		username = request.form['Username']
		password = request.form['Password']
		email    = request.form['Email']
		insertUser(username, password, email)
		return render_template('login.html')
	else:
		return render_template('login.html')
#  Insert data in database (SIGNUP)
# ==================================
def insertUser(username, password, email):
	with sqlite3.connect("employee.db") as con:
		cur = con.cursor()
		cur.execute("INSERT INTO student (Name,Password,Email) VALUES ('%s','%s','%s')" % (username, password, email))
		con.commit()
		#con.close()

##########______________############
@app.route("/contacts")
def contacts():
	return render_template("contacts.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/info")
def info():
	return render_template("about.html")

##########______________############
@app.route("/add")
def add():
	return render_template("add.html")

##########______________############

@app.route("/savedetails",methods = ["POST","GET"])
def saveDetails():
	msg = "msg"
	if request.method == "POST":
		try:
			name = request.form["name"]
			email = request.form["email"]
			with sqlite3.connect("employee.db") as con:
				cur = con.cursor()

				cur.execute("INSERT into student (name, email) values (?,?)",(name,email))

				con.commit()
				msg = " Student successfully Added "
		except:
			con.rollback()
			msg = " can not add the student to the list"
		finally:
			return render_template("success.html",msg = msg)
			con.close()

##########################################
@app.route("/update")
def update():
	return render_template('update.html')

@app.route("/updateDetails",methods = ["POST","GET"])
def updateDetails():
	msg = "msg"
	if request.method == "POST":
		try:
			id    = request.form["id"]
			name  = request.form["name"]
			email = request.form["email"]
			with sqlite3.connect("employee.db") as con:
				cur = con.cursor()
				cur.execute("update student set name=?, email=? where id=?",(name,email,id))

				con.commit()
				msg = " Student successfully Updated "
		except:
			con.rollback()
			msg = " Can't update the student to the list"
		finally:
			return render_template("success.html",msg = msg)
			con.close()
################################
@app.route("/page2")
def CRUD():
	return render_template('page2.html')
################################

@app.route("/page3")
def view():
	con = sqlite3.connect("employee.db")
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	cur.execute("select * from Student")
	rows = cur.fetchall()
	return render_template("page3.html",rows = rows)

#############______________##########

@app.route("/weatherforecasting")
def weather():
	return render_template('weather2.html')

@app.route('/predict', methods=["POST","GET"])
def predict():
	if request.method == 'POST':
		Temperature = request.form['Temperature']
		Humidity = request.form['Humidity']
		cloudcover = request.form['Cloudcover']
		Precipitationcover = request.form['Precipitation']
		sample_data = [Temperature, Humidity, cloudcover, Precipitationcover]
		clean_data = [float(i) for i in sample_data]

		ex = np.array(clean_data).reshape(1,-1)
		final_model = joblib.load('data/model.joblib')
		val = round(int(final_model.predict(ex)))

		if(val==0):
			result_prediction = 'Clear'
		elif(val==1):
			result_prediction = 'Partially Cloudy'
		elif(val==2):
			result_prediction = 'Rain,Overcast'
		elif(val==3):
			result_prediction = 'Rain,Partially Cloudy'
		elif(val==4):
			result_prediction = 'Overcast'
		elif(val==5):
			result_prediction = 'High Rain'
		return render_template('predictresult.html',prediction=result_prediction)


#############______________##########
#############______________##########
@app.route('/ml')
def ml():
	return render_template('ml.html')


@app.route('/cropprediction')
def cropprediction():
	return render_template('cropprediction.html')

#def predict():


if __name__ == "__main__":
	app.debug = True
	app.run()
