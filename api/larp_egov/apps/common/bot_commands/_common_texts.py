from django.utils.translation import ugettext_lazy as _

UNREGISTERED = str(_("Seems like you aren't registered"))
NO_ACCESS_DATA = str(_("You have no access to this data"))
NO_ACCESS_COMMAND = str(_("You have no access to this command"))
NO_USER = str(_("No such user exists"))
NO_REPORT_FOUND = str(_("No such report found. Check report ID or assigned office of the report please"))
NO_SUBSCRIPTION = str(_("No such subscription"))
NO_CORP = str(_("No such corporation"))
NO_ACTIVE_HACK = str(_("No active hack"))


def validate_police(character):
    return character.is_police or character.is_security or character.is_staff


def validate_security(character):
    return character.is_security or character.is_staff
