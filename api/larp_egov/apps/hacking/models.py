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
        if not hacker.is_hacker:
            hacker.send_message("Хіба ж ти хакер?..")
            return
        if cls.objects.filter(hacker=hacker, is_active=True).exists():
            hacker.send_message("У вас уже є незавершений активний злам.")
            return
        # if hacker == target:
        #     return ValueError("You can't hack yourself!")
        ticks = BASE_HACK_TICKS - target.defence_level * DEFENCE_MULTIPLIER - init_value
        cls.objects.create(hacker=hacker, target=target, ticks_remaining=ticks)
        hacker.system_heat += HACK_HEAT_INCREASE
        hacker.send_message(f"Залишилося {ticks} доступних системних тіків до дострокової зупинки зламу і підняття тривоги. Рівень системної підозрілості: {hacker.system_heat}")
        hacker.save()
        if target.video_to_send_to_hacker:
            hacker._send_video(target.video_to_send_to_hacker)
        elif target.custom_hack_beginning_text_field:
            hacker.send_message(target.custom_hack_beginning_text_field)
        if target.is_warned_of_hack_attack:
            target.send_message("Зареєстровано хакерську атаку на ваш акаунт!!!")
            if target.is_warned_of_hacker:
                target.send_message("Дані про хакера: {data}".format(data=hacker.common_introspect_data))

    def finish_hack(self):
        ticks = self.ticks_remaining - HACKER_FINISHING_VALUE
        self.is_active = False
        self.save()
        self.hacker.send_message(f"Злам завершено")
        if ticks <= 0:
            for user in UserAccount.objects.get_security_officers():
                user.send_message(f'Зареєстровано хакерську атаку! Нападник: {self.hacker.character_id}')

    def decrease_ticks(self, value):
        self.ticks_remaining -= value
        if self.ticks_remaining <= 0:
            for user in UserAccount.objects.get_security_officers():
                user.send_message(f'Зареєстровано хакерську атаку! Нападник: {self.hacker}; жертва: {self.target}')
            self.is_active = False
            self.hacker.send_message(f'Відключення. Піднято тривогу.')
        else:
            self.hacker.send_message(f"Залишилося {self.ticks_remaining} доступних системних тіків до дострокової зупинки зламу і підняття тривоги.")
        self.save()
