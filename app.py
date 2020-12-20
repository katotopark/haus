from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, setup_db, db_drop_and_create_all, Inhabitant, Inquiry
from util import ErrorWithCode
import json
from auth import AuthError, requires_auth
from config import auth0_config

AUTH0_DOMAIN = auth0_config["AUTH0_DOMAIN"]
ALGORITHMS = auth0_config["ALGORITHMS"]
API_AUDIENCE = auth0_config["API_AUDIENCE"]
AUTH0_CALLBACK_URL = auth0_config["AUTH0_CALLBACK_URL"]
AUTH0_CLIENT_ID = auth0_config["AUTH0_CLIENT_ID"]

app = Flask(__name__)
CORS(app)
setup_db(app)
migrate = Migrate(app, db)
# db_drop_and_create_all()


@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET, PUT, PATCH, POST, DELETE, OPTIONS"
    )
    return response


@app.route("/authorization/url", methods=["GET"])
def generate_auth_url():
    url = (
        f"https://{AUTH0_DOMAIN}/authorize"
        f"?audience={API_AUDIENCE}"
        f"&response_type=token&client_id="
        f"{AUTH0_CLIENT_ID}&redirect_uri="
        f"{AUTH0_CALLBACK_URL}"
    )
    return jsonify({"url": url})


# get inhabitants
@app.route("/inhabitants", methods=["GET"])
@requires_auth("get:inhabitants")
def get_inhabitants(f):
    try:
        inhabitants = Inhabitant.query.all()
        if len(inhabitants) < 0:
            raise ErrorWithCode(404)
        return jsonify(
            {
                "inhabitants": [inhabitant.format() for inhabitant in inhabitants],
                "success": True,
                "total_count": len(inhabitants),
            }
        )
    except ErrorWithCode as e:
        db.session.rollback()
        abort(e.code)
    finally:
        db.session.close()


# get inquiries
@app.route("/inquiries", methods=["GET"])
@requires_auth("get:inquiries")
def get_inquiries(f):
    try:
        inquiries = Inquiry.query.all()
        if len(inquiries) < 0:
            raise ErrorWithCode(404)

        return jsonify(
            {
                "inquiries": [inquiry.format() for inquiry in inquiries],
                "success": True,
                "total_count": len(inquiries),
            }
        )
    except ErrorWithCode as e:
        db.session.rollback()
        abort(e.code)
    finally:
        db.session.close()


# post new inquiry
@app.route("/inquiries", methods=["POST"])
@requires_auth("post:inquiry")
def create_inquiry(f):
    data = request.get_json()
    try:
        if not data:
            raise ErrorWithCode(400)

        new_inquiry = Inquiry(
            inquirer_id=data.get("inquirer_id"),
            items=data.get("items"),
            status="open",
            tag=data.get("tag"),
        )
        new_inquiry.insert()

        all_inquiries = Inquiry.query.all()
        if len(all_inquiries) <= 0:
            raise ErrorWithCode(500)

        return jsonify(
            {
                "inquiries": [inquiry.format() for inquiry in all_inquiries],
                "success": True,
                "total_count": len(all_inquiries),
            }
        )
    except ErrorWithCode as e:
        db.session.rollback()
        abort(e.code)
    finally:
        db.session.close()


# update inquiry status
@app.route("/inquiries/<int:id>", methods=["PATCH"])
@requires_auth("patch:inquiry")
def update_inquiry_status(f, id):
    try:
        inquiry = (
            Inquiry.query.filter(Inquiry.id == id).one_or_none()
            if id
            else ErrorWithCode(405)
        )
        if not inquiry:
            raise ErrorWithCode(404)
        else:
            inquiry.status = "active" if inquiry.status == "open" else "closed"
            inquiry.update()
        return jsonify({"inquiry": inquiry.format(), "success": True})
    except ErrorWithCode as e:
        db.session.rollback()
        abort(e.code)
    finally:
        db.session.close()


# delete inquiry
@app.route("/inquiries/<int:id>", methods=["DELETE"])
@requires_auth("delete:inquiry")
def delete_inquiry(f, id):
    try:
        inquiry = (
            Inquiry.query.filter(Inquiry.id == id).one_or_none()
            if id
            else ErrorWithCode(405)
        )
        if not inquiry:
            raise ErrorWithCode(404)
        else:
            inquiry.delete()
        all_inquiries = Inquiry.query.all()
        if len(all_inquiries) < 0:
            raise ErrorWithCode(500)
        return jsonify(
            {
                "inquiries": [inquiry.format() for inquiry in all_inquiries],
                "success": True,
                "total_count": len(all_inquiries),
            }
        )
    except ErrorWithCode as e:
        db.session.rollback()
        abort(e.code)
    finally:
        db.session.close()


@app.errorhandler(400)
def bad_request(error):
    return (
        jsonify(
            {
                "error": error.code,
                "message": "bad request",
                "success": False,
            }
        ),
        400,
    )


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify(
            {
                "error": error.code,
                "message": "resource not found",
                "success": False,
            }
        ),
        404,
    )


@app.errorhandler(405)
def not_allowed(error):
    return (
        jsonify(
            {
                "error": error.code,
                "message": "method not allowed",
                "success": False,
            }
        ),
        405,
    )


@app.errorhandler(422)
def unprocessable(error):
    return (
        jsonify({"error": error.code, "message": "unprocessable", "success": False}),
        422,
    )


@app.errorhandler(500)
def internal_server_error(error):
    return (
        jsonify(
            {
                "error": error.code,
                "message": "internal server error",
                "success": False,
            }
        ),
        500,
    )


@app.errorhandler(AuthError)
def handle_auth_error(e):
    response = jsonify(e.error)
    response.status_code = e.status_code
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)