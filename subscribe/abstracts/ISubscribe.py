import abc
from dataclasses import dataclass


@dataclass
class TriggerConfig:
    period:str
    start_date:str
    hour:int = None
    minute:int = None
    year:str = "*"
    month:str = "*"
    week:str = "*"
    day_of_week:str = None
    day:str = "*"


class ITrigger(abc.ABC):
    
    @abc.abstractmethod
    def __init__(self, config:TriggerConfig):
        raise NotImplementedError

    @abc.abstractmethod
    def get_settings(self) -> dict:
        raise NotImplementedError


class ITriggerFactory(abc.ABC):

    @abc.abstractmethod
    def get_trigger(self, subs_trigger:dict) -> ITrigger:
        raise NotImplementedError


class ITaskFileManager(abc.ABC):

    @abc.abstractmethod
    def create_task_media_dirs(self, task_id:str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_task_media_dirs(self, task_id:str) -> bool:
        raise NotImplementedError


class ITask(abc.ABC):

    @abc.abstractmethod
    def __init_(self, task_id:str):
        raise NotImplementedError

    @abc.abstractmethod
    def run(self) -> None:
        raise NotImplementedError


class ISchedulerEventListener(abc.ABC):

    @abc.abstractmethod
    def event_start(self, event):
        raise NotImplementedError

    @abc.abstractmethod
    def event_shutdown(self, event):
        raise NotImplementedError

    @abc.abstractmethod
    def event_pause(self, event):
        raise NotImplementedError

    @abc.abstractmethod
    def event_resume(self, event):
        raise NotImplementedError
    
    @abc.abstractmethod
    def event_job_submit(self, event):
        raise NotImplementedError

    @abc.abstractmethod
    def event_job_max_instances(self, event):
        raise NotImplementedError

    @abc.abstractmethod
    def event_job_execute(self, event):
        raise NotImplementedError

    @abc.abstractmethod
    def event_job_error(self, event):
        raise NotImplementedError

    @abc.abstractmethod
    def event_job_miss(self, event):
        raise NotImplementedError


@dataclass
class ScheduleConfig:
    db_host:str=""
    db_port:int=1521
    db_name:str=""
    db_user:str=""
    db_pwd:str=""
    max_workers:int=10
    tablename:str="Py3SchedulerJobs"
    timezone:str="Asia/Taipei"


class IScheduleManager(abc.ABC):

    @abc.abstractmethod
    def __init__(self, config:ScheduleConfig, event_listener:ISchedulerEventListener):
        raise NotImplementedError

    @abc.abstractmethod
    def start(self, paused:bool) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def shutdown(self, wait:bool) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def pause(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def resume(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get_state(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_job(self, id:str) -> object:
        raise NotImplementedError

    @abc.abstractmethod
    def add_job(self, task_id:str, trigger:ITrigger, task:ITask) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_job(self, id:str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def pause_job(self, id:str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def resume_job(self, id:str) -> bool:
        raise NotImplementedError


class ISubscribeHandler(abc.ABC):

    @abc.abstractmethod
    def __init__(self, scheduler:IScheduleManager, trigger_fac:ITriggerFactory):
        raise NotImplementedError

    @abc.abstractmethod
    def add_task(self, data:dict) -> ITask:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_task(self, task_ids:str) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def pause_task(self, task_ids:str) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def resume_task(self, task_ids:str) -> list:
        raise NotImplementedError