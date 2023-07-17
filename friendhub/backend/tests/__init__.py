from configparser import ConfigParser
from config_keys import GH_ACTIONS

__LOCAL = "http://127.0.0.1"

LOGIN_ENDPOINT = __LOCAL + "/api/login"
REGISTER_ENDPOINT = __LOCAL + "/api/register"
LOGOUT_ENDPOINT = __LOCAL + "/api/logout"
UPLOAD_ENDPOINT = __LOCAL + "/api/upload"
ALL_POSTS_ENDPOINT = __LOCAL + "/api/post/all"
POST_ENDPOINT = __LOCAL + "/api/post"
DELETE_USER_ENDPOINT = __LOCAL + "/api/profile"
PROFILE_ENDPOINT = __LOCAL + "/api/profile"
RELATIONSHIP_ENDPOINT = __LOCAL + "/api/relationship"
SEARCH_ENDPOINT = __LOCAL + "/api/search"
STATS_ENDPOINT = __LOCAL + "/api/stats"

# github action only
USER_EMAIL = ""
USER_PASSWORD = ""
USER_FIRST_NAME = ""
USER_MIDDLE_NAME = ""
USER_LAST_NAME = ""
USER_COUNTRY = ""
USER_CITY = ""
USER_EDUCATION = ""
USER_EXTRA = ""

if not GH_ACTIONS:
    ini_file = ConfigParser()
    ini_file.read("friendhub/backend/config/testing.ini")

    LOCAL = "http://127.0.0.1"
    HOST = ini_file.get("url", "host") if ini_file.get("deploy", "active") == "1" else LOCAL

    USER_EMAIL = ini_file.get("mock_user", "email")
    USER_PASSWORD = ini_file.get("mock_user", "password")
    USER_FIRST_NAME = ini_file.get("mock_user", "first_name")
    USER_MIDDLE_NAME = ini_file.get("mock_user", "middle_name")
    USER_LAST_NAME = ini_file.get("mock_user", "last_name")
    USER_COUNTRY = ini_file.get("mock_user", "country")
    USER_CITY = ini_file.get("mock_user", "city")
    USER_EDUCATION = ini_file.get("mock_user", "education")
    USER_EXTRA = ini_file.get("mock_user", "extra")
