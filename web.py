from flask import Flask, request, jsonify
from process import process_image
from quotes import positive, negative
app = Flask(__name__)

@app.route("/api")
def analyse():
	image_url = request.args.get('image_url', '')
	data = process_image(image_url)

	return jsonify(data=data, positive=positive(data), negative=negative(data))

if __name__ == "__main__":
	app.run(use_reloader=True, debug=True)
