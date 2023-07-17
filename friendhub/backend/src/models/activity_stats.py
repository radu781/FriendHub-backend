# add datetime to all relevant tables to see the day of event creation
# - posts OK
# - votes
# - relationships
# - comments
# - replies
# - stories
# - profile picture change
# - banner picture change
#
# each will have a different weight and the options are taken into account are displayed on profile
# different hue and saturation based on activity score
# computation is done at end of day and the result is inserted into a table
# the user can choose if they want to also include non public activity (friends only or private)
# create service that updates the values
# table columns: id | user_id | date | score
