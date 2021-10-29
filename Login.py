from PyQt5 import uic, QtWidgets
import sqlite3
import re


def chama_logout_window():
    login_window.label_4.setText("")
    username = login_window.lineEdit.text()
    password = login_window.lineEdit_2.text()
    database = sqlite3.connect('database_register.db')
    cursor = database.cursor()
    try:
        cursor.execute(
            "SELECT password FROM register WHERE login ='{}'".format(username))
        password_bd = cursor.fetchall()
        database.close()
    except:
        print("erro ao validar login")

    if password == password_bd[0][0]:
        login_window.close()
        logout_window.show()
    else:
        login_window.label_4.setText("Dados de login incorretos!")


def logout():
    logout_window.close()
    login_window.show()


def open_register_window():
    register_window.show()


def register():
    username = register_window.lineEdit.text()
    email = register_window.lineEdit_5.text()
    login = register_window.lineEdit_2.text()
    password = register_window.lineEdit_3.text()
    confirm_password = register_window.lineEdit_4.text()

    if len(password) < 6 and len(password) > 12:
        register_window.label_2.setText(
            "Password must contain at least 6 characters and maximum 12 characters")
    elif re.search('[0-9]', password) is None:
        register_window.label_2.setText(
            "Password must contain at least one number")
    elif re.search('[A-Z]', password) is None:
        register_window.label_2.setText(
            "Password must contain at least one upper case")
    elif re.search('[a-z]', password) is None:
        register_window.label_2.setText(
            "Password must contain at least one lower case")
    else:
        if password == confirm_password:
            try:
                database = sqlite3.connect('database_register.db')
                cursor = database.cursor()
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS register (username text,login text,password text)")
                cursor.execute("INSERT INTO register VALUES ('" +
                               username+"','"+email+"''"+login+"','"+password+"')")

                database.commit()
                database.close()
                register_window.label_2.setText("Successful!")

            except sqlite3.Error as errors:
                print("insert error: ", errors)
        else:
            register_window.label_2.setText(" Passwords do not match!")


app = QtWidgets.QApplication([])
login_window = uic.loadUi("login_window.ui")
logout_window = uic.loadUi("logout_window.ui")
register_window = uic.loadUi("register_window.ui")
login_window.pushButton.clicked.connect(chama_logout_window)
logout_window.pushButton_2.clicked.connect(logout)
login_window.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
login_window.pushButton_2.clicked.connect(open_register_window)
register_window.pushButton_2.clicked.connect(register)


login_window.show()
app.exec()
