from flask import Flask, request, jsonify, send_file
from nw import surreal_analysis
from quotes import positive, negative
from werkzeug import secure_filename
import os, pyimgur

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp/faceoff'
CLIENT_ID = 'a078954f99f99de'

@app.before_request
def option_autoreply():
    """ Always reply 200 on OPTIONS request """

    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers

        # Allow the origin which made the XHR
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        # Allow the actual method
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']
        # Allow for 10 seconds
        h['Access-Control-Max-Age'] = "10"

        # We also keep current headers
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers

        return resp


@app.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """

    h = resp.headers

    # Allow crossdomain for other HTTP Verbs
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']


    return resp

@app.route("/api/<emotion>", methods=['GET', 'POST'])
def analyse(emotion):
	image_url = request.args.get('image_url', '')
	
	if image_url == '':
		file = request.files['image']
		if not file: return {}
		
		filename = secure_filename(file.filename)
		filepath = os.path.join(UPLOAD_FOLDER, filename)
		file.save(filepath)
		image_url = "http://104.131.73.46/%s" % filename
		print image_url

	data = surreal_analysis(image_url)

	if (emotion == 'positive'): return positive(data)
	else: return negative(data)

@app.route("/image/<filename>")
def image(filename):
	return send_file(os.path.join(UPLOAD_FOLDER, filename), mimetype='image/jpg')

if __name__ == "__main__":
	app.run(use_reloader=True, debug=True, host='0.0.0.0', port=81)
