import os
from find_spark_job import SparkMasterJobDiscover

def main(master: str, spark_targets: str):
    
    match master:
        case "default":
            discover = SparkMasterJobDiscover(os.environ['MASTER_URL'])
     
    discover.gen_discover_file(spark_targets)


if __name__ == "__main__":


    master = os.environ['MASTER_TYPE']
    spark_targets = os.environ['SPARK_TARGETS_PATH']

    main(master, spark_targets)
