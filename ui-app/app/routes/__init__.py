from .buildings import buildings_bp
from .inspections import inspections_bp
from .interventions import interventions_bp
from .dashboard import dashboard_bp
from .prestataires import prestataires_bp
from .zones import zones_bp
from .protections import protections_bp
from .proprietaires import proprietaires_bp
from .types import types_bp
from .documents import documents_bp

__all__ = [
    'buildings_bp', 
    'inspections_bp', 
    'interventions_bp', 
    'dashboard_bp', 
    'prestataires_bp', 
    'zones_bp',
    'protections_bp',
    'proprietaires_bp',
    'types_bp',
    'documents_bp'
]