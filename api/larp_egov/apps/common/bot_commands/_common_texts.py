from django.utils.translation import ugettext_lazy as _

UNREGISTERED = _("Seems like you aren't registered")
NO_ACCESS_DATA = _("You have no access to this data")
NO_ACCESS_COMMAND = _("You have no access to this command")
NO_USER = _("No such user exists")
NO_REPORT_FOUND = _("No such report found. Check report ID or assigned office of the report please")
NO_SUBSCRIPTION = _("No such subscription")
NO_CORP = _("No such corporation")


def validate_police(character):
    return character.is_police or character.is_security or character.is_staff


def validate_security(character):
    return character.is_security or character.is_staff
