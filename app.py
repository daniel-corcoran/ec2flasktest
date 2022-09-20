from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

user_db = {}

app.config['UPLOAD_FOLDER'] = 'uploads'
@app.route('/limerick', methods=['GET', 'POST'])
def process_limerick():
    if request.method == 'POST':
        # check if the post request has the file part

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
                fo = f.read()
                foriginal = fo
                invalid_char = [',', '.', ';', ':', '?', '!']
                fo = fo.lower()
                for invalid in invalid_char:
                    fo = fo.replace(invalid, '')

                f_d = {}
                for i in fo.split():
                    if i not in f_d:
                        f_d[i] = 0
                    f_d[i] += 1





            return render_template('limerick_fun.html', lim_str = foriginal, frequency=f_d)




def user_info(username):
    # TODO: Check for password in args
    user_info = user_db[username]
    return render_template("user_info.html",
                           first_name = user_info['first_name'],
                           last_name = user_info['last_name'],
                           email = user_info['email'],
                           username = username)


@app.route("/register_endpoint", methods=['POST'])
def register_endpoint():
    username = request.form.get("username")
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    if username in user_db:
        return render_template("register.html", msg="That username already exists.")
    else:
        user_db[username] = {
            'password': password,
            'first_name': first_name,
            "last_name": last_name,
            "email": email
        }
        print(user_db)
        return render_template("index.html", msg="Account created")


@app.route("/register")
def register():
    return render_template("register.html")

def check_valid_credentials(username, password):
    if username in user_db:
        if password == user_db[username]['password']:
            return {"status": True}
        else:
            return {"status": False, "err": "Invalid Password"}
    else:
        return {"status": False, 'err': "Username doesn't exist"}


@app.route("/login_endpoint", methods=['POST'])
def login_endpoint():
    username = request.form.get("username")
    password = request.form.get('password')
    value = check_valid_credentials(username, password)
    print(value)
    if value['status']:
        return user_info(username)
    else:
        return render_template("login.html", msg=value['err'])

@app.route('/login')
def login():


    return render_template("login.html")

@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
