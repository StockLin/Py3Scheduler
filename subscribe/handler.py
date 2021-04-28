from uuid import uuid4
from subscribe.abstracts.ISubscribe import ISubscribeHandler
from subscribe.task import MyCustomExampleTask


"""
you can custom your function here
"""
class ExampleSubscribeHandler(ISubscribeHandler):

    def __init__(self, scheduler=None, trigger_fac=None):
        self.__scheduler = scheduler
        self.__trigger_fac = trigger_fac

    def add_task(self, data={}) -> ITask:
        try:
            new_task = MyCustomExampleTask(name=data["name"])
            return self.__scheduler.add_job(
                task_id = str(uuid4()),
                trigger = data["trigger"],
                task = new_task
            )

        except Exception as e:
            raise e

    def remove_task(self, task_ids=[]) -> list:
        try:
            if task_ids:
                removed_tasks = []
                for id in task_ids:
                    is_removed = self.__scheduler.remove_job(id)
                    removed_tasks.append({id:True} if is_removed else {id:False})

                removed_tasks

            return []

        except Exception as e:
            raise e

    def pause_task(self, task_ids=[]) -> list:
        try:
            if task_ids:
                paused_tasks = []
                for id in task_ids:
                    is_removed = self.__scheduler.pause_job(id)
                    paused_tasks.append({id:True} if is_removed else {id:False})

                paused_tasks

            return []

        except Exception as e:
            raise e

    def resume_task(self, task_ids=[]) -> list:
        try:
            if task_ids:
                resumed_tasks = []
                for id in task_ids:
                    is_removed = self.__scheduler.resume_job(id)
                    resumed_tasks.append({id:True} if is_removed else {id:False})

                resumed_tasks

            return []

        except Exception as e:
            raise e