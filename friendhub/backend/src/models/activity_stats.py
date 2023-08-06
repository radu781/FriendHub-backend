# add datetime to all relevant tables to see the day of event creation
# - posts OK
# - votes OK
# - relationships OK
# - comments
# - replies
# - stories IN POSTS
# - profile picture change OK
# - banner picture change OK
#
# each will have a different weight and the options are taken into account are displayed on profile
# different hue and saturation based on activity score
# computation is done at end of day and the result is inserted into a table
# the user can choose if they want to also include non public activity (friends only or private)
# create service that updates the values
# table columns: id | user_id | date | score


POST_WEIGHT = 20
VOTE_WEIGHT = 1
FRIEND_ADDED_WEIGHT = 3


def compute():
    ...
