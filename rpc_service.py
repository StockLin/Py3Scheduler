import logging
import rpyc


class SubscribeRpcService(rpyc.Service):

    def __init__(self, scheduler=None, subscribe_handler=None):
        self.__scheduler = scheduler
        self.__subscribe_handler = subscribe_handler

    def expose_start(self):
        try:
            is_started = self.__scheduler.start()
            return {"response":is_started}

        except Exception as e:
            logging.error(f"Subscribe start error...... {str(e)}")
            return {"response":False}

    def expose_shutdown(self):
        try:
            is_shutdowned = self.__scheduler.shutdown()
            return {"response":is_shutdowned}

        except Exception as e:
            logging.error(f"Subscribe shutdown error...... {str(e)}")
            return {"response":False}

    def expose_pause(self):
        try:
            is_paused = self.__scheduler.pause()
            return {"response":is_paused}

        except Exception as e:
            logging.error(f"Subscribe pause error...... {str(e)}")
            return {"response":False}

    def expose_resume(self):
        try:
            is_resumed = self.__scheduler.resume()
            return {"response":is_resumed}

        except Exception as e:
            logging.error(f"Subscribe resume error...... {str(e)}")
            return {"response":False}

    def expose_get_state(self):
        try:
            state = self.__scheduler.get_state()
            return {"response":state}

        except Exception as e:
            logging.error(f"Subscribe get_state error...... {str(e)}")
            return {"response":None}

    def expose_add_task(self, data={}):
        try:
            task = self.__subscribe_handler.add_task(data)
            if task is not None:
                return {"response":task.id}

            return {"response":None}

        except Exception as e:
            logging.error(f"Subscribe add_task error...... {str(e)}")
            return {"response":None}

    def expose_remove_tasks(self, ids={}):
        try:
            removeds = self.__subscribe_handler.remove_task(ids)
            return {"response":removeds}

        except Exception as e:
            logging.error(f"Subscribe remove_tasks error...... {str(e)}")
            return {"response":None}

    def expose_pause_tasks(self, ids={}):
        try:
            pauseds = self.__subscribe_handler.pause_task(ids)
            return {"response":pauseds}

        except Exception as e:
            logging.error(f"Subscribe pause_tasks error...... {str(e)}")
            return {"response":None}

    def expose_resume_tasks(self, ids={}):
        try:
            resumeds = self.__subscribe_handler.resume_task(ids)
            return {"response":resumeds}

        except Exception as e:
            logging.error(f"Subscribe resume_tasks error...... {str(e)}")
            return {"response":None}