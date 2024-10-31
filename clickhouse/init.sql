CREATE DATABASE IF NOT EXISTS olap;
CREATE TABLE IF NOT EXISTS olap.product_dim (
    id UInt32,
    name String,
    slug_name String,
    description String,
    category String,
    version UInt32
)
ENGINE = ReplacingMergeTree(version)
ORDER BY id
PRIMARY KEY id;