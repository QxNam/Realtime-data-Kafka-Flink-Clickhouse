import json, os
import logging
import clickhouse_connect

from pyflink.common import Types, WatermarkStrategy
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import (
    KafkaOffsetsInitializer,
    KafkaSource,
)

# from dotenv import load_dotenv
# load_dotenv()
# KAFKA_HOST = os.getenv("KAFKA_HOST")
# KAFKA_PORT = os.getenv("KAFKA_PORT")
# KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
# CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")

KAFKA_HOST="kafka1"
KAFKA_PORT=9092
KAFKA_TOPIC="product_dim"
CLICKHOUSE_HOST="clickhouse-server"
CLICKHOUSE_DATABASE="olap"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def initialize_env() -> StreamExecutionEnvironment:
    """Makes stream execution environment initialization"""
    env = StreamExecutionEnvironment.get_execution_environment()

    # Get current directory
    root_dir_list = __file__.split("/")[:-2]
    root_dir = "/".join(root_dir_list)

    # Adding the jar to the flink streaming environment
    env.add_jars(
        f"file://{root_dir}/lib/flink-sql-connector-kafka-3.1.0-1.18.jar",
    )
    return env

def configure_source(server: str, earliest: bool = False) -> KafkaSource:
    """Makes kafka source initialization"""
    properties = {
        "bootstrap.servers": server,
        "group.id": "user-behaviors",
    }

    offset = KafkaOffsetsInitializer.latest()
    if earliest:
        offset = KafkaOffsetsInitializer.earliest()

    kafka_source = (
        KafkaSource.builder()
        .set_topics(KAFKA_TOPIC)
        .set_properties(properties)
        .set_starting_offsets(offset)
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )
    return kafka_source

###################################################
#  Hàm chuyển đổi dữ liệu và ghi vào ClickHouse   #
###################################################
def product_dim(record):
    client = clickhouse_connect.get_client(host=CLICKHOUSE_HOST, database=CLICKHOUSE_DATABASE)
    try:
        # Parse JSON record
        data = json.loads(record)
        
        # Trích xuất các trường và chuyển đổi timestamp thành đối tượng datetime
        id = int(data.get("id"))
        name = data.get("name")
        slug_name = data.get("slug_name")
        description = data.get("description")
        category = data.get("category")
        version = data.get("version")
        
        # Chuẩn bị dữ liệu để chèn vào ClickHouse
        row = (id, name, slug_name, description, category, version)
        
        # Ghi dữ liệu vào ClickHouse
        client.insert('product_dim', [row])
        logger.info(f"Ghi thành công bản ghi: {row}")
        
    except Exception as e:
        logger.error(f"Lỗi khi xử lý bản ghi: {e}")
    client.close()


def main() -> None:
    """Main flow controller"""

    # Initialize environment
    env = initialize_env()
    logger.info("✅ Initializing environment")

    # Define source and sinks
    kafka_source = configure_source(f"{KAFKA_HOST}:{KAFKA_PORT}")
    logger.info("🐿️ Configuring source and sinks")

    data_stream = env.from_source(
        kafka_source, WatermarkStrategy.no_watermarks(), "Kafka sensors topic"
    )
    logger.info("🙊 Create a DataStream from the Kafka source and assign watermarks")
    data_stream.print()

    logger.info("🚀 Ready to sink data")
    data_stream.map(lambda record: product_dim(record))

    # Thực thi job Flink
    env.execute("Flink ClickHouse Job")

if __name__ == "__main__":
    main()