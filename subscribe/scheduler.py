import logging
from apscheduler.events import *
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers import SchedulerNotRunningError
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from subscribe.constants import STATE_STOPPED, STATE_RUNNING, STATE_PAUSED

from subscribe.abstracts.ISubscribe import ISchedulerEventListener, IScheduleManager


class SchedulerEventListener(ISchedulerEventListener):

    def event_start(self, event):
        logging.warn(f"Scheduler...... started!")

    def event_shutdown(self, event):
        logging.warn(f"Scheduler...... shutdown!")

    def event_pause(self, event):
        logging.warn(f"Scheduler...... paused")

    def event_resume(self, event):
        logging.warn(f"Scheduler...... resumed")
    
    def event_job_submit(self, event):
        logging.warn(f"Scheduler...... Job[{event.job_id}] was submitted!")

    def event_job_max_instances(self, event):
        pass

    def event_job_execute(self, event):
        logging.warn(f"Scheduler...... Job[{event.job_id}] was executed!")

    def event_job_error(self, event):
        logging.error(f"Scheduler...... Job[{event.job_id}] error!")

    def event_job_miss(self, event):
        logging.warn(f"Scheduler...... Job[{event.job_id}] was missed!")


class ScheduleManager(IScheduleManager):

    def __init__(self, config=None, event_listener=None):
        self.__config = config
        self.__event_listener = event_listener
        jobstores, executors, job_defaults, timezone = self.__get_apscheduler_settings()

        # initial apscheduler
        self.__scheduler = BackgroundScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults,
            timezone=timezone
        )

        if self.__event_listener:
            self.__scheduler.add_listener(self.__event_listener.event_start, EVENT_SCHEDULER_STARTED)
            self.__scheduler.add_listener(self.__event_listener.event_shutdown, EVENT_SCHEDULER_SHUTDOWN)
            self.__scheduler.add_listener(self.__event_listener.event_pause, EVENT_SCHEDULER_PAUSED)
            self.__scheduler.add_listener(self.__event_listener.event_resume, EVENT_SCHEDULER_RESUMED)
            self.__scheduler.add_listener(self.__event_listener.event_job_submit, EVENT_JOB_SUBMITTED)
            self.__scheduler.add_listener(self.__event_listener.event_job_max_instances, EVENT_JOB_MAX_INSTANCES)
            self.__scheduler.add_listener(self.__event_listener.event_job_execute, EVENT_JOB_EXECUTED)
            self.__scheduler.add_listener(self.__event_listener.event_job_error, EVENT_JOB_ERROR)
            self.__scheduler.add_listener(self.__event_listener.event_job_miss, EVENT_JOB_MISSED)

    def __get_apscheduler_settings(self):
        try:
            jobstore_url = "oracle+cx_oracle://{username}:{password}${host}:{port}/{dbname}".format(
                username=self.__config.db_user,
                password=self.__config.db_pwd,
                host=self.__config.db_host,
                port=self.__config.db_port,
                dbname=self.__config.db_name,
            )

            jobstores = {
                "default": SQLAlchemyJobStore(url=jobstore_url, tablename=self.__config.tablename)
            }

            executors = {
                "default": ThreadPoolExecutor(self.__config.max_workers),
                "processpool": ProcessPoolExecutor(2)
            }

            job_defaults = {
                "coalesce": True,
                "max_instances": 10,
                "misfire_grace_time": 30
            }

            timezone = self.__config.timezone

            return jobstores, executors, job_defaults, timezone

        except Exception as e:
            raise e

    def start(self, paused=False) -> bool:
        try:
            if self.__scheduler.state == STATE_RUNNING:
                return True

            self.__scheduler.start(paused=paused)

        except Exception as e:
            logging.error(f"scheduler start error...... {str(e)}")
            raise e

    def shutdown(self, wait=False) -> bool:
        try:
            self.__scheduler.shutdown(wait=wait)
            if self.__scheduler.state == STATE_STOPPED:
                return True

            return False

        except Exception as e:
            logging.error(f"scheduler shutdown error...... {str(e)}")
            raise e

    def pause(self) -> bool:
        try:
            self.__scheduler.pause()
            if self.__scheduler.state == STATE_PAUSED:
                return True

            return False

        except Exception as e:
            logging.error(f"scheduler pause error...... {str(e)}")
            raise e

    def resume(self) -> bool:
        try:
            self.__scheduler.resume()
            if self.__scheduler.state == STATE_RUNNING:
                return True

            return False

        except Exception as e:
            logging.error(f"scheduler resume error...... {str(e)}")
            raise e

    def get_state(self) -> str:
        try:
            if self.__scheduler.state == STATE_RUNNING:
                return "RUNNING"

            if self.__scheduler.state == STATE_PAUSED:
                return "PAUSED"

            return "STOPPED"

        except Exception as e:
            logging.error(f"scheduler get_state error...... {str(e)}")
            raise e

    def get_job(self, id="") -> object:
        try:
            job = self.__scheduler.get_job(id)
            return job

        except Exception as e:
            logging.error(f"scheduler get_job error...... {str(e)}")
            raise e

    def add_job(self, task_id="", trigger=None, task=None) -> bool:
        try:
            settings = {}
            settings["id"] = task_id
            settings["func"] = task.run
            settings["coalesce"] = True
            settings["replace_existing"] = True
            settings = {**settings, **(trigger.get_settings())}

            job = self.__scheduler.add_job(**settings)
            
            return True if self.get_job(job.id) else False

        except Exception as e:
            logging.error(f"scheduler add_job error...... {str(e)}")
            raise e

    def remove_job(self, id:str) -> bool:
        try:
            self.__scheduler.remove_job(id)
            return True if not self.get_job(id) else False

        except JobLookupError as e:
            return False

        except Exception as e:
            logging.error(f"scheduler remove_job error...... {str(e)}")
            raise e

    def pause_job(self, id:str) -> bool:
        try:
            job = self.__scheduler.pause_job(id)
            return True if job else False

        except Exception as e:
            logging.error(f"scheduler pause_job error...... {str(e)}")
            raise e

    def resume_job(self, id:str) -> bool:
        try:
            job = self.__scheduler.resume_job(id)
            return True if job else False

        except Exception as e:
            logging.error(f"scheduler resume_job error...... {str(e)}")
            raise e
