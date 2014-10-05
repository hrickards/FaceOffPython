from flask import Flask, request, jsonify, send_file
from process import process_image
from quotes import positive, negative
from werkzeug import secure_filename
import os, pyimgur

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp/faceoff'
CLIENT_ID = 'a078954f99f99de'

@app.route("/api", methods=['GET', 'POST'])
def analyse():
	image_url = request.args.get('image_url', '')
	
	if image_url == '':
		file = request.files['image']
		if not file: return {}
		
		filename = secure_filename(file.filename)
		filepath = os.path.join(UPLOAD_FOLDER, filename)
		file.save(filepath)
		image_url = "%s/image/%s" % (request.host, filename)

	data = process_image(image_url)

	return jsonify(data=data, positive=positive(data), negative=negative(data))


@app.route("/image/<filename>")
def image(filename):
	return send_file(os.path.join(UPLOAD_FOLDER, filename), mimetype='image/jpg')

if __name__ == "__main__":
	app.run(use_reloader=True, debug=True)
