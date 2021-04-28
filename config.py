import os


default_db_host = "10.1.1.2"
default_db_port = 1521
default_db_name = "dbname"
default_db_user = "mydb"
default_db_pwd = "pwd123123"

default_max_worker = 128
default_tablename = "Py3SchedulerJobs"
default_timezone = "Asia/Taipei"

defulat_remote_rpc_port = 8000


class Config:
    db_host = os.getenv('db_host') if os.getenv('db_host') else default_db_host
    db_port = os.getenv('db_port') if os.getenv('db_port') else default_db_port
    db_name = os.getenv('db_name') if os.getenv('db_name') else default_db_name
    db_user = os.getenv('db_user') if os.getenv('db_user') else default_db_user
    db_pwd = os.getenv('db_pwd') if os.getenv('db_pwd') else default_db_pwd
    max_worker = os.getenv('max_worker') if os.getenv('max_worker') else default_max_worker
    tablename = os.getenv('tablename') if os.getenv('tablename') else default_tablename
    timezone = os.getenv('timezone') if os.getenv('timezone') else default_timezone
    remote_rpc_port = os.getenv('remote_rpc_port') if os.getenv('remote_rpc_port') else defulat_remote_rpc_port