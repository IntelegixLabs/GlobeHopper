import logging
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import abort, Blueprint, jsonify, request, Response
from flask_api import status

from .hotel_utils import Hotels, get_city_id

load_dotenv()

hotel_blp = Blueprint('hotel_Blueprint', __name__)


@hotel_blp.route('/search-hotels', methods=['GET', "OPTIONS"])
def get_search_hotels_api() -> Response:
    """
    Its fetch the hotels that comes from www.hotels.com
    First its try to get city id where client wants to visit (it could be any location area), then
    its build the query and then call endpoint get hotels from mentioned city
    """
    logging.info("------Fetching hotels --------")
    try:
        hotel_api = Hotels("/v2/hotels/search")
        location = request.args.get("location")
        if not location:
            return abort(422, "location argument is required")
        country = request.args.get("country", "IN")
        locale = request.args.get("locale", "en_IN")
        region_id = get_city_id(query_location=location, country=country, locale=locale).get("city_id", "792")
        check_in = datetime.now().strftime("%Y-%m-%d")
        check_out = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")

        querystring = {"region_id": region_id,
                       "locale": locale,
                       "checkin_date": check_in,
                       "sort_order": "REVIEW",
                       "adults_number": "1",
                       "domain": country,
                       "checkout_date": check_out,
                       "lodging_type": "HOTEL,HOSTEL,APART_HOTEL,BED_AND_BREAKFAST",
                       "star_rating_ids": "3,4,5",
                       "page_number": "1",
                       "available_filter": "SHOW_AVAILABLE_ONLY"
                       }
        res = hotel_api.build_request(query_params=querystring)
        if res.status_code != status.HTTP_200_OK:
            logging.error("GOTCHA!! error in /search-hotels api\n{}\n".format(res.text, res.status_code))
            return abort(status.HTTP_400_BAD_REQUEST, "There is an issue with the backend we will notify you shortly")

        def json_format_style(datas: list):
            return [{
                "image-url": data["propertyImage"]["image"]["url"],
                "name": data["name"],
                "price": data["price"]["lead"]["formatted"],
                "rating": data.get("star"),
            } for data in datas]

        return jsonify(json_format_style(datas=res.json()["properties"]), status.HTTP_200_OK)

    except Exception as err:
        return jsonify({"message": f"Module /search-hotels api - Error - {err}"}, status.HTTP_400_BAD_REQUEST)


@hotel_blp.route("/region")
def get_region_api() -> Response:
    """
    Every-city or any location has unique id, and It will fetch that id and return.
    """
    try:
        location = request.args.get("location", "Kolkata")
        country = request.args.get("country", "IN")
        locale = request.args.get("locale", "en_IN")
        return jsonify(get_city_id(query_location=location, country=country, locale=locale))
    except Exception as err:
        return jsonify({"message": f"Module /region api - Error - {err}"}, status.HTTP_400_BAD_REQUEST)
