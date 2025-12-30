from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

# Load pictures data
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################
@app.route("/count")
def count():
    if data:
        return jsonify(length=len(data)), 200
    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE BY ID
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((pic for pic in data if pic["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    return jsonify({"message": "Picture not found"}), 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()  # استخرج البيانات من request body
    if not picture:
        return jsonify({"message": "No input data provided"}), 400

    # تحقق لو فيه صورة بنفس الـ id
    existing = next((pic for pic in data if pic["id"] == picture.get("id")), None)
    if existing:
        return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    # أضف الصورة الجديدة لقائمة البيانات
    data.append(picture)
    return jsonify(picture), 201
data.append({
    "id": 999,
    "pic_url": "http://dummyimage.com/230x100.png/dddddd/000000",
    "event_country": "Test Country",
    "event_state": "Test State",
    "event_city": "Test City",
    "event_date": "01/01/2030"
})


#####################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_data = request.get_json()
    if not updated_data:
        return jsonify({"message": "No input data provided"}), 400

    # البحث عن الصورة بالـ id
    picture = next((pic for pic in data if pic["id"] == id), None)
    if picture:
        # تحديث كل الحقول بالبيانات الجديدة
        picture.update(updated_data)
        return jsonify(picture), 200

    return jsonify({"message": "picture not found"}), 404
#####################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    global data
    picture = next((pic for pic in data if pic["id"] == id), None)
    if picture:
        data.remove(picture)
        return '', 204  # No Content
    return jsonify({"message": "picture not found"}), 404
