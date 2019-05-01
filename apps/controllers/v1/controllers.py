# -*- coding: utf-8 -*-
from flask import Blueprint

from apps.common.response import ok

app = Blueprint('v1', __name__)


@app.route('/', methods=['get'])
def main():
    return ok()
