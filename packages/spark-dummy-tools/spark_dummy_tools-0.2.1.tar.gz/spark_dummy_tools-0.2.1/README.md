# spark_dummy_tools


[![Github License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Updates](https://pyup.io/repos/github/woctezuma/google-colab-transfer/shield.svg)](pyup)
[![Python 3](https://pyup.io/repos/github/woctezuma/google-colab-transfer/python-3-shield.svg)](pyup)
[![Code coverage](https://codecov.io/gh/woctezuma/google-colab-transfer/branch/master/graph/badge.svg)](codecov)




spark_dummy_tools is a Python library that implements for dummy table
## Installation

The code is packaged for PyPI, so that the installation consists in running:
```sh
pip install spark-dummy-tools --user 
```


## Usage

wrapper take Dummy

```sh

from spark_dummy_tools import generated_dummy_table_artifactory
from spark_dummy_tools import generated_dummy_table_datum
import spark_dataframe_tools


Generated Dummy Table Datum
============================================================
path = "fields_pe_datum2.csv"
table_name = "t_kctk_collateralization_atrb"
storage_zone = "master"
sample_parquet = 10
columns_integer_default={}
columns_date_default={"gf_cutoff_date":"2026-01-01"}
columns_string_default={}
columns_decimal_default={"other_concepts_amount":"500.00"}

generated_dummy_table_datum(spark=spark,
                            path=path,
                            table_name=table_name,
                            storage_zone=storage_zone,
                            sample_parquet=sample_parquet,
                            partition_colum=["gf_cutoff_date"],
                            columns_integer_default=columns_integer_default,
                            columns_date_default=columns_date_default,
                            columns_string_default=columns_string_default,
                            columns_decimal_default=columns_decimal_default
                           )
                       



Generated Dummy Table Artifactory
============================================================
path = "lclsupplierspurchases.output.schema"
sample_parquet = 10
columns_integer_default={}
columns_date_default={"gf_cutoff_date":"2026-01-01"}
columns_string_default={}
columns_decimal_default={"other_concepts_amount":"500.00"}


generated_dummy_table_artifactory(spark=spark,
                                  path=path,
                                  sample_parquet=sample_parquet,
                                  columns_integer_default=columns_integer_default,
                                  columns_date_default=columns_date_default,
                                  columns_string_default=columns_string_default,
                                  columns_decimal_default=columns_decimal_default
                                 )










import os, sys
is_windows = sys.platform.startswith('win')
path_directory = os.path.join("DIRECTORY_DUMMY", table_name)
if is_windows:
    path_directory = path_directory.replace("\\", "/")
    

df =  spark.read.parquet(path_directory)
df.show2(10)
  
```



## License

[Apache License 2.0](https://www.dropbox.com/s/8t6xtgk06o3ij61/LICENSE?dl=0).


## New features v1.0

 
## BugFix
- choco install visualcpp-build-tools



## Reference

 - Jonathan Quiza [github](https://github.com/jonaqp).
 - Jonathan Quiza [RumiMLSpark](http://rumi-ml.herokuapp.com/).
 - Jonathan Quiza [linkedin](https://www.linkedin.com/in/jonaqp/).
