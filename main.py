from subscribe.handler import ExampleSubscribeHandler
from subscribe.abstracts.ISubscribe import ScheduleConfig


if __name__ == "__main__":
    data = {
        "name":"HelloWorld",
        "trigger":{
            "period":"H",
            "start_date":"2021-04-28 11:11:10",
            "hour":0,
            "minute":2
        }
    }

    handler = ExampleSubscribeHandler()

    # # daily trigger example
    # "trigger":{
    #     "period":"D",
    #     "start_date":"2021-04-28 11:11:10",
    #     "hour":2,
    #     "minute":2
    # }

    # # week trigger example
    # "trigger":{
    #     "period":"W",
    #     "start_date":"2021-04-28 11:11:10",
    #     "hour":0,
    #     "minute":2,
    #     "day_of_week":"0,2,6"
    # }

    # # month trigger example
    # "trigger":{
    #     "period":"H",
    #     "start_date":"2021-04-28 11:11:10",
    #     "hour":0,
    #     "minute":2,
    #     "month":"1,2,12",
    #     "day":"10, 22, last"
    # }


import os, sys
import logging
from rpyc.utils.server import ThreadedServer
from dependency_injector.wiring import inject, Provide
from containers import Containers
from config import Config
from subscribe.abstracts.ISubscribe import IScheduleManager
from rpc_service import SubscribeRpcService


@inject
def main(scheduler:IScheduleManager=Provide[Containers.scheduler], 
        remote_service:SubscribeRpcService=Provide[Containers.remote_service]):
    
    scheduler.start()

    server = ThreadedServer(
        service=remote_service,
        port=Config.remote_rpc_port,
        protocol_config={"allow_public_attrs":True, "allow_pickle":True}
    )

if __name__ == "__main__":
    try:
        container = Containers()
        container.init_resources()
        container.config.from_dict(
            {
                "sched_config": ScheduleConfig(**{
                    "db_host": Config.db_host,
                    "db_port": Config.db_port,
                    "db_name": Config.db_name,
                    "db_user": Config.db_user,
                    "db_pwd": Config.db_pwd,
                    "max_worker": Config.max_worker,
                    "tablename": Config.tablename,
                    "timezone": Config.tablename
                })
            } 
        )

        logging.warning(f"start main service.")

        container.wire(modules=[sys.modules[__name__]])
        main(*sys.argv[1:])

    except KeyboardInterrupt:
        logging.warning("KeyboardInterrupt in main.")

    except Exception as e:
        logging.error(f"unexcepted error...... {str(e)}")
        raise e