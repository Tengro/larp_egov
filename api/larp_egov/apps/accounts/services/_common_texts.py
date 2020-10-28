UNREGISTERED = "Seems like you aren't registered"
NO_ACCESS_DATA = "You have no access to this data"
NO_ACCESS_COMMAND = "You have no access to this command"
NO_USER = "No such user exists"
NO_REPORT_FOUND = "No such report found. Check report ID or assigned office of the report please"
NO_SUBSCRIPTION = "No such subscription"
NO_CORP = "No such corporation"


def validate_police(character):
    return character.is_police or character.is_security or character.is_staff


def validate_security(character):
    return character.is_security or character.is_staff
