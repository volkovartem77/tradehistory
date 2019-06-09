import json
import os

# constants
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__))) + '/'


def get_abs_path(path):
    # return '/root/thbot/' + PROJECT_DIR + path
    return PROJECT_DIR + path


def get_preferences():
    ff = open(get_abs_path('preferences.txt'), "r")
    preferences = json.loads(ff.read())
    ff.close()
    return preferences
