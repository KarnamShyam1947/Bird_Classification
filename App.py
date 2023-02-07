from flask import Flask,render_template,Response, request, send_from_directory
from werkzeug.utils import secure_filename
import Recognition
import web_utils
import firebase
import os

app=Flask(__name__)
app.config['UPLOADS_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = ['.jpg', 'jpeg', '.png']

model = Recognition.load_model()

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('login.html', msg='')

@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        result = firebase.login(email, password)

        if result:
            return render_template('index.html')

        else :
            return render_template('login.html', msg = 'Invalid username/password....')

    if request.method == 'GET':
        return render_template('index.html')

    return render_template('login.html', msg='')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        result = firebase.create_user(email, password)

        if result:
            return render_template('login.html', msg = 'Account created successfully....')

        else :
            return render_template('register.html', msg = 'Email already in use.....')

    return render_template('register.html')

@app.route('/result', methods=['POST'])
def result():
    file = request.files['img']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOADS_FOLDER'], filename)

    if file:
        extension = os.path.splitext(filename)[1].lower()
        if extension in app.config['ALLOWED_EXTENSIONS']:
            file.save(filepath)

            response, result, bird_names = Recognition.detect_labels(filepath, confidence=0.6, model=model)

            if response:
                result += ' and '
                if len(bird_names) == 0:
                    result += 'image doesn\'t contain any birds'

                else:
                    result += ' The bird name(s)  : '
                    for name in bird_names:
                        result = result + name + '   '

            else :
                web_utils.log_details(result)
                return render_template('result.html', result=result, image=filename)

        else:
            result = 'Please upload an image file. Allowed extensions are .jpg, .jepg, .png'
            web_utils.log_details(result)
            return render_template('result.html', result=result, image='')

    else:
        result = 'Please select a file'
        web_utils.log_details(result)
        return render_template('result.html', result=result, image='')

    web_utils.log_details(result)
    return render_template('result.html', result=result, image='result.png')

@app.route('/gallery', methods=['GET'])
def gallery():
    images = list()

    files = os.listdir(app.config['UPLOADS_FOLDER'])
    for file in files:
        extension = os.path.splitext(file)[1].lower()

        if extension in app.config['ALLOWED_EXTENSIONS']:
            images.append(file)

    return render_template('gallery.html', images=images)

@app.route('/logs', methods=['GET'])
def logs():
    logs = list()
    with open('logs.txt', 'r') as f:
        logs.append(f.read())

    return render_template('logs.html', logs=logs)

@app.route('/video')
def video():
    return render_template('video.html')  

@app.route('/video-stream')
def video_stream():
    return Response(web_utils.generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/dispaly-image/<filename>')
def display_image(filename):
    return send_from_directory('static/uploads/',filename)

if __name__=="__main__":
    app.run(debug=True)
