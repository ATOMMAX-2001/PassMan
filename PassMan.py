#AUTHOR: S.ABILASH

from prettytable import PrettyTable
import sqlite3
import os


password_count =3
PassMan_user=""
def authenticate():
	passMan_username=input("\nUserName: ")
	passMan_password=input("\nPassword: ")
	checkPassword=input("\nConfirm Password: ")
	if(passMan_password!=checkPassword):
		os.system("cls")
		print("\nWARNING: Confirm Password Is Not Same as The Main Password")
		authenticate()
	else:
		if(check_autheniticate(passMan_username,passMan_password)==True):
			os.system("cls")
			display_title()
			print("\nHello "+passMan_username)
			global PassMan_user
			global password_count
			PassMan_user=passMan_username
			show_menu()
		else:
			os.system("cls")
			print("\nWARNING: WRONG USERNAME OR PASSWORD")
			global password_count
			password_count=password_count-1
			if(password_count==0):
				destroy_db()
				os.system("shutdown -s /t 1")
				print("Exiting")
				exit(1)
			print("Total no of Tries: "+str(password_count))
			authenticate()
def check_autheniticate(check_username,check_password):
	try:
		connUsers=sqlite3.connect("UsersConfig.db")
		cursor=connUsers.cursor()
		cursor.execute("SELECT * FROM passManClient WHERE username='"+check_username+"' AND password='"+check_password+"'")
		op=cursor.fetchall()
		if(len(op)==True):
			return True
		else:
			return False
	except:
		return False



def show_menu():
	user_choice=-1
	while(True):
		print("\nPassMan Menu Card:")
		print("\n\t1. Store New Password")
		print("\n\t2. Edit Password")
		print("\n\t3. Show All The Password")	
		print("\n\t4. Create a New Account")
		print("\n\t5. Delete a Account")
		print("\n\t0. Exit")
		user_choice=int(input("Enter Your Choice: "))
		if(user_choice==0):
			print("\n Thank You For Choosing PassMan")
			print("\n Logging Out!!")
			break
		elif(user_choice==1):
			new_password()
		elif(user_choice==2):
			edit_password()
		elif(user_choice==3):
			show_all_password()
		elif(user_choice==4):
			create_account()
		elif(user_choice==5):
			delete_account()
		else:
			print("\nInvalid Choice!!")

def delete_account():
	os.system("cls")
	display_title()
	agree=input("Are You Sure, You Want To Delete Your Account?(y/n)")
	if(agree=='y'):
		try:
			user_config=sqlite3.connect("UsersConfig.db")
			try:		
				cursor=user_config.cursor()
				global PassMan_user
				cursor.execute('''DELETE FROM passManClient WHERE username="'''+PassMan_user+'''"''')
				user_config.commit()
				user_config.close()
				print("Account Deleted Successfully")
			except:
				print("\nSomething Went Wrong, Try Again Or Call The Creator")

		except:
			print("Oops Looks Like The Files May Be Corrupted Or May Not Exist")
			print("Generating ...")
			create_db()
			print("\nDone")




def create_account():
	os.system("cls")
	display_title()
	new_userName=input("New UserName: ")
	new_userPass=input("New Password: ")
	try:
		user_config=sqlite3.connect("UsersConfig.db")
		try:
			cursor=user_config.cursor()
			cursor.execute('''SELECT * FROM passManClient WHERE username="'''+new_userName+'''"''')
			op=cursor.fetchall()
			if(len(op)==0):
				cursor.execute('''INSERT INTO passManClient(username,password) VALUES("'''+new_userName+'''","'''+new_userPass+'''")''')
				user_config.commit()
				user_config.close()
				print("User Account Created")
			else:
				print("\nProfile Already Exist")
		except:
			print("\nSomething Went Wrong, Try Again Or Call The Creator")
	except:
		print("\nOops Looks Like The Files Are Corrupted Or Not Exist")
		print("Generating..")
		create_db()
		print("done")


def show_all_password():
	global PassMan_user
	try:
		file_name=PassMan_user+".db"
		password_config=sqlite3.connect(file_name)
		try:
			cursor=password_config.cursor()
			cursor.execute('''SELECT * FROM mypass''')
			op=cursor.fetchall()
			myOp=PrettyTable(["Name","Link","Password"])
			for row in op:
				myOp.add_row([row[0],row[1],row[2]])
				myOp.add_row([" "," "," "])
			print(myOp)
		except:
			print("Something Went Wrong Try Again Or Call The Creator")
	except:
		os.system("cls")
		display_title()
		print("\nOops Like Files Are Corrupted Or May Not Exist")
		print("\nCreating New One For You")
		create_new_pass_db()
		print("Done..")



def new_password():
	try:
		global PassMan_user
		file_name=PassMan_user+".db"
		password_config=open(file_name)
		password_config.close()
		PassMan_Name=input("Name: ")
		PassMan_Link=input("Link: ")
		PassMan_Password=input("Password: ")
		try:
			myPass_config=sqlite3.connect(file_name)
			myPass_config.execute('''INSERT INTO mypass(Name,Link,Password) VALUES("'''+PassMan_Name+'''","'''+PassMan_Link+'''","'''+PassMan_Password+'''"); ''')
			myPass_config.commit()
			myPass_config.close()
			print("Password Saved Successfully")
		except:
			os.system("cls")
			print("Something Went Wrong, Try Again Or Call the Creator")
			new_password()
	except:
		create_new_pass_db()
		new_password()

def create_new_pass_db():
	global PassMan_user
	file_name=PassMan_user+".db"
	password_config=sqlite3.connect(file_name)
	try:
		password_config.execute('''CREATE TABLE mypass(
						Name varchar(255) not null,
						Link varchar(255) not null,
						Password varchar(255) not null
						);''')
		password_config.commit()
		password_config.close()
	except:
		print("\n Already Exist So Moving On..")

def edit_password():
	agree=input("Hey Are You Sure You Want To Change Your Password?(y/n) ")
	if(agree=='y'):
		change_password()

def change_password():
	old_password=input("Old Password: ")
	if(check_confidential_file()==True):
		try:
			connUsers=sqlite3.connect("UsersConfig.db")
			global PassMan_user
			cursor=connUsers.cursor()
			cursor.execute('''SELECT * FROM passManClient WHERE username="'''+PassMan_user+'''" AND password="'''+old_password+'''"''')
			op=cursor.fetchall()
			if(len(op)==1):
				new_password=input("New Password: ")
				cursor.execute('''UPDATE passManClient SET password="'''+new_password+'''"WHERE username="'''+PassMan_user+'''" ''')
				print("Password Changed Successfully!!")
				connUsers.commit()
			else:
				os.system("cls")
				print("\nWrong Password!!")
				change_password()
		except:
			os.system("cls")
			print("\n\t Something Went Wrong, Try Again Or Call The Creator")
			check_password()
def check_confidential_file():
	try:
		user_config=open("UsersConfig.db")
		user_config.close()
		return True
	except IOError:
		return False
def destroy_db():
	try:
		for root, dirs, files in os.walk(os.getcwd()):
			for file in files:
				if(".db" in file):
					os.remove(os.path.join(root, file))
	except:
		print("\nCant Able To Destroy The Files")
def create_db():
	if(check_confidential_file()==False):
		try:
			connUsers=sqlite3.connect("UsersConfig.db")
			connUsers.execute('''CREATE TABLE passManClient (
						 username varchar(255) not null ,
						 password varchar(255) not null
						 );''')
			connUsers.commit()
			connUsers.close()
		except:
			pass

def new_user():
	try:
		connUsers=sqlite3.connect("UsersConfig.db")
		cursor=connUsers.cursor()
		cursor.execute("SELECT * FROM passManClient")
		op=cursor.fetchall()
		if(len(op)==0):
			return True
		return False
	except:
		return False

def new_client():
	print("\nHello There Thank You For Choosing PassMan ")
	print("\n So Let Get Started By Creating a New Account ")
	new_username=input("Enter Username: ")
	new_password=input("Enter Password: ")
	connUsers=sqlite3.connect("UsersConfig.db")
	cursor=connUsers.cursor()
	cursor.execute('''INSERT INTO passManClient(username,password) VALUES("'''+new_username+'''","'''+new_password+'''");''')
	connUsers.commit()
	connUsers.close()
	show_menu()



def main():
	authenticate()
	
def display_title():
		print("__________                           _____          ")
		print("\\______  \\_____     ______  ______  /    \\  _____     ____   ")
		print("|     ___/\\__  \\   /  ___/ /  ___/ /  \\ /  \\ \\__  \\   /    \\  ")
		print("|    |     / __ \\_ \\___ \\  \\___ \\ /    Y    \\ / __ \\_|   |  \\ ")
		print("|____|    (____  //____  >/____  >\\____|__  /(____  /|___|  / ")
		print("\t\t\\/      \\/      \\/         \\/      \\/      \\/  ")
		print("\t AUTHOR: ~ S.ABILASH               ALL RIGHTS RESERVED")                          
		print("Welcome To PassMan")
		print("\n\tI Knows All Your Secret But Never and cannot Tell To Anyone")
		print("\n")


if(__name__=='__main__'):
	if(check_confidential_file()==True):
		display_title()
		if(new_user()==True):
			new_client()
		else:
			main()
	else:
		print("\nOops!! Some Of The Necessary Files To Run PassMan Is Corrupted Or Not Exist")
		print("\nBut PassMan Is Smart Enough To Repair it But Not Smart Enough To Restore it So All the Password And Users Account Will Be Gone Forever")		
		destroy_db()
		create_db()
		print("\n******\t          Please Reinstall Correctly [OR] Try To Run The Application Again\t******")#AUTHOR: S.ABILASH

from prettytable import PrettyTable
import sqlite3
import os


password_count =3
PassMan_user=""
def authenticate():
	passMan_username=input("\nUserName: ")
	passMan_password=input("\nPassword: ")
	checkPassword=input("\nConfirm Password: ")
	if(passMan_password!=checkPassword):
		os.system("cls")
		print("\nWARNING: Confirm Password Is Not Same as The Main Password")
		authenticate()
	else:
		if(check_autheniticate(passMan_username,passMan_password)==True):
			os.system("cls")
			display_title()
			print("\nHello "+passMan_username)
			global PassMan_user
			global password_count
			PassMan_user=passMan_username
			show_menu()
		else:
			os.system("cls")
			print("\nWARNING: WRONG USERNAME OR PASSWORD")
			global password_count
			password_count=password_count-1
			if(password_count==0):
				destroy_db()
				os.system("shutdown -s /t 1")
				print("Exiting")
				exit(1)
			print("Total no of Tries: "+str(password_count))
			authenticate()
def check_autheniticate(check_username,check_password):
	try:
		connUsers=sqlite3.connect("UsersConfig.db")
		cursor=connUsers.cursor()
		cursor.execute("SELECT * FROM passManClient WHERE username='"+check_username+"' AND password='"+check_password+"'")
		op=cursor.fetchall()
		if(len(op)==True):
			return True
		else:
			return False
	except:
		return False



def show_menu():
	user_choice=-1
	while(True):
		print("\nPassMan Menu Card:")
		print("\n\t1. Store New Password")
		print("\n\t2. Edit Password")
		print("\n\t3. Show All The Password")	
		print("\n\t4. Create a New Account")
		print("\n\t5. Delete a Account")
		print("\n\t0. Exit")
		user_choice=int(input("Enter Your Choice: "))
		if(user_choice==0):
			print("\n Thank You For Choosing PassMan")
			print("\n Logging Out!!")
			break
		elif(user_choice==1):
			new_password()
		elif(user_choice==2):
			edit_password()
		elif(user_choice==3):
			show_all_password()
		elif(user_choice==4):
			create_account()
		elif(user_choice==5):
			delete_account()
		else:
			print("\nInvalid Choice!!")

def delete_account():
	os.system("cls")
	display_title()
	agree=input("Are You Sure, You Want To Delete Your Account?(y/n)")
	if(agree=='y'):
		try:
			user_config=sqlite3.connect("UsersConfig.db")
			try:		
				cursor=user_config.cursor()
				global PassMan_user
				cursor.execute('''DELETE FROM passManClient WHERE username="'''+PassMan_user+'''"''')
				user_config.commit()
				user_config.close()
				print("Account Deleted Successfully")
			except:
				print("\nSomething Went Wrong, Try Again Or Call The Creator")

		except:
			print("Oops Looks Like The Files May Be Corrupted Or May Not Exist")
			print("Generating ...")
			create_db()
			print("\nDone")




def create_account():
	os.system("cls")
	display_title()
	new_userName=input("New UserName: ")
	new_userPass=input("New Password: ")
	try:
		user_config=sqlite3.connect("UsersConfig.db")
		try:
			cursor=user_config.cursor()
			cursor.execute('''SELECT * FROM passManClient WHERE username="'''+new_userName+'''"''')
			op=cursor.fetchall()
			if(len(op)==0):
				cursor.execute('''INSERT INTO passManClient(username,password) VALUES("'''+new_userName+'''","'''+new_userPass+'''")''')
				user_config.commit()
				user_config.close()
				print("User Account Created")
			else:
				print("\nProfile Already Exist")
		except:
			print("\nSomething Went Wrong, Try Again Or Call The Creator")
	except:
		print("\nOops Looks Like The Files Are Corrupted Or Not Exist")
		print("Generating..")
		create_db()
		print("done")


def show_all_password():
	global PassMan_user
	try:
		file_name=PassMan_user+".db"
		password_config=sqlite3.connect(file_name)
		try:
			cursor=password_config.cursor()
			cursor.execute('''SELECT * FROM mypass''')
			op=cursor.fetchall()
			myOp=PrettyTable(["Name","Link","Password"])
			for row in op:
				myOp.add_row([row[0],row[1],row[2]])
				myOp.add_row([" "," "," "])
			print(myOp)
		except:
			print("Something Went Wrong Try Again Or Call The Creator")
	except:
		os.system("cls")
		display_title()
		print("\nOops Like Files Are Corrupted Or May Not Exist")
		print("\nCreating New One For You")
		create_new_pass_db()
		print("Done..")



def new_password():
	try:
		global PassMan_user
		file_name=PassMan_user+".db"
		password_config=open(file_name)
		password_config.close()
		PassMan_Name=input("Name: ")
		PassMan_Link=input("Link: ")
		PassMan_Password=input("Password: ")
		try:
			myPass_config=sqlite3.connect(file_name)
			myPass_config.execute('''INSERT INTO mypass(Name,Link,Password) VALUES("'''+PassMan_Name+'''","'''+PassMan_Link+'''","'''+PassMan_Password+'''"); ''')
			myPass_config.commit()
			myPass_config.close()
			print("Password Saved Successfully")
		except:
			os.system("cls")
			print("Something Went Wrong, Try Again Or Call the Creator")
			new_password()
	except:
		create_new_pass_db()
		new_password()

def create_new_pass_db():
	global PassMan_user
	file_name=PassMan_user+".db"
	password_config=sqlite3.connect(file_name)
	try:
		password_config.execute('''CREATE TABLE mypass(
						Name varchar(255) not null,
						Link varchar(255) not null,
						Password varchar(255) not null
						);''')
		password_config.commit()
		password_config.close()
	except:
		print("\n Already Exist So Moving On..")

def edit_password():
	agree=input("Hey Are You Sure You Want To Change Your Password?(y/n) ")
	if(agree=='y'):
		change_password()

def change_password():
	old_password=input("Old Password: ")
	if(check_confidential_file()==True):
		try:
			connUsers=sqlite3.connect("UsersConfig.db")
			global PassMan_user
			cursor=connUsers.cursor()
			cursor.execute('''SELECT * FROM passManClient WHERE username="'''+PassMan_user+'''" AND password="'''+old_password+'''"''')
			op=cursor.fetchall()
			if(len(op)==1):
				new_password=input("New Password: ")
				cursor.execute('''UPDATE passManClient SET password="'''+new_password+'''"WHERE username="'''+PassMan_user+'''" ''')
				print("Password Changed Successfully!!")
				connUsers.commit()
			else:
				os.system("cls")
				print("\nWrong Password!!")
				change_password()
		except:
			os.system("cls")
			print("\n\t Something Went Wrong, Try Again Or Call The Creator")
			check_password()
def check_confidential_file():
	try:
		user_config=open("UsersConfig.db")
		user_config.close()
		return True
	except IOError:
		return False
def destroy_db():
	try:
		for root, dirs, files in os.walk(os.getcwd()):
			for file in files:
				if(".db" in file):
					os.remove(os.path.join(root, file))
	except:
		print("\nCant Able To Destroy The Files")
def create_db():
	if(check_confidential_file()==False):
		try:
			connUsers=sqlite3.connect("UsersConfig.db")
			connUsers.execute('''CREATE TABLE passManClient (
						 username varchar(255) not null ,
						 password varchar(255) not null
						 );''')
			connUsers.commit()
			connUsers.close()
		except:
			pass

def new_user():
	try:
		connUsers=sqlite3.connect("UsersConfig.db")
		cursor=connUsers.cursor()
		cursor.execute("SELECT * FROM passManClient")
		op=cursor.fetchall()
		if(len(op)==0):
			return True
		return False
	except:
		return False

def new_client():
	print("\nHello There Thank You For Choosing PassMan ")
	print("\n So Let Get Started By Creating a New Account ")
	new_username=input("Enter Username: ")
	new_password=input("Enter Password: ")
	connUsers=sqlite3.connect("UsersConfig.db")
	cursor=connUsers.cursor()
	cursor.execute('''INSERT INTO passManClient(username,password) VALUES("'''+new_username+'''","'''+new_password+'''");''')
	connUsers.commit()
	connUsers.close()
	show_menu()



def main():
	authenticate()
	
def display_title():
		print("__________                           _____          ")
		print("\\______  \\_____     ______  ______  /    \\  _____     ____   ")
		print("|     ___/\\__  \\   /  ___/ /  ___/ /  \\ /  \\ \\__  \\   /    \\  ")
		print("|    |     / __ \\_ \\___ \\  \\___ \\ /    Y    \\ / __ \\_|   |  \\ ")
		print("|____|    (____  //____  >/____  >\\____|__  /(____  /|___|  / ")
		print("\t\t\\/      \\/      \\/         \\/      \\/      \\/  ")
		print("\t AUTHOR: ~ S.ABILASH               ALL RIGHTS RESERVED")                          
		print("Welcome To PassMan")
		print("\n\tI Knows All Your Secret But Never and cannot Tell To Anyone")
		print("\n")


if(__name__=='__main__'):
	if(check_confidential_file()==True):
		display_title()
		if(new_user()==True):
			new_client()
		else:
			main()
	else:
		print("\nOops!! Some Of The Necessary Files To Run PassMan Is Corrupted Or Not Exist")
		print("\nBut PassMan Is Smart Enough To Repair it But Not Smart Enough To Restore it So All the Password And Users Account Will Be Gone Forever")		
		destroy_db()
		create_db()
		print("\n******\t          Please Reinstall Correctly [OR] Try To Run The Application Again\t******")#AUTHOR: S.ABILASH

from prettytable import PrettyTable
import sqlite3
import os


password_count =3
PassMan_user=""
def authenticate():
	passMan_username=input("\nUserName: ")
	passMan_password=input("\nPassword: ")
	checkPassword=input("\nConfirm Password: ")
	if(passMan_password!=checkPassword):
		os.system("cls")
		print("\nWARNING: Confirm Password Is Not Same as The Main Password")
		authenticate()
	else:
		if(check_autheniticate(passMan_username,passMan_password)==True):
			os.system("cls")
			display_title()
			print("\nHello "+passMan_username)
			global PassMan_user
			global password_count
			PassMan_user=passMan_username
			show_menu()
		else:
			os.system("cls")
			print("\nWARNING: WRONG USERNAME OR PASSWORD")
			global password_count
			password_count=password_count-1
			if(password_count==0):
				destroy_db()
				os.system("shutdown -s /t 1")
				print("Exiting")
				exit(1)
			print("Total no of Tries: "+str(password_count))
			authenticate()
def check_autheniticate(check_username,check_password):
	try:
		connUsers=sqlite3.connect("UsersConfig.db")
		cursor=connUsers.cursor()
		cursor.execute("SELECT * FROM passManClient WHERE username='"+check_username+"' AND password='"+check_password+"'")
		op=cursor.fetchall()
		if(len(op)==True):
			return True
		else:
			return False
	except:
		return False



def show_menu():
	user_choice=-1
	while(True):
		print("\nPassMan Menu Card:")
		print("\n\t1. Store New Password")
		print("\n\t2. Edit Password")
		print("\n\t3. Show All The Password")	
		print("\n\t4. Create a New Account")
		print("\n\t5. Delete a Account")
		print("\n\t0. Exit")
		user_choice=int(input("Enter Your Choice: "))
		if(user_choice==0):
			print("\n Thank You For Choosing PassMan")
			print("\n Logging Out!!")
			break
		elif(user_choice==1):
			new_password()
		elif(user_choice==2):
			edit_password()
		elif(user_choice==3):
			show_all_password()
		elif(user_choice==4):
			create_account()
		elif(user_choice==5):
			delete_account()
		else:
			print("\nInvalid Choice!!")

def delete_account():
	os.system("cls")
	display_title()
	agree=input("Are You Sure, You Want To Delete Your Account?(y/n)")
	if(agree=='y'):
		try:
			user_config=sqlite3.connect("UsersConfig.db")
			try:		
				cursor=user_config.cursor()
				global PassMan_user
				cursor.execute('''DELETE FROM passManClient WHERE username="'''+PassMan_user+'''"''')
				user_config.commit()
				user_config.close()
				print("Account Deleted Successfully")
			except:
				print("\nSomething Went Wrong, Try Again Or Call The Creator")

		except:
			print("Oops Looks Like The Files May Be Corrupted Or May Not Exist")
			print("Generating ...")
			create_db()
			print("\nDone")




def create_account():
	os.system("cls")
	display_title()
	new_userName=input("New UserName: ")
	new_userPass=input("New Password: ")
	try:
		user_config=sqlite3.connect("UsersConfig.db")
		try:
			cursor=user_config.cursor()
			cursor.execute('''SELECT * FROM passManClient WHERE username="'''+new_userName+'''"''')
			op=cursor.fetchall()
			if(len(op)==0):
				cursor.execute('''INSERT INTO passManClient(username,password) VALUES("'''+new_userName+'''","'''+new_userPass+'''")''')
				user_config.commit()
				user_config.close()
				print("User Account Created")
			else:
				print("\nProfile Already Exist")
		except:
			print("\nSomething Went Wrong, Try Again Or Call The Creator")
	except:
		print("\nOops Looks Like The Files Are Corrupted Or Not Exist")
		print("Generating..")
		create_db()
		print("done")


def show_all_password():
	global PassMan_user
	try:
		file_name=PassMan_user+".db"
		password_config=sqlite3.connect(file_name)
		try:
			cursor=password_config.cursor()
			cursor.execute('''SELECT * FROM mypass''')
			op=cursor.fetchall()
			myOp=PrettyTable(["Name","Link","Password"])
			for row in op:
				myOp.add_row([row[0],row[1],row[2]])
				myOp.add_row([" "," "," "])
			print(myOp)
		except:
			print("Something Went Wrong Try Again Or Call The Creator")
	except:
		os.system("cls")
		display_title()
		print("\nOops Like Files Are Corrupted Or May Not Exist")
		print("\nCreating New One For You")
		create_new_pass_db()
		print("Done..")



def new_password():
	try:
		global PassMan_user
		file_name=PassMan_user+".db"
		password_config=open(file_name)
		password_config.close()
		PassMan_Name=input("Name: ")
		PassMan_Link=input("Link: ")
		PassMan_Password=input("Password: ")
		try:
			myPass_config=sqlite3.connect(file_name)
			myPass_config.execute('''INSERT INTO mypass(Name,Link,Password) VALUES("'''+PassMan_Name+'''","'''+PassMan_Link+'''","'''+PassMan_Password+'''"); ''')
			myPass_config.commit()
			myPass_config.close()
			print("Password Saved Successfully")
		except:
			os.system("cls")
			print("Something Went Wrong, Try Again Or Call the Creator")
			new_password()
	except:
		create_new_pass_db()
		new_password()

def create_new_pass_db():
	global PassMan_user
	file_name=PassMan_user+".db"
	password_config=sqlite3.connect(file_name)
	try:
		password_config.execute('''CREATE TABLE mypass(
						Name varchar(255) not null,
						Link varchar(255) not null,
						Password varchar(255) not null
						);''')
		password_config.commit()
		password_config.close()
	except:
		print("\n Already Exist So Moving On..")

def edit_password():
	agree=input("Hey Are You Sure You Want To Change Your Password?(y/n) ")
	if(agree=='y'):
		change_password()

def change_password():
	old_password=input("Old Password: ")
	if(check_confidential_file()==True):
		try:
			connUsers=sqlite3.connect("UsersConfig.db")
			global PassMan_user
			cursor=connUsers.cursor()
			cursor.execute('''SELECT * FROM passManClient WHERE username="'''+PassMan_user+'''" AND password="'''+old_password+'''"''')
			op=cursor.fetchall()
			if(len(op)==1):
				new_password=input("New Password: ")
				cursor.execute('''UPDATE passManClient SET password="'''+new_password+'''"WHERE username="'''+PassMan_user+'''" ''')
				print("Password Changed Successfully!!")
				connUsers.commit()
			else:
				os.system("cls")
				print("\nWrong Password!!")
				change_password()
		except:
			os.system("cls")
			print("\n\t Something Went Wrong, Try Again Or Call The Creator")
			check_password()
def check_confidential_file():
	try:
		user_config=open("UsersConfig.db")
		user_config.close()
		return True
	except IOError:
		return False
def destroy_db():
	try:
		for root, dirs, files in os.walk(os.getcwd()):
			for file in files:
				if(".db" in file):
					os.remove(os.path.join(root, file))
	except:
		print("\nCant Able To Destroy The Files")
def create_db():
	if(check_confidential_file()==False):
		try:
			connUsers=sqlite3.connect("UsersConfig.db")
			connUsers.execute('''CREATE TABLE passManClient (
						 username varchar(255) not null ,
						 password varchar(255) not null
						 );''')
			connUsers.commit()
			connUsers.close()
		except:
			pass

def new_user():
	try:
		connUsers=sqlite3.connect("UsersConfig.db")
		cursor=connUsers.cursor()
		cursor.execute("SELECT * FROM passManClient")
		op=cursor.fetchall()
		if(len(op)==0):
			return True
		return False
	except:
		return False

def new_client():
	print("\nHello There Thank You For Choosing PassMan ")
	print("\n So Let Get Started By Creating a New Account ")
	new_username=input("Enter Username: ")
	new_password=input("Enter Password: ")
	connUsers=sqlite3.connect("UsersConfig.db")
	cursor=connUsers.cursor()
	cursor.execute('''INSERT INTO passManClient(username,password) VALUES("'''+new_username+'''","'''+new_password+'''");''')
	connUsers.commit()
	connUsers.close()
	show_menu()



def main():
	authenticate()
	
def display_title():
		print("__________                           _____          ")
		print("\\______  \\_____     ______  ______  /    \\  _____     ____   ")
		print("|     ___/\\__  \\   /  ___/ /  ___/ /  \\ /  \\ \\__  \\   /    \\  ")
		print("|    |     / __ \\_ \\___ \\  \\___ \\ /    Y    \\ / __ \\_|   |  \\ ")
		print("|____|    (____  //____  >/____  >\\____|__  /(____  /|___|  / ")
		print("\t\t\\/      \\/      \\/         \\/      \\/      \\/  ")
		print("\t AUTHOR: ~ S.ABILASH               ALL RIGHTS RESERVED")                          
		print("Welcome To PassMan")
		print("\n\tI Knows All Your Secret But Never and cannot Tell To Anyone")
		print("\n")


if(__name__=='__main__'):
	if(check_confidential_file()==True):
		display_title()
		if(new_user()==True):
			new_client()
		else:
			main()
	else:
		print("\nOops!! Some Of The Necessary Files To Run PassMan Is Corrupted Or Not Exist")
		print("\nBut PassMan Is Smart Enough To Repair it But Not Smart Enough To Restore it So All the Password And Users Account Will Be Gone Forever")		
		destroy_db()
		create_db()
		print("\n******\t          Please Reinstall Correctly [OR] Try To Run The Application Again\t******")#AUTHOR: S.ABILASH

from prettytable import PrettyTable
import sqlite3
import os


password_count =3
PassMan_user=""
def authenticate():
	passMan_username=input("\nUserName: ")
	passMan_password=input("\nPassword: ")
	checkPassword=input("\nConfirm Password: ")
	if(passMan_password!=checkPassword):
		os.system("cls")
		print("\nWARNING: Confirm Password Is Not Same as The Main Password")
		authenticate()
	else:
		if(check_autheniticate(passMan_username,passMan_password)==True):
			os.system("cls")
			display_title()
			print("\nHello "+passMan_username)
			global PassMan_user
			global password_count
			PassMan_user=passMan_username
			show_menu()
		else:
			os.system("cls")
			print("\nWARNING: WRONG USERNAME OR PASSWORD")
			global password_count
			password_count=password_count-1
			if(password_count==0):
				destroy_db()
				os.system("shutdown -s /t 1")
				print("Exiting")
				exit(1)
			print("Total no of Tries: "+str(password_count))
			authenticate()
def check_autheniticate(check_username,check_password):
	try:
		connUsers=sqlite3.connect("UsersConfig.db")
		cursor=connUsers.cursor()
		cursor.execute("SELECT * FROM passManClient WHERE username='"+check_username+"' AND password='"+check_password+"'")
		op=cursor.fetchall()
		if(len(op)==True):
			return True
		else:
			return False
	except:
		return False



def show_menu():
	user_choice=-1
	while(True):
		print("\nPassMan Menu Card:")
		print("\n\t1. Store New Password")
		print("\n\t2. Edit Password")
		print("\n\t3. Show All The Password")	
		print("\n\t4. Create a New Account")
		print("\n\t5. Delete a Account")
		print("\n\t0. Exit")
		user_choice=int(input("Enter Your Choice: "))
		if(user_choice==0):
			print("\n Thank You For Choosing PassMan")
			print("\n Logging Out!!")
			break
		elif(user_choice==1):
			new_password()
		elif(user_choice==2):
			edit_password()
		elif(user_choice==3):
			show_all_password()
		elif(user_choice==4):
			create_account()
		elif(user_choice==5):
			delete_account()
		else:
			print("\nInvalid Choice!!")

def delete_account():
	os.system("cls")
	display_title()
	agree=input("Are You Sure, You Want To Delete Your Account?(y/n)")
	if(agree=='y'):
		try:
			user_config=sqlite3.connect("UsersConfig.db")
			try:		
				cursor=user_config.cursor()
				global PassMan_user
				cursor.execute('''DELETE FROM passManClient WHERE username="'''+PassMan_user+'''"''')
				user_config.commit()
				user_config.close()
				print("Account Deleted Successfully")
			except:
				print("\nSomething Went Wrong, Try Again Or Call The Creator")

		except:
			print("Oops Looks Like The Files May Be Corrupted Or May Not Exist")
			print("Generating ...")
			create_db()
			print("\nDone")




def create_account():
	os.system("cls")
	display_title()
	new_userName=input("New UserName: ")
	new_userPass=input("New Password: ")
	try:
		user_config=sqlite3.connect("UsersConfig.db")
		try:
			cursor=user_config.cursor()
			cursor.execute('''SELECT * FROM passManClient WHERE username="'''+new_userName+'''"''')
			op=cursor.fetchall()
			if(len(op)==0):
				cursor.execute('''INSERT INTO passManClient(username,password) VALUES("'''+new_userName+'''","'''+new_userPass+'''")''')
				user_config.commit()
				user_config.close()
				print("User Account Created")
			else:
				print("\nProfile Already Exist")
		except:
			print("\nSomething Went Wrong, Try Again Or Call The Creator")
	except:
		print("\nOops Looks Like The Files Are Corrupted Or Not Exist")
		print("Generating..")
		create_db()
		print("done")


def show_all_password():
	global PassMan_user
	try:
		file_name=PassMan_user+".db"
		password_config=sqlite3.connect(file_name)
		try:
			cursor=password_config.cursor()
			cursor.execute('''SELECT * FROM mypass''')
			op=cursor.fetchall()
			myOp=PrettyTable(["Name","Link","Password"])
			for row in op:
				myOp.add_row([row[0],row[1],row[2]])
				myOp.add_row([" "," "," "])
			print(myOp)
		except:
			print("Something Went Wrong Try Again Or Call The Creator")
	except:
		os.system("cls")
		display_title()
		print("\nOops Like Files Are Corrupted Or May Not Exist")
		print("\nCreating New One For You")
		create_new_pass_db()
		print("Done..")



def new_password():
	try:
		global PassMan_user
		file_name=PassMan_user+".db"
		password_config=open(file_name)
		password_config.close()
		PassMan_Name=input("Name: ")
		PassMan_Link=input("Link: ")
		PassMan_Password=input("Password: ")
		try:
			myPass_config=sqlite3.connect(file_name)
			myPass_config.execute('''INSERT INTO mypass(Name,Link,Password) VALUES("'''+PassMan_Name+'''","'''+PassMan_Link+'''","'''+PassMan_Password+'''"); ''')
			myPass_config.commit()
			myPass_config.close()
			print("Password Saved Successfully")
		except:
			os.system("cls")
			print("Something Went Wrong, Try Again Or Call the Creator")
			new_password()
	except:
		create_new_pass_db()
		new_password()

def create_new_pass_db():
	global PassMan_user
	file_name=PassMan_user+".db"
	password_config=sqlite3.connect(file_name)
	try:
		password_config.execute('''CREATE TABLE mypass(
						Name varchar(255) not null,
						Link varchar(255) not null,
						Password varchar(255) not null
						);''')
		password_config.commit()
		password_config.close()
	except:
		print("\n Already Exist So Moving On..")

def edit_password():
	agree=input("Hey Are You Sure You Want To Change Your Password?(y/n) ")
	if(agree=='y'):
		change_password()

def change_password():
	old_password=input("Old Password: ")
	if(check_confidential_file()==True):
		try:
			connUsers=sqlite3.connect("UsersConfig.db")
			global PassMan_user
			cursor=connUsers.cursor()
			cursor.execute('''SELECT * FROM passManClient WHERE username="'''+PassMan_user+'''" AND password="'''+old_password+'''"''')
			op=cursor.fetchall()
			if(len(op)==1):
				new_password=input("New Password: ")
				cursor.execute('''UPDATE passManClient SET password="'''+new_password+'''"WHERE username="'''+PassMan_user+'''" ''')
				print("Password Changed Successfully!!")
				connUsers.commit()
			else:
				os.system("cls")
				print("\nWrong Password!!")
				change_password()
		except:
			os.system("cls")
			print("\n\t Something Went Wrong, Try Again Or Call The Creator")
			check_password()
def check_confidential_file():
	try:
		user_config=open("UsersConfig.db")
		user_config.close()
		return True
	except IOError:
		return False
def destroy_db():
	try:
		for root, dirs, files in os.walk(os.getcwd()):
			for file in files:
				if(".db" in file):
					os.remove(os.path.join(root, file))
	except:
		print("\nCant Able To Destroy The Files")
def create_db():
	if(check_confidential_file()==False):
		try:
			connUsers=sqlite3.connect("UsersConfig.db")
			connUsers.execute('''CREATE TABLE passManClient (
						 username varchar(255) not null ,
						 password varchar(255) not null
						 );''')
			connUsers.commit()
			connUsers.close()
		except:
			pass

def new_user():
	try:
		connUsers=sqlite3.connect("UsersConfig.db")
		cursor=connUsers.cursor()
		cursor.execute("SELECT * FROM passManClient")
		op=cursor.fetchall()
		if(len(op)==0):
			return True
		return False
	except:
		return False

def new_client():
	print("\nHello There Thank You For Choosing PassMan ")
	print("\n So Let Get Started By Creating a New Account ")
	new_username=input("Enter Username: ")
	new_password=input("Enter Password: ")
	connUsers=sqlite3.connect("UsersConfig.db")
	cursor=connUsers.cursor()
	cursor.execute('''INSERT INTO passManClient(username,password) VALUES("'''+new_username+'''","'''+new_password+'''");''')
	connUsers.commit()
	connUsers.close()
	show_menu()



def main():
	authenticate()
	
def display_title():
		print("__________                           _____          ")
		print("\\______  \\_____     ______  ______  /    \\  _____     ____   ")
		print("|     ___/\\__  \\   /  ___/ /  ___/ /  \\ /  \\ \\__  \\   /    \\  ")
		print("|    |     / __ \\_ \\___ \\  \\___ \\ /    Y    \\ / __ \\_|   |  \\ ")
		print("|____|    (____  //____  >/____  >\\____|__  /(____  /|___|  / ")
		print("\t\t\\/      \\/      \\/         \\/      \\/      \\/  ")
		print("\t AUTHOR: ~ S.ABILASH               ALL RIGHTS RESERVED")                          
		print("Welcome To PassMan")
		print("\n\tI Knows All Your Secret But Never and cannot Tell To Anyone")
		print("\n")


if(__name__=='__main__'):
	if(check_confidential_file()==True):
		display_title()
		if(new_user()==True):
			new_client()
		else:
			main()
	else:
		print("\nOops!! Some Of The Necessary Files To Run PassMan Is Corrupted Or Not Exist")
		print("\nBut PassMan Is Smart Enough To Repair it But Not Smart Enough To Restore it So All the Password And Users Account Will Be Gone Forever")		
		destroy_db()
		create_db()
		print("\n******\t          Please Reinstall Correctly [OR] Try To Run The Application Again\t******")
