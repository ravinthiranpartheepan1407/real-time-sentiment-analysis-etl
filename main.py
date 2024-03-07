# ----------------------------------- Files ----------------------------------------------------------
# Config: Contains keys related to kafka cluster, openAI, and schema registry
# Dockerfile.spark: Used to create container
# docker-compose.yml: Conatins all services (Master & Workers) and containers.
# ----------------------------------- Files ----------------------------------------------------------

# ----------------------------------- Modules ----------------------------------------------------------
# Socket: Used to capture and transmit data in real time
# Spark: Used to process the data stream
# Kafka: Used to buffer and manage the flow of real time data stream
# Elastisearch: Used to query and visualize the processed data (Store and Index)
# OpenAI: To harness the sentiment analysis capabilities
# ----------------------------------- Modules ----------------------------------------------------------

# ----------------------------------- Workflow ----------------------------------------------------------
# Data Ingestion: Stream data from csv using sockets
# Data Preprocessing: Spark streaming from socket data stream and process it into chunks of text
# Sentiment Analysis: With the help of openAI sentiment api it analysis the sentiment freq based on chunks of text
# Data storage: Store the analysed sentiment freq with data in kafka and streamed into elastisearch