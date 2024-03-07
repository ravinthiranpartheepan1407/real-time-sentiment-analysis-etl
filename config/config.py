import os
from dotenv import load_dotenv

load_dotenv()
config = {
    "kafka": {
        "bootstrap.servers": os.getenv("kafka_bootstrap"),
        "security.protocol": "SASL_SSL",
        "sasl.mechanisms": "PLAIN",
        "sasl.username": os.getenv("cluster_api_key"),
        "sasl.password": os.getenv("cluster_secret"),
        "session.timeout.ms": 45000,
    },
    "schema_registry": {
        "url": os.getenv("kafka_api"),
        "basic.auth.user.info": os.getenv("schema_url") + ":" + os.getenv("schema_auth")
    },
    "openai": {
        "api_key": os.getenv("openai_api_key")
    }
}
