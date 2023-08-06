def read_fields_datum(spark=None, path=None, table_name=None, storage_zone=None):
    from pyspark.sql import functions as func
    import sys
    if str(storage_zone).upper() in ('RAW', 'RAWDATA'):
        storage_zone = 'RAWDATA'
    elif str(storage_zone).upper() in ('MASTER', 'MASTERDATA'):
        storage_zone = 'MASTERDATA'
    else:
        raise Exception(f'required var storage_zone in : "raw,rawdata,master, masterdata"')
    is_windows = sys.platform.startswith('win')
    if is_windows:
        path = path.replace("\\", "/")

    df = spark.read.csv(path, sep=';', header=True)
    df = df.select(*[func.col(c).alias(c.upper().replace(' ', '_').strip()) for c in df.columns]) \
        .dropDuplicates(["FIELD_ID"])
    df = df.select("FIELD_ID", "PHYSICAL_NAME_OBJECT", "PHYSICAL_NAME_FIELD", "SOURCE_FIELD",
                   "DATA_TYPE", "KEY", "FORMAT", "LOGICAL_FORMAT", "SECURITY_CLASS", "SECURITY_LABEL",
                   "MANDATORY", "FIELD_POSITION_IN_THE_OBJECT", "STORAGE_TYPE", "STORAGE_ZONE",
                   "NAME_DATA_SYSTEM", "PARTITION_COLUMN_IND")
    df = df.withColumn('FIELD_POSITION_IN_THE_OBJECT',
                       func.format_string("%03d", func.col('FIELD_POSITION_IN_THE_OBJECT').cast('int')))
    df = df[df["STORAGE_ZONE"].isin([storage_zone])]
    df = df[df["PHYSICAL_NAME_OBJECT"] == f"{table_name}"]

    df = df.orderBy(func.col("FIELD_POSITION_IN_THE_OBJECT").asc())
    return df


def generated_dummy_table_artifactory(spark=None,
                                      path=None,
                                      sample_parquet=10,
                                      columns_integer_default={},
                                      columns_date_default={},
                                      columns_string_default={},
                                      columns_decimal_default={},
                                      ):
    global struct_list, struct_list_string
    import os
    import sys
    import pandas as pd
    import shutil
    import json
    from pyspark.sql import functions as func
    from pyspark.sql import types
    from spark_dummy_tools.utils.color import get_color_b
    from spark_dummy_tools.utils.utils import extract_only_parenthesis
    from spark_dummy_tools.utils.utils import generate_faker
    from spark_dummy_tools.utils.utils import get_reformat_dtype

    is_windows = sys.platform.startswith('win')
    spark.conf.set("spark.sql.debug.maxToStringFields", 5000)

    with open(path) as f:
        artifactory_json = json.load(f)
    table_name = artifactory_json.get("name")
    partition_colum = artifactory_json.get("partitions")

    output = list()
    for _ in range(sample_parquet):
        columns_dict = dict()
        struct_list = list()
        struct_list_string = list()
        for row in artifactory_json["fields"]:
            naming = str(row['name']).lower().strip()
            logical_format = row['logicalFormat']
            parentheses = extract_only_parenthesis(format=logical_format)
            _reformat = get_reformat_dtype(naming, logical_format, convert_string=False)
            _type = _reformat.get("_type")
            _type_string = _reformat.get("_type_string")
            _format_text = _reformat.get("_format_text")
            _fake = generate_faker(naming=naming,
                                   format=_format_text,
                                   parentheses=parentheses,
                                   columns_integer_default=columns_integer_default,
                                   columns_date_default=columns_date_default,
                                   columns_string_default=columns_string_default,
                                   columns_decimal_default=columns_decimal_default)
            columns_dict[naming] = _fake
            struct_list.append(_type)
            struct_list_string.append(_type_string)
        output.append(columns_dict)
    spark_schema = types.StructType(struct_list)
    spark_schema_string = types.StructType(struct_list_string)
    df2 = pd.DataFrame(output)
    df3 = spark.createDataFrame(df2, schema=spark_schema_string)
    for i in spark_schema.jsonValue()["fields"]:
        column_name = str(i["name"])
        column_type = str(i["type"])
        if column_type.startswith("decimal"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast(f"{column_type}"))
        elif column_type.startswith("date"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast("date"))
        elif column_type.startswith("timestamp"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast("timestamp"))

    directory_dummy = "DIRECTORY_DUMMY"
    if os.path.exists(os.path.join(directory_dummy)):
        shutil.rmtree(directory_dummy)
    path_directory = os.path.join(directory_dummy, table_name)
    if is_windows:
        path_directory = path_directory.replace("\\", "/")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)
    df3.coalesce(1).write.partitionBy(partition_colum).mode("overwrite").parquet(path_directory)

    shutil.make_archive("DIRECTORY_DUMMY", "zip", "DIRECTORY_DUMMY")
    shutil.move("DIRECTORY_DUMMY.zip", f"{path_directory}.zip")

    print(get_color_b(f'GENERATED DUMMY TABLE: {table_name}'))


def generated_dummy_table_datum(spark=None,
                                path=None,
                                table_name=None,
                                storage_zone=None,
                                sample_parquet=10,
                                partition_colum=["cutoff_date"],
                                columns_integer_default={},
                                columns_date_default={},
                                columns_string_default={},
                                columns_decimal_default={},
                                ):
    global struct_list, struct_list_string
    import os
    import sys
    import pandas as pd
    import shutil
    from pyspark.sql import functions as func
    from pyspark.sql import types
    from spark_dummy_tools.utils.color import get_color_b
    from spark_dummy_tools.utils.utils import extract_only_parenthesis
    from spark_dummy_tools.utils.utils import generate_faker
    from spark_dummy_tools.utils.utils import get_reformat_dtype

    is_windows = sys.platform.startswith('win')
    spark.conf.set("spark.sql.debug.maxToStringFields", 5000)

    df = read_fields_datum(spark=spark, path=path, table_name=table_name, storage_zone=storage_zone)
    df = df.select("PHYSICAL_NAME_OBJECT", "PHYSICAL_NAME_FIELD", "LOGICAL_FORMAT")

    output = list()
    for _ in range(sample_parquet):
        columns_dict = dict()
        struct_list = list()
        struct_list_string = list()
        for row in df.collect():
            naming = str(row['PHYSICAL_NAME_FIELD']).lower().strip()
            logical_format = row['LOGICAL_FORMAT']
            parentheses = extract_only_parenthesis(format=logical_format)
            _reformat = get_reformat_dtype(naming, logical_format, convert_string=False)
            _type = _reformat.get("_type")
            _type_string = _reformat.get("_type_string")
            _format_text = _reformat.get("_format_text")
            _fake = generate_faker(naming=naming,
                                   format=_format_text,
                                   parentheses=parentheses,
                                   columns_integer_default=columns_integer_default,
                                   columns_date_default=columns_date_default,
                                   columns_string_default=columns_string_default,
                                   columns_decimal_default=columns_decimal_default)
            columns_dict[naming] = _fake
            struct_list.append(_type)
            struct_list_string.append(_type_string)
        output.append(columns_dict)
    spark_schema = types.StructType(struct_list)
    spark_schema_string = types.StructType(struct_list_string)
    df2 = pd.DataFrame(output)
    df3 = spark.createDataFrame(df2, schema=spark_schema_string)
    for i in spark_schema.jsonValue()["fields"]:
        column_name = str(i["name"])
        column_type = str(i["type"])
        if column_type.startswith("decimal"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast(f"{column_type}"))
        elif column_type.startswith("date"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast("date"))
        elif column_type.startswith("timestamp"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast("timestamp"))

    directory_dummy = "DIRECTORY_DUMMY"
    if os.path.exists(os.path.join(directory_dummy)):
        shutil.rmtree(directory_dummy)
    path_directory = os.path.join(directory_dummy, table_name)
    if is_windows:
        path_directory = path_directory.replace("\\", "/")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)
    df3.coalesce(1).write.partitionBy(partition_colum).mode("overwrite").parquet(path_directory)

    shutil.make_archive("DIRECTORY_DUMMY", "zip", "DIRECTORY_DUMMY")
    shutil.move("DIRECTORY_DUMMY.zip", f"{path_directory}.zip")

    print(get_color_b(f'GENERATED DUMMY TABLE: {table_name}'))
