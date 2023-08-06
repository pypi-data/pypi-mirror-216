import pandas as pd

from warpzone.healthchecks import HealthCheckResult, check_health_of
from warpzone.tablestorage.tables.client import WarpzoneTableClient

TABLE_STORAGE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class WarpzoneDatabaseClient:
    """Class to interact with Azure Table Storage for database queries
    (using Azure Blob Service underneath)
    """

    def __init__(self, table_client: WarpzoneTableClient):
        self._table_client = table_client

    @classmethod
    def from_connection_string(cls, conn_str: str):
        table_client = WarpzoneTableClient.from_connection_string(conn_str)
        return cls(table_client)

    def query(self, table_name: str, time_interval: pd.Interval = None):

        if time_interval:
            start_time_str = time_interval.left.strftime(TABLE_STORAGE_TIME_FORMAT)
            end_time_str = time_interval.right.strftime(TABLE_STORAGE_TIME_FORMAT)
            query = (
                f"((PartitionKey ge '{start_time_str}')"
                f" and (PartitionKey le '{end_time_str}'))"
            )
        else:
            query = ""

        records = self._table_client.query(table_name, query)

        if not records:
            return pd.DataFrame()

        df = pd.DataFrame.from_records(records)
        df = df.drop(columns=["PartitionKey", "RowKey"])

        return df

    def check_health(self) -> HealthCheckResult:
        """
        Pings the connections to the client's associated storage
        ressources in Azure.
        """

        health_check = check_health_of(self._table_client)

        return health_check
