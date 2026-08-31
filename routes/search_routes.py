from flask import Blueprint, request, jsonify
from services.search_service import SearchService
from security.rbac import login_required

search_bp = Blueprint('search', __name__, url_prefix='/search')
search_service = SearchService()

@search_bp.route('/api')
@login_required
def search_api():
    query = request.args.get('q', '')
    results = search_service.global_search(query)
    return jsonify({'query': query, 'results': results})
