from censius.endpoint import CENSIUS_ENDPOINT


GATEWAY_LLM_URL = f"{CENSIUS_ENDPOINT}/api/llm"

GATEWAY_URL = f"{CENSIUS_ENDPOINT}/api/sdkapi"


LLM_REGISTER_DATASET_URL = (
    lambda project_id: f"{GATEWAY_URL}/{project_id}/res/nlp-input-training/frd/v1/llm/register_training_data"
)

LLM_REGISTER_MODEL_URL = (
    lambda project_id: f"{GATEWAY_URL}/{project_id}/res/register_model/frd/api/llm/register_model"
)

LLM_REGISTER_LOGS = (
    lambda project_id: f"{GATEWAY_URL}/{project_id}/res/nlp-input-logs/frd/v1/llm/register_logs"
)

BULK_CHUNK_SIZE = 2000
