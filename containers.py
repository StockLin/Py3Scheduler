import os, sys
import logging.config
from dependency_injector import containers, providers
from subscribe.trigger import TriggerFactory
from subscribe.scheduler import SchedulerEventListener, ScheduleManager
from subscribe.handler import ExampleSubscribeHandler
from rpc_service import SubscribeRpcService


class Containers(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.fileConfig,
        fname=os.path.join(os.getcwd(), "logging.ini")
    )

    # declare objects initialize

    trigger_factory = providers.Factory(TriggerFactory)

    sched_event_listener = providers.Factory(SchedulerEventListener)

    scheduler = providers.Singleton(
        ScheduleManager,
        config = config.sched_config,
        event_listener = sched_event_listener
    )

    custom_handler = providers.Singleton(
        ExampleSubscribeHandler,
        scheduler = scheduler,
        trigger_fac = trigger_factory
    )

    remote_service = providers.Singleton(
        SubscribeRpcService,
        scheduler = scheduler,
        subscribe_handler = custom_handler
    )
