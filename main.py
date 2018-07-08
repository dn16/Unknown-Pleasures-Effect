# coding: UTF-8
import os
import werkzeug

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, jsonify, send_file
from werkzeug import secure_filename
from PIL import Image, ImageFilter

app = Flask(__name__,
            static_folder = './dist/static',
            template_folder = "./dist")

UPLOAD_FOLDER = './static/image/uploads/'
SAVE_FOLDER = './static/image/save/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'gif', 'JPG', 'PNG', 'GIF'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SAVE_FOLDER'] = SAVE_FOLDER
# limit upload file size : 3MB
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


def contrastPoints(x,j,img):
    threshold=20
    contrast=[]
    i=0
    l2=1
    while l2==1:
        r1=img[i,j][0]
        b1=img[i,j][1]
        g1=img[i,j][2]
        ave1=((r1+b1+g1)/3)
        
        r2=img[(i+1),j][0]
        b2=img[(i+1),j][1]
        g2=img[(i+1),j][2]
        ave2=((r2+b2+g2)/3)

        r3=img[(i+2),j][0]
        b3=img[(i+2),j][1]
        g3=img[(i+2),j][2]
        ave3=((r3+b3+g3)/3)

        r4=img[(i+3),j][0]
        b4=img[(i+3),j][1]
        g4=img[(i+3),j][2]
        ave4=((r4+b4+g4)/3)

        if abs(ave2-ave1)>threshold:
            if abs(ave1-ave3)>(threshold/2):
                contrast.append(i)

        i=i+1		
        if i==(x-3):
            l2=0
    return contrast


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        img_file = request.files['img_file']

        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            splitName = filename.split('.')
            changeName = splitName[0] + '_glitch'
            splitName[0] = changeName
            splitName.insert(1, '.')
            newName = ''.join(splitName)
            
            # change save file name
            source = Image.open(img_file)
            img = source.load()
            print(source.format)
            print(source.size)
            print(source.mode)

            x = source.size[0]
            y = source.size[1]

            i=0
            j=0
            k=0
            l=0
            m=0
            l1=1
            contrast=contrastPoints(x,j,img)
            print("\n", j, "/", y)
            while (l1==1):

                if len(contrast)>m:
                    if i>=contrast[m]:
                        img[i,j]=(0,0,0)
                        m=m+1

                i=i+1
                if i==(x-1):
                    contrast=contrastPoints(x,j,img)
                    m=0
                    i=0

                    k=k+1
                    if k==1:
                        k=0

                        j=j+1
                        print(j, "/",y)
                        if j==y:
                            l1=0

            source.save(os.path.join(app.config['SAVE_FOLDER'], newName), quality=100)

            # return render_template('index.html')
            return newName

        else:
            return 'File extension not allowed'
    else:
        return redirect(url_for('index'))


@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def handle_over_max_file_size(error):
    print('werkzeug.exceptions.RequestEntityTooLarge')
    return 'uploaded image file size should be less than 3MB'
    

@app.route('/static/image/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/static/image/save/<filename>')
def save_file(filename):
    return send_from_directory(app.config['SAVE_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
