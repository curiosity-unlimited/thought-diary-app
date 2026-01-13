"""System blueprint initialization."""

from flask import Blueprint

system_bp = Blueprint('system', __name__, url_prefix='')
