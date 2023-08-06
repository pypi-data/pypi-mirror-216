def extract_only_parenthesis(format):
    import re
    _number = re.findall(r'\(.*?\)', format)
    if len(_number) > 0:
        res = str(_number[0])
        res = res.replace("(", "").replace(")", "").strip()
    else:
        res = ""
    return res


def extract_only_column_text(columns):
    import re
    new_col = str(columns).lower()

    _text = re.findall(r'([a-zA-Z ]+)', new_col)
    if len(_text) > 0:
        res = _text[0]
    else:
        res = ""
    return res


def get_reformat_dtype(columns, format, convert_string=False):
    from pyspark.sql import types

    _format = str(extract_only_column_text(format)).upper()
    _format_text = str(extract_only_column_text(format)).upper()
    if str(_format).upper() == "DATE":
        _mask = "yyyy-MM-dd"
        _format = format
        _locale = "es_PE"
        _schema_type = "['date', 'null']"
        _type = types.StructField(columns, types.DateType())
        _type_string = types.StructField(columns, types.StringType())
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC(10)"
            _locale = ""
            _schema_type = "['string', 'null']"
    elif str(_format).upper() == "TIMESTAMP":
        _mask = "yyyy-MM-dd HH:mm:ss.SSSSSS"
        _format = format
        _locale = "es_PE"
        _schema_type = "['timestamp', 'null']"
        _type = types.StructField(columns, types.TimestampType())
        _type_string = types.StructField(columns, types.StringType())
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC(26)"
            _locale = ""
            _schema_type = "['string', 'null']"

    elif str(_format).upper() == "TIME":
        _mask = ""
        _format = "ALPHANUMERIC(8)"
        _locale = "PE"
        _schema_type = "['string', 'null']"
        _type = types.StructField(columns, types.StringType())
        _type_string = types.StructField(columns, types.StringType())
    elif str(_format).upper() in ("NUMERIC SHORT", "INTEGER"):
        _mask = ""
        _format = format
        _locale = ""
        _schema_type = "['null', 'int32']"
        _type = types.StructField(columns, types.IntegerType())
        _type_string = types.StructField(columns, types.StringType())
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC"
            _locale = ""
            _schema_type = "['string', 'null']"

    elif str(_format).upper().startswith("DECIMAL"):
        _parentheses = extract_only_parenthesis(format)
        _parentheses_split = str(_parentheses).split(",")
        if len(_parentheses_split) <= 1:
            _decimal_left = int(_parentheses_split[0])
            _decimal_right = 0
        else:
            _decimal_left = int(_parentheses_split[0])
            _decimal_right = int(_parentheses_split[1])

        _mask = ""
        _format = format
        _locale = ""
        _schema_type = f"['null', '{format}']"
        _type = types.StructField(columns, types.DecimalType(precision=_decimal_left, scale=_decimal_right))
        _type_string = types.StructField(columns, types.StringType())
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC"
            _locale = ""
            _schema_type = "['string', 'null']"

    else:
        _mask = ""
        _format = format
        _locale = ""
        _schema_type = "['string', 'null']"
        _type = types.StructField(columns, types.StringType())
        _type_string = types.StructField(columns, types.StringType())
        _format_text = "STRING"

    result = dict()
    result["_format"] = _format
    result["_mask"] = _mask
    result["_locale"] = _locale
    result["_type"] = _type
    result["_type_string"] = _type_string
    result["_schema_type"] = _schema_type
    result["_format_text"] = _format_text

    return result


def generate_faker(naming=None,
                   format=None,
                   parentheses=None,
                   columns_integer_default=None,
                   columns_date_default=None,
                   columns_string_default=None,
                   columns_decimal_default=None
                   ):
    from faker import Faker
    import random
    import string
    from datetime import datetime
    from dateutil.relativedelta import relativedelta

    fake = Faker()
    _fake = None
    format = str(format).upper()

    if format.startswith("INTEGER"):
        _fake = fake.pyint(min_value=0, max_value=9999)
        if naming in list(columns_integer_default.keys()):
            new_int = int(columns_integer_default[naming])
            _fake = fake.pyint(min_value=new_int, max_value=new_int)

    elif format.startswith("TIMESTAMP"):
        d2 = datetime.now()
        d1 = d2 - relativedelta(months=6)
        _fake = str(fake.date_time_between(start_date=d1, end_date=d2))
    elif format.startswith("DECIMAL"):
        _parentheses_split = str(parentheses).split(",")
        if len(_parentheses_split) <= 1:
            _decimal_left = int(_parentheses_split[0])
            _decimal_right = 0
        else:
            _decimal_left = int(_parentheses_split[0])
            _decimal_right = int(_parentheses_split[1])
        min_value_left = int("1" * (_decimal_left - _decimal_right))
        max_value_left = int("9" * (_decimal_left - _decimal_right))
        _fake = str(fake.pydecimal(left_digits=_decimal_left,
                                   right_digits=_decimal_right,
                                   positive=True,
                                   min_value=min_value_left,
                                   max_value=max_value_left))
        if naming in list(columns_decimal_default.keys()):
            new_decimal = float(columns_decimal_default[naming])
            _fake = fake.bothify(text=f'{new_decimal}')
    elif format.startswith("TIME"):
        _fake = fake.time()
    elif format.startswith("DATE"):
        if naming in list(columns_date_default.keys()):
            new_text = columns_date_default[naming]
            _fake = str(datetime.strptime(new_text, '%Y-%m-%d'))
        else:
            d2 = datetime.today()
            d1 = d2 - relativedelta(months=6)
            _fake = str(fake.date_between(start_date=d1, end_date=d2))
    elif format.startswith("STRING"):
        if naming in ("g_entific_id",):
            _fake = fake.bothify(text='PE')
        elif naming in ("gf_frequency_type", "frequency_type"):
            _fake = fake.bothify(text='?', letters='DM')
        elif naming in list(columns_string_default.keys()):
            new_text = columns_string_default[naming]
            _fake = fake.bothify(text=new_text)
        else:
            _fake = ''.join(random.choices(string.ascii_letters + string.digits, k=int(parentheses)))
    return _fake
