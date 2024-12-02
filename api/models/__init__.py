

from .owner import Owner, OwnerSchema
from .difficulty import Difficulty, DifficultySchema
from .routetype import RouteType, RouteTypeSchema
from .location import Location, LocationSchema
from .trail import Trail, TrailSchema
from .trailfeature import TrailFeature, TrailFeatureSchema
from .trailfeaturejoin import TrailFeatureJoin, TrailFeatureJoinSchema
from .locationpoint import LocationPoint, LocationPointSchema

from config import db, ma
