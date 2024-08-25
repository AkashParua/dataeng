import json
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
)
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames
parameters = {
    GenTextParamsMetaNames.DECODING_METHOD: "sample",
    GenTextParamsMetaNames.STOP_SEQUENCES: ['\n\n']
}
from llama_index.llms.ibm import WatsonxLLM
# Specify the path to your settings.json file
settings_file = 'config/config.json'

# Load the JSON data from the file
with open(settings_file) as f:
    settings = json.load(f)

# Import all the settings as variables
globals().update(settings)

