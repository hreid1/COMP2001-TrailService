from .owner import Owner, OwnerSchema
from .trailfeaturejoin import TrailFeatureJoin, TrailFeatureJoinSchema
from .difficulty import Difficulty, DifficultySchema
from .routetype import RouteType, RouteTypeSchema
from .location import Location, LocationSchema
from .trail import Trail, TrailSchema
from .trailfeature import TrailFeature, TrailFeatureSchema
from .locationpoint import LocationPoint, LocationPointSchema

from api.database.config import db, ma  # Make sure to import db and ma
