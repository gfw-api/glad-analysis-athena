"""API ROUTER"""
from flask import jsonify, Blueprint, request, Response, stream_with_context
import requests

from gladAnalysis.services import custom_geom_queries
from gladAnalysis.validators import validate_geojson
from gladAnalysis.middleware import get_geojson
from gladAnalysis.errors import Error

custom_geom_endpoints = Blueprint('custom_geom_endpoints', __name__)


@custom_geom_endpoints.route('/', methods=['GET', 'POST'])
@custom_geom_endpoints.route('/use/<use_type>/<use_id>', methods=['GET'])
@custom_geom_endpoints.route('/wdpa/<wdpa_id>', methods=['GET'])
@get_geojson
@validate_geojson
def custom_stats(geojson, wdpa_id=None, use_type=None, use_id=None):

    resp = custom_geom_queries.calc_stats(geojson, request)

    return jsonify(resp)


@custom_geom_endpoints.route('/download', methods=['GET', 'POST'])
@get_geojson
@validate_geojson
def custom_download(geojson):

    # http://flask.pocoo.org/snippets/118/
    url = 'https://0kepi1kf41.execute-api.us-east-1.amazonaws.com/dev/glad-alerts/download'
    req = requests.post(url, json={"geojson": geojson}, stream=True, params=request.args.to_dict())

    return Response(stream_with_context(req.iter_content(chunk_size=1024)), content_type = req.headers['content-type'])


@custom_geom_endpoints.errorhandler(Error)
def handle_error(error):
    return error.serialize

