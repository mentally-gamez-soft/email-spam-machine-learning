"""Define the api application."""

import os
from datetime import datetime, timedelta

import joblib
from flask import Blueprint, jsonify, request
from sklearn.feature_extraction.text import TfidfVectorizer

from core import app_env, db_mode
from core.email_spam_analyzer import EmailSpamAnalyzer
from core.services.email_classifier_database_service.factory.factory_db_service import (
    FactoryDbService,
)
from core.services.ip_address_geolocator_service.ip_address_location_service import (
    IpAddressLocationService,
)
from core.utils.databases.managers.factory.factory_db_manager import (
    FactoryDbManager,
)

urls_blueprint = Blueprint("api_urls", __name__)


@urls_blueprint.route("/", methods=["GET"])
def home2():
    """Define a test page to check the webservice is up and running at root url."""
    return "Page par defaut", 200


@urls_blueprint.route("/spam-email-refine/api/v1.0", methods=["GET"])
def home():
    """Define a test page to check the webservice is up and running at ws url."""
    return (
        (
            "Welcome to this web service\nThe aim of this service is to"
            " predict if an email could be valid or is potentially a spam."
        ),
        200,
    )


@urls_blueprint.route(
    "/spam-email-refine/api/v1.0/define-email-classification", methods=["POST"]
)
def refine_model_email():
    """Define the method to set an email as a spam or a ham."""
    payload = request.get_json(force=True)
    if "email" not in payload.keys():
        result = {"status": "ko", "message": "no email found in the payload."}
        return jsonify(result), 200

    if "classification" not in payload.keys():
        result = {
            "status": "ko",
            "message": "no email classification found in the payload.",
        }
        return jsonify(result), 200

    if (
        "ham" in payload["classification"].lower()
        or payload["classification"][0:1] == "0"
    ):
        payload["classification"] = "0"
    else:
        payload["classification"] = "1"

    email_to_analyze = payload["email"]
    email_classification = payload["classification"]
    message_status = "spam" if email_classification == "1" else "ham"
    user_ip_address = request.remote_addr

    # # ###################################################################################################
    # # #####################   MODULE FAKER TO FAKE THE IP ADDRESS ORIGIN  ###############################
    # # ###################################################################################################
    # from faker import Faker
    # from faker.providers import internet
    # fake = Faker(['es_ES'])
    # fake.add_provider(internet)
    # user_ip_address = fake.ipv4()
    # # ###################################################################################################
    # # ###################################################################################################
    # # ###################################################################################################

    ip_address_location = __get_ip_address_location(ip_address=user_ip_address)

    __record_email_in_database(
        message_status=message_status,
        ip_address_location=ip_address_location,
        email_to_analyze=email_to_analyze,
    )

    __add_email_to_csv_file(
        spam_ham_status=email_classification, email=email_to_analyze
    )

    result = {
        "status": "ok",
        "message": "your email has been added as {}".format(message_status),
    }

    return jsonify(result), 200


@urls_blueprint.route(
    "/spam-email-refine/api/v1.0/generate_model", methods=["GET"]
)
def regenerate_model():
    """Launch the training of the model with a newest dataset."""
    if __is_model_ready_for_regenerate():
        __regenerate_model()

    return jsonify({"status": "ok"}), 200


@urls_blueprint.route(
    "/spam-email-refine/api/v1.0/my_email_is_spam_or_ham", methods=["POST"]
)
def check_email():
    """Indicate if an input email is a ham or a spam."""
    payload = request.get_json(force=True)
    if "email" not in payload.keys():
        result = {"status": "ko", "message": "no email found in the payload."}
        return jsonify(result), 200

    email_to_analyze = payload["email"]
    email = [email_to_analyze]
    result = __analyze_email_with_trained_model(email=email)

    if str(result.item()) == "0":
        return (
            jsonify(
                {
                    "status": "ok",
                    "classification": "ham",
                    "email": email_to_analyze,
                }
            ),
            200,
        )
    elif str(result.item()) == "1":
        return (
            jsonify(
                {
                    "status": "ok",
                    "classification": "spam",
                    "email": email_to_analyze,
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "status": "ko",
                    "classification": (
                        "this email can not be auto-classified yet.\nHint: you"
                        " could set its classification for refining purposes"
                        ' by calling "define-email-classification"'
                    ),
                    "email": email_to_analyze,
                }
            ),
            200,
        )


def __record_email_in_database(
    message_status: str, ip_address_location: dict, email_to_analyze: str
):
    db_manager = FactoryDbManager.new_instance_db_manager(
        mode=db_mode,
        host=app_env["HOSTNAME"],
        database=app_env["DB_NAME"],
        user=app_env["DB_USER"],
        password=app_env["DB_PASSWORD"],
    )
    db_service = FactoryDbService.new_instance_service_db(
        db_manager=db_manager
    )

    if message_status == "spam":
        db_service.record_spam_email(
            ip_user=ip_address_location, email=email_to_analyze
        )
    else:
        db_service.record_ham_email(
            ip_user=ip_address_location, email=email_to_analyze
        )


def __get_ip_address_location(ip_address: str) -> dict:
    ip_address_location_service = IpAddressLocationService(
        ip_address=ip_address
    )

    is_ip_address_known = ip_address_location_service.is_known_ip_address()

    if (
        is_ip_address_known["status"]
        and is_ip_address_known["level"] != "cache"
    ):
        ip_address_location_service.set_ip_address_in_redis_cache()

    return ip_address_location_service.response


def __add_email_to_csv_file(spam_ham_status: str, email: str):
    spam_data_file = open("core/machine_learning/data/spam.csv", "a")
    spam_data_file.write('\n"' + spam_ham_status + '","' + email + '"')
    spam_data_file.close()


def __is_model_ready_for_regenerate() -> bool:
    datenow = datetime.now()
    last_model_creation_time = datetime.fromtimestamp(
        os.path.getctime(
            "core/machine_learning/ml_model_export/email_spam_detector_model.joblib"
        )
    )
    one_day = timedelta(days=1)

    return datenow - last_model_creation_time > one_day


def __regenerate_model():
    email_spam_analyzer = EmailSpamAnalyzer(
        "core/machine_learning/data/spam.csv"
    )
    email_spam_analyzer.sanitize_data()
    email_spam_analyzer.generate_model()
    email_spam_analyzer.train_model()
    email_spam_analyzer.save_model()


def __analyze_email_with_trained_model(email: list):
    SVM = joblib.load(
        "core/machine_learning/ml_model_export/email_spam_detector_model.joblib"
    )
    tf_vec = joblib.load(
        "core/machine_learning/ml_model_export/tf_vectorizer.joblib"
    )
    email_transfromed = tf_vec.transform(email)

    return SVM.predict(email_transfromed)
