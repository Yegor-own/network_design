from sqlalchemy.orm import Session, aliased
from typing import List
from geoalchemy2.functions import ST_DistanceSphere,ST_X, ST_Y