import postgres_client
import honeycomb_io
import pandas as pd
import datetime
import os

class HoneycombRDSClient(postgres_client.PostgresClient):
    def __init__(
        self,
        dbname=None,
        user=None,
        password=None,
        host=None,
        port=None
    ):
        super().__init__(
            dbname=os.getenv('HONEYCOMB_RDS_DATABASE') or dbname,
            user=os.getenv('HONEYCOMB_RDS_USER') or user,
            password=os.getenv('HONEYCOMB_RDS_PASSWORD') or password,
            host=os.getenv('HONEYCOMB_RDS_HOST') or host,
            port=os.getenv('HONEYCOMB_RDS_PORT') or port,
        )

    def fetch_position_data(
        self,
        start,
        end,
        device_ids=None,
        part_numbers=None,
        serial_numbers=None,
        tag_ids=None,
        names=None,
        environment_id=None,
        environment_name=None,
        connection=None,
        honeycomb_chunk_size=100,
        honeycomb_client=None,
        honeycomb_uri=None,
        honeycomb_token_uri=None,
        honeycomb_audience=None,
        honeycomb_client_id=None,
        honeycomb_client_secret=None
    ):
        device_ids = honeycomb_io.fetch_device_ids(
            device_types=['UWBTAG'],
            device_ids=device_ids,
            part_numbers=part_numbers,
            serial_numbers=serial_numbers,
            tag_ids=tag_ids,
            names=names,
            environment_id=environment_id,
            environment_name=environment_name,
            start=start,
            end=end,
            chunk_size=honeycomb_chunk_size,
            client=honeycomb_client,
            uri=honeycomb_uri,
            token_uri=honeycomb_token_uri,
            audience=honeycomb_audience,
            client_id=honeycomb_client_id,
            client_secret=honeycomb_client_secret
        )
        start_utc_naive = start.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        end_utc_naive = end.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        query_list = [
            {'fields': ['timestamp'], 'operator': 'gte', 'values': [start_utc_naive]},
            {'fields': ['timestamp'], 'operator': 'lt', 'values': [end_utc_naive]},
            {'fields': ['object'], 'operator': 'in', 'values': device_ids},
        ]
        position_data = self.select(
            table='positions',
            schema='honeycomb',
            fields=None,
            query_list=query_list,
            connection=connection,
            convert_to_dataframe=True
        )
        position_data['timestamp'] = pd.to_datetime(position_data['timestamp']).dt.tz_localize('UTC')
        position_data['x'] = pd.to_numeric(position_data['data.coordinates'].apply(lambda x: x[0]))
        position_data['y'] = pd.to_numeric(position_data['data.coordinates'].apply(lambda x: x[1]))
        position_data['z'] = pd.to_numeric(position_data['data.coordinates'].apply(lambda x: x[2]))
        position_data['anchor_count'] = pd.to_numeric(position_data['anchor_count']).astype('Int64')
        position_data['socket_read_time'] = pd.to_datetime(position_data['socket_read_time']).dt.tz_localize('UTC')
        position_data['network_time'] = pd.to_numeric(position_data['network_time']).astype('Int64')
        position_data = (
            position_data
            .rename(columns={
                'object': 'device_id',
                'coordinate_space': 'coordinate_space_id',
            })
            .reindex(columns=[
                'position_id',
                'timestamp',
                'device_id',
                'x',
                'y',
                'z',
                'quality',
                'anchor_count',
                'socket_read_time',
                'network_time',
                'coordinate_space_id',
            ])
            .set_index('position_id')
        )
        return position_data

    def fetch_accelerometer_data(
        self,
        start,
        end,
        device_ids=None,
        part_numbers=None,
        serial_numbers=None,
        tag_ids=None,
        names=None,
        environment_id=None,
        environment_name=None,
        connection=None,
        honeycomb_chunk_size=100,
        honeycomb_client=None,
        honeycomb_uri=None,
        honeycomb_token_uri=None,
        honeycomb_audience=None,
        honeycomb_client_id=None,
        honeycomb_client_secret=None
    ):
        device_ids = honeycomb_io.fetch_device_ids(
            device_types=['UWBTAG'],
            device_ids=device_ids,
            part_numbers=part_numbers,
            serial_numbers=serial_numbers,
            tag_ids=tag_ids,
            names=names,
            environment_id=environment_id,
            environment_name=environment_name,
            start=start,
            end=end,
            chunk_size=honeycomb_chunk_size,
            client=honeycomb_client,
            uri=honeycomb_uri,
            token_uri=honeycomb_token_uri,
            audience=honeycomb_audience,
            client_id=honeycomb_client_id,
            client_secret=honeycomb_client_secret
        )
        start_utc_naive = start.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        end_utc_naive = end.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        query_list = [
            {'fields': ['timestamp'], 'operator': 'gte', 'values': [start_utc_naive]},
            {'fields': ['timestamp'], 'operator': 'lt', 'values': [end_utc_naive]},
            {'fields': ['device'], 'operator': 'in', 'values': device_ids},
        ]
        accelerometer_data = self.select(
            table='accelerometer_data',
            schema='honeycomb',
            fields=None,
            query_list=query_list,
            connection=connection,
            convert_to_dataframe=True
        )
        accelerometer_data['timestamp'] = pd.to_datetime(accelerometer_data['timestamp']).dt.tz_localize('UTC')
        accelerometer_data['x'] = pd.to_numeric(accelerometer_data['data.data'].apply(lambda x: x[0]))
        accelerometer_data['y'] = pd.to_numeric(accelerometer_data['data.data'].apply(lambda x: x[1]))
        accelerometer_data['z'] = pd.to_numeric(accelerometer_data['data.data'].apply(lambda x: x[2]))
        accelerometer_data['socket_read_time'] = pd.to_datetime(accelerometer_data['socket_read_time']).dt.tz_localize('UTC')
        accelerometer_data['network_time'] = pd.to_numeric(accelerometer_data['network_time']).astype('Int64')
        accelerometer_data = (
            accelerometer_data
            .rename(columns={
                'device': 'device_id',
            })
            .reindex(columns=[
                'accelerometer_data_id',
                'timestamp',
                'device_id',
                'x',
                'y',
                'z',
                'socket_read_time',
                'network_time',
            ])
            .set_index('accelerometer_data_id')
        )
        return accelerometer_data

