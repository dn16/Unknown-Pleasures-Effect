# coding: UTF-8
import os
import werkzeug
# import time
import image_processing

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file, jsonify
from werkzeug import secure_filename
from PIL import Image, ImageFilter
# from tqdm import tqdm

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

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        img_file = request.files['img_file']

        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # change save file name
            splitName = filename.split('.')
            changeName = splitName[0] + '_glitch'
            splitName[0] = changeName
            splitName.insert(1, '.')
            newName = ''.join(splitName)
            
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
            contrast=image_processing.contrastPoints(x,j,img)
            print("\n", j, "/", y)
            while (l1==1):

                if len(contrast)>m:
                    if i>=contrast[m]:
                        img[i,j]=(0,0,0)
                        m=m+1

                i=i+1
                if i==(x-1):
                    contrast=image_processing.contrastPoints(x,j,img)
                    m=0
                    i=0

                    k=k+1
                    if k==1:
                        k=0

                        j=j+1
                        # print(j, "/",y)

                        if j==y:
                            l1=0
            # print(j)
            # for i in tqdm(range(j)):
            #     time.sleep(0.0005)
            source.save(os.path.join(app.config['SAVE_FOLDER'], newName), quality=100)

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
    app.run(host='127.0.0.1', port=3000, debug=True)
