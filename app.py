from flask import *
import os,datetime
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import datetime

def restart_deployment(v1_apps, deployment, namespace):
    now = datetime.datetime.now()
    now = str(now.isoformat("T") + "Z")
    body = {
        'spec': {
            'template':{
                'metadata': {
                    'annotations': {
                        'kubectl.kubernetes.io/restartedAt': now
                    }
                }
            }
        }
    }
    try:
        v1_apps.patch_namespaced_deployment(deployment, namespace, body, pretty='true')
    except ApiException as e:
        print("Exception when calling AppsV1Api->read_namespaced_deployment_status: %s\n" % e)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html')

@app.route('/')
def index():
    return render_template("fake-login.html")


@app.route('/login',methods=['POST','GET'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'zealcomm' and password == 'zealcomm123.com':
            session['passphrase'] = 'serverisup'
            return redirect(url_for('real_login'))
        else:
            return render_template("error.html")
    else:
        return render_template("fake-login.html")

@app.route('/1231312213213/23423212123123/xowijsfjsdjfjadfa/main')
def main():
    if  not session.get('username'):
        return render_template("error.html")
    return render_template("main.html")

@app.route("/1231312213213/23423212123123/xowijsfjsdjfjadfa/logout")
def logout():
    if session.get('passphrase') != 'serverisup':
        return render_template("error.html")
    session.pop('username')
    return redirect(url_for("real_login"))

@app.route("/1231312213213/23423212123123/xowijsfjsdjfjadfa/login",methods=['POST','GET'])
def real_login():
    if session.get('passphrase') != 'serverisup':
        return render_template("error.html")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            session['username'] = username
            sess = session.get('username')
            return render_template("main.html",test='hahahahh')
        else:
            # session['passphrase'] = 'serverisup'
            return redirect(url_for('real_login'))
    else:
        return render_template("real-login.html")