import os

class config(object):
    SECRET_KY = os.environ.get('SECRET_KEY') or "major_project_comp8047"