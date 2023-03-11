from flask import Flask, render_template, request, redirect
import os
app = Flask(__name__)


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    '''
    Вью функція створює файл, у який додаються значення з фласку.
    Виконуються перевірка, якщо емейл вже записаний у файл, то виконується redirect на сторінку логін.
    :return: html, перенаправлення на сторінку логін
    '''
    data_filename = 'data'
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form['password']
        if os.path.isfile(data_filename) is True:
            with open(data_filename, 'r') as fp:
                if email in fp.read():
                    return redirect('/login')

        with open(data_filename, 'a') as f:
            f.write(email + ',' + password + '\n')
    return render_template('registration.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    '''
    Вью функція перевіряє чи існує файл, якщо не існує, то виводить відповідне повідомлення.
    Виконуєтья перевірка на введені у фласку емейл і пароль, з тими даними, які записані у файл. Якщо дані збігаються
    або не збігаються, з'являється відповідне повідомлення.
    :return: html, текст
    '''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if os.path.isfile('data') is True:
            with open('data', 'r') as f:
                for line in f:
                    if email in line:
                        email_, saved_password = line.strip().split(',')
                        if saved_password == password:
                            return 'Ви в системі'
                        else:
                            return 'Не правильний емейл або пароль'
        else:
            return 'Обліковий запис не знайдено, пройдіть реєстрацію'
    return render_template('login.html')

