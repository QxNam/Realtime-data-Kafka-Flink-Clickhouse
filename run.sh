docker compose exec flink-jobmanager flink run -py ./jobs/etl.py -d

docker exec -it clickhouse-server clickhouse-client --query "SELECT count(*) FROM olap.product_dim;" 
watch -n 1 docker exec -it clickhouse-server clickhouse-client --query "SELECT * FROM olap.product_dim LIMIT 10;"