from .difficulty_end import create, delete, read_all, read_one, update
from .location_end import create, delete, read_all, read_one, update
# from .locationpoint_end import 
from .owner_end import create, delete, read_all, read_one, update
from .routetype_end import create, delete, read_all, read_one, update
from .trail_end import create, delete, read_all, read_one, update
# from .trailfeature_end import create, delete, read_all, read_one, update
# from .trailfeaturejoin_end import create, delete, read_all, read_one, update

def register_routes(app):
    # Register routes for each endpoint
    app.add_url_rule('/difficulties', 'read_all_difficulties', read_all, methods=['GET'])
    app.add_url_rule('/difficulties/<int:difficulty_id>', 'read_one_difficulty', read_one, methods=['GET'])
    app.add_url_rule('/difficulties', 'create_difficulty', create, methods=['POST'])
    app.add_url_rule('/difficulties/<int:difficulty_id>', 'update_difficulty', update, methods=['PUT'])
    app.add_url_rule('/difficulties/<int:difficulty_id>', 'delete_difficulty', delete, methods=['DELETE'])

    app.add_url_rule('/locations', 'read_all_locations', read_all, methods=['GET'])
    app.add_url_rule('/locations/<int:location_id>', 'read_one_location', read_one, methods=['GET'])
    app.add_url_rule('/locations', 'create_location', create, methods=['POST'])
    app.add_url_rule('/locations/<int:location_id>', 'update_location', update, methods=['PUT'])
    app.add_url_rule('/locations/<int:location_id>', 'delete_location', delete, methods=['DELETE'])

    app.add_url_rule('/owners', 'read_all_owners', read_all, methods=['GET'])
    app.add_url_rule('/owners/<int:owner_id>', 'read_one_owner', read_one, methods=['GET'])
    app.add_url_rule('/owners', 'create_owner', create, methods=['POST'])
    app.add_url_rule('/owners/<int:owner_id>', 'update_owner', update, methods=['PUT'])
    app.add_url_rule('/owners/<int:owner_id>', 'delete_owner', delete, methods=['DELETE'])

    app.add_url_rule('/routetypes', 'read_all_routetypes', read_all, methods=['GET'])
    app.add_url_rule('/routetypes/<int:routetype_id>', 'read_one_routetype', read_one, methods=['GET'])
    app.add_url_rule('/routetypes', 'create_routetype', create, methods=['POST'])
    app.add_url_rule('/routetypes/<int:routetype_id>', 'update_routetype', update, methods=['PUT'])
    app.add_url_rule('/routetypes/<int:routetype_id>', 'delete_routetype', delete, methods=['DELETE'])

    app.add_url_rule('/trails', 'read_all_trails', read_all, methods=['GET'])
    app.add_url_rule('/trails/<int:trail_id>', 'read_one_trail', read_one, methods=['GET'])
    app.add_url_rule('/trails', 'create_trail', create, methods=['POST'])
    app.add_url_rule('/trails/<int:trail_id>', 'update_trail', update, methods=['PUT'])
    app.add_url_rule('/trails/<int:trail_id>', 'delete_trail', delete, methods=['DELETE'])

    # app.add_url_rule('/trailfeatures', 'read_all_trailfeatures', read_all, methods=['GET'])
    # app.add_url_rule('/trailfeatures/<int:trailfeature_id>', 'read_one_trailfeature', read_one, methods=['GET'])
    # app.add_url_rule('/trailfeatures', 'create_trailfeature', create, methods=['POST'])
    # app.add_url_rule('/trailfeatures/<int:trailfeature_id>', 'update_trailfeature', update, methods=['PUT'])
    # app.add_url_rule('/trailfeatures/<int:trailfeature_id>', 'delete_trailfeature', delete, methods=['DELETE'])

    # app.add_url_rule('/trailfeaturejoins', 'read_all_trailfeaturejoins', read_all, methods=['GET'])
    # app.add_url_rule('/trailfeaturejoins/<int:trailfeaturejoin_id>', 'read_one_trailfeaturejoin', read_one, methods=['GET'])
    # app.add_url_rule('/trailfeaturejoins', 'create_trailfeaturejoin', create, methods=['POST'])
    # app.add_url_rule('/trailfeaturejoins/<int:trailfeaturejoin_id>', 'update_trailfeaturejoin', update, methods=['PUT'])
    # app.add_url_rule('/trailfeaturejoins/<int:trailfeaturejoin_id>', 'delete_trailfeaturejoin', delete, methods=['DELETE'])
