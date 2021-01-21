from django.db import models
from larp_egov.apps.common.models import CoreModel
from larp_egov.apps.accounts.models import UserAccount
from larp_egov.apps.hacking.config import (
    DEFENCE_MULTIPLIER, BASE_HACK_TICKS,
    HACKER_FINISHING_VALUE, HACK_HEAT_INCREASE
)


class HackingSession(CoreModel):
    hacker = models.ForeignKey(UserAccount, related_name='hack_sessions', on_delete=models.CASCADE)
    target = models.ForeignKey(UserAccount, related_name='hack_attacks', on_delete=models.CASCADE)
    ticks_remaining = models.IntegerField()

    @classmethod
    def begin_hack(cls, hacker, target, init_value):
        if cls.objects.filter(hacker=hacker, is_active=True).exists():
            return ValueError("Another hack in progress!")
        # if hacker == target:
        #     return ValueError("You can't hack yourself!")
        ticks = BASE_HACK_TICKS - target.defence_level * DEFENCE_MULTIPLIER - init_value
        cls.objects.create(hacker=hacker, target=target, ticks_remaining=ticks)
        hacker.system_heat += HACK_HEAT_INCREASE
        hacker.send_message(f"{ticks} system ticks available for this hack before raising alert. Current total system heat: {hacker.system_heat}")
        hacker.save()

    def finish_hack(self):
        ticks = self.ticks_remaining - HACKER_FINISHING_VALUE
        self.is_active = False
        self.save()
        if ticks <= 0:
            for user in UserAccount.objects.get_security_officers():
                user.send_message(f'Hack attack registered! Attacker: {hacker.character_id}')

    def decrease_ticks(self, value):
        self.ticks_remaining -= value
        if ticks <= 0:
            for user in UserAccount.objects.get_security_officers():
                user.send_message(f'Hack attack registered! Attacker: {hacker.character_id}')
            self.is_active = False
            self.hacker.send_message(f'Connection drop. Alert raised.')
        self.hacker.send_message(f"{self.ticks_remaining} system ticks available for this hack before raising alert.")
        self.save()
