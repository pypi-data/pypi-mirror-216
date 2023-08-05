from ngdataenginterface.table import *
from ngdataenginterface.utils import *
from ngdataenginterface.process import *
import logging

# import pyspark packages
from pyspark.sql.types import *

from pyspark.sql import functions as F


def landing_to_raw(
    spark: SparkManager,
    aws_interface: AWSInterface,
    env: str,
    current_step_params,
    execution_date: datetime,
    overwrite: bool,
    kwargs: dict,
):
    print(f"Landing to Raw - Execution Date: {execution_date} \n")

    table_params = current_step_params
    read_path = handle_input_api(env, table_params["read"])
    write_path = handle_input_api(env, table_params["write"])

    read_params = PathParams.from_dict(read_path)
    write_params = PathParams.from_dict(write_path)
    meta = MetaParams(date=execution_date, overwrite=overwrite)

    read_table = Table(
        path=read_params,
        meta=meta,  # type: ignore
        aws_interface=aws_interface,  # type: ignore
        spark_manager=spark,
    )

    write_table = Table(
        path=write_params,
        meta=meta,  # type: ignore
        aws_interface=aws_interface,  # type: ignore
        spark_manager=spark,
    )

    process = Process(read=read_table, write=write_table)

    if not process.read.check_for_new_data():
        print(f"No new events found for path {process.read.path.object_path}")
        return

    # read table in landing layer to be written in raw layer
    df = process.read.read_table()

    process.write.write_table(df=df)
    return
