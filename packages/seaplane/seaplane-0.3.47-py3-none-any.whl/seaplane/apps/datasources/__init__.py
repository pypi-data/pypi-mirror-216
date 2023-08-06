import json
import os

from ...api.sql_api import GlobalSQL
from ...configuration import config
from ...logging import log
from ...model.sql import CreatedDatabase
from .request_data_source import RequestDataSource
from .sql_executor import SqlExecutor
from ...api.api_http import headers
from ...api.api_request import provision_req
from typing import Dict, Any
from ...util import unwrap
from urllib.parse import urlparse
import requests

requests_table = """
CREATE TABLE requests (
     id VARCHAR PRIMARY KEY,
     batch_count INTEGER
);
"""

results_table = """
CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR,
    original_order INTEGER,
    output JSONB
);

ALTER SEQUENCE results_id_seq START WITH 10 INCREMENT BY 1;
CREATE INDEX idx_request_id ON results(request_id);
"""


def create_schema(database: CreatedDatabase) -> None:
    attemps = 0
    exit = False
    log.debug("Creating db schemas...")

    while attemps < 3 and not exit:
        try:
            sql = SqlExecutor.from_seaplane_database(database)

            sql.execute(requests_table)
            sql.execute(results_table)
            exit = True
        except Exception:
            attemps = attemps + 1
            log.debug(f"Create schema error attempt: {attemps}")

    if attemps == 3:
        log.debug("Error creating the default DB tables")

def get_default_db_info(tenant: str) -> Any:
    url = f"https://{urlparse(config.carrier_endpoint).netloc}/apps/kv/{tenant}/default_db"
    req = provision_req(config._token_api)

    return unwrap(
        req(
            lambda access_token: requests.get(
                url,                
                headers=headers(access_token),
            )
        )
    )

def put_database(tenant: str, created_database: CreatedDatabase) -> Any:
    url = f"https://{urlparse(config.carrier_endpoint).netloc}/apps/kv"
    req = provision_req(config._token_api)

    payload: Dict[str, str] = {
        "tenant": tenant,
        "key": "default_db",
        "value": json.dumps(created_database._asdict())
    }

    return unwrap(
        req(
            lambda access_token: requests.put(
                url,
                json=payload,
                headers=headers(access_token),
            )
        )
    )

def tenant_database(tenant: str) -> CreatedDatabase:
    default_db = get_default_db_info(tenant)
    log.debug(f"💥 DEFAULT DB: {default_db}")

    if not default_db:
        log.debug("Tenant db provisioning doesn't exist, creating .seaplane config")
        sql = GlobalSQL(config)
        new_database = sql.create_database()

        create_schema(new_database)
        put_database(tenant, new_database)        

        return new_database
    else:                
        return CreatedDatabase(**json.loads(default_db))

    if os.path.exists(".seaplane"):
        log.debug("Tenant db provisioning exists, using .seaplane config")

        with open(".seaplane", "r") as file:
            database = json.load(file)
            return CreatedDatabase(**database)
    else:
        log.debug("Tenant db provisioning doesn't exist, creating .seaplane config")
        sql = GlobalSQL(config)
        new_database = sql.create_database()

        with open(".seaplane", "w") as file:
            db_info = json.dumps(new_database._asdict())
            file.write(db_info)

        create_schema(new_database)

        return new_database


__all__ = ["RequestDataSource", "SqlExecutor", "KVStore"]
