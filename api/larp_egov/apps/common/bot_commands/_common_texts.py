from django.utils.translation import ugettext_lazy as _

UNREGISTERED = _("Здається, ви не зарєєстроваані!")
NO_ACCESS_DATA = _("У вас немає доступу до цих даних")
NO_ACCESS_COMMAND = _("У вас немає доступу до цієї команди")
NO_USER = _("Такий користувач не існує у базі даних")
NO_REPORT_FOUND = _("Немає такої скарги")
NO_SUBSCRIPTION = _("Немає такої ліцензій")
NO_CORP = _("Немає такої корпорації")
NO_ACTIVE_HACK = _("Немає активного процесу зламу")
NO_CORPORATIONS = _("користувач не належить до корпорації")
NO_SUBSCRIPTIONS = _("У користувача немає підписок чи ліцензій")
HACK_TERMINATED = _("Процес зламу терміновано достроково.")


def validate_police(character):
    return character.is_police or character.is_staff


def validate_security(character):
    return character.is_security or character.is_staff
