from subscribe.abstracts.ISubscribe import TriggerConfig, ITrigger, ITriggerFactory


class NullTrigger(ITrigger):

    def __init__(self, config=None):
        self.__config = config

    def get_settings(self) -> dict:
        return None


class HourlyTrigger(ITrigger):

    def __init__(self, config=None):
        self.__config = config

    def get_settings(self) -> dict:
        try:
            if self.__config:
                trigger = {
                    "trigger":"interval",
                    "start_date":self.__config.start_date,
                    "hours":int(self.__config.hour),
                    "minutes":int(self.__config.minute)
                }

                return trigger

            return {}

        except Exception as e:
            raise e


class DailyTrigger(ITrigger):

    def __init__(self, config=None):
        self.__config = config

    def get_settings(self) -> dict:
        try:
            if self.__config:
                trigger = {
                    "trigger":"cron",
                    "start_date":self.__config.start_date,
                    "hour":int(self.__config.hour),
                    "minute":int(self.__config.minute),
                    "year":int(self.__config.year),
                    "month":int(self.__config.month),
                    "week":int(self.__config.week),
                    "day":int(self.__config.day)
                }

                return trigger

            return {}

        except Exception as e:
            raise e


class WeeklyTrigger(ITrigger):

    def __init__(self, config=None):
        self.__config = config

    def get_settings(self) -> dict:
        try:
            if self.__config:
                trigger = {
                    "trigger":"cron",
                    "start_date":self.__config.start_date,
                    "hour":int(self.__config.hour),
                    "minute":int(self.__config.minute),
                    "year":int(self.__config.year),
                    "month":int(self.__config.month),
                    "week":int(self.__config.week),
                    "day_of_week":int(self.__config.day_of_week),
                    "day":int(self.__config.day)
                }

                return trigger

            return {}

        except Exception as e:
            raise e


class MonthlyTrigger(ITrigger):

    def __init__(self, config=None):
        self.__config = config

    def get_settings(self) -> dict:
        try:
            if self.__config:
                trigger = {
                    "trigger":"cron",
                    "start_date":self.__config.start_date,
                    "hour":int(self.__config.hour),
                    "minute":int(self.__config.minute),
                    "year":int(self.__config.year),
                    "month":int(self.__config.month),
                    "week":int(self.__config.week),
                    "day":int(self.__config.day)
                }

                return trigger

            return {}

        except Exception as e:
            raise e


class TriggerFactory(ITriggerFactory):

    def __init__(self):
        self.HOURLY_PERIOD = "H"
        self.DAILY_PERIOD = "D"
        self.WEEKLY_PERIOD = "W"
        self.MONTHLY_PERIOD = "M"

    def get_trigger(self, subs_trigger={}) -> ITrigger:
        try:
            
            if not subs_trigger:
                return NullTrigger()

            trigger_config = TriggerConfig(**subs_trigger)
            period = subs_trigger["period"]

            if period == self.HOURLY_PERIOD:
                return HourlyTrigger(trigger_config)

            if period == self.DAILY_PERIOD:
                return DailyTrigger(trigger_config)

            if period == self.WEEKLY_PERIOD:
                return WeeklyTrigger(trigger_config)

            if period == self.MONTHLY_PERIOD:
                return MonthlyTrigger(trigger_config)

            return NullTrigger()

        except Exception as e:
            raise e