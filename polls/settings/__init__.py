# settings.py
import os
from dotenv import load_dotenv


def join_filesystem_paths(*paths):
    '''
    Combine filesystem paths.

    :return: path
    '''
    return os.path.normpath(os.path.join(*paths))


# Get current directory
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Project directory
PROJECT_ROOT = join_filesystem_paths(CURRENT_DIRECTORY, '..')

# Directory for static files (e.g. css, javascript and images files)
STATIC_ROOT = join_filesystem_paths(PROJECT_ROOT, 'static')

# Directory for media files
MEDIA_ROOT = join_filesystem_paths(PROJECT_ROOT, 'media')

# Media URL
MEDIA_URL = '/media'

# Directory for template files
TEMPLATE_ROOT = join_filesystem_paths(PROJECT_ROOT, 'templates')

# Load .env file
dotenv_path = join_filesystem_paths(PROJECT_ROOT, '../.env')
load_dotenv(dotenv_path)


AUTH_SECRET = os.environ.get(
    "AUTH_SECRET",
    "UkaRDkaypEIRUQmn7grWWUrCxykbXkvPhR1dzMdb")
TIMEZONE = os.environ.get("TIMEZONE", "Asia/Kolkata")
