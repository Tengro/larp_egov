from larp_egov.apps.accounts.selectors import get_user_by_telegram_id


def get_help_message(update):
    user = get_user_by_telegram_id(update.message.chat_id)
    if not user:
        help_text = """
            Вітаємо у боті грі "Атом Людяності"! Для розблокування основих функцій гри завершіть процес реєстрації.
            Для цього залогінтеся у гру за адресою https://atomlarp.com/login/ використовуючи логін та пароль, що їх надали майстри
            Після цього на сторінці https://atomlarp.com/profile/ ви отримаєте інструкції для завершення реєстрації.

            Хорошої гри!
            Завжди ваш, TengrOS
        """
    else:
        help_text = """
            Вітаю на сторінці довідки боту. Ось основний перелік найбільш потрібних команд.
            /my_record - надає інформацію про ваш стан (банківський рахунок, рівень захисту, особисті дані)
            /corporations - надає список корпорацій, членами яких ви є
            /subscriptions - надає список підписок, ліцензій чи податків які ви сплачуєте
            /misconducts - надає список усіх скарг, поданих на вас
            /filed_misconducts - надає список усіх поданих вами скарг на інших громадян чи гостей міста

            /public_record [User ID] - надає публічну інформацію про особу з вказаним [User ID]
            /all_corporations - надає увесь список зареестрованих "корпорацій"
            /all_subscriptions - надає увесь список зареестрованих ліцензій (у т.ч. обмежених), підписок та податків
            /misconduct_types - надає увесь список типів правопорушень разом з їх кодами

            /bank_history - надає вам інформацію про вашу особисту банківську історію
            /send [User ID] [amount] [comment - опціонально, можна не залишати] - надсилає вказаному користувачу вказану кількість грошей з вашого рахунку (якщо залишити коментар - то з певним коментарем). Транзакції фіналізуються кожні 5 хвилин.
            /cancel [Transaction ID] - відміняє ще не фіналізовану транзакцію (вкажіть ідентифікатор транзакції)

            Інші команди (корпоративні, самозахист, скарги та спеціальні команди, якщо у вас є до них допуск) можна переглянути за адресою
            https://atomlarp.com/help/
        """
    return help_text
