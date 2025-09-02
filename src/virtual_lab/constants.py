"""Holds constants."""

# 支持OpenAI和智谱AI模型
DEFAULT_MODEL = "glm-4-plus"  # 智谱AI默认模型

# OpenAI模型价格 (USD per token，2025年1月18日)
OPENAI_MODEL_TO_INPUT_PRICE_PER_TOKEN = {
    "gpt-3.5-turbo-0125": 0.5 / 10**6,
    "gpt-4o-2024-08-06": 2.5 / 10**6,
    "gpt-4o-2024-05-13": 5 / 10**6,
    "gpt-4o-mini-2024-07-18": 0.15 / 10**6,
    "o1-mini-2024-09-12": 3 / 10**6,
}

OPENAI_MODEL_TO_OUTPUT_PRICE_PER_TOKEN = {
    "gpt-3.5-turbo-0125": 1.5 / 10**6,
    "gpt-4o-2024-08-06": 10 / 10**6,
    "gpt-4o-2024-05-13": 15 / 10**6,
    "gpt-4o-mini-2024-07-18": 0.6 / 10**6,
    "o1-mini-2024-09-12": 12 / 10**6,
}

# 智谱AI模型价格 (CNY per token，按照官方定价)
ZHIPUAI_MODEL_TO_INPUT_PRICE_PER_TOKEN = {
    "glm-4-plus": 0.1 / 1000,  # 100元/百万tokens
    "glm-4-0520": 0.1 / 1000,
    "glm-4": 0.1 / 1000,
    "glm-4-air": 0.001 / 1000,  # 1元/百万tokens
    "glm-4-airx": 0.01 / 1000,  # 10元/百万tokens
    "glm-4-flash": 0.001 / 1000,  # 1元/百万tokens
}

ZHIPUAI_MODEL_TO_OUTPUT_PRICE_PER_TOKEN = {
    "glm-4-plus": 0.1 / 1000,
    "glm-4-0520": 0.1 / 1000,
    "glm-4": 0.1 / 1000,
    "glm-4-air": 0.001 / 1000,
    "glm-4-airx": 0.01 / 1000,
    "glm-4-flash": 0.001 / 1000,
}

# 合并价格配置，优先支持智谱AI
MODEL_TO_INPUT_PRICE_PER_TOKEN = {
    **ZHIPUAI_MODEL_TO_INPUT_PRICE_PER_TOKEN,
    **OPENAI_MODEL_TO_INPUT_PRICE_PER_TOKEN,
}

MODEL_TO_OUTPUT_PRICE_PER_TOKEN = {
    **ZHIPUAI_MODEL_TO_OUTPUT_PRICE_PER_TOKEN,
    **OPENAI_MODEL_TO_OUTPUT_PRICE_PER_TOKEN,
}

FINETUNING_MODEL_TO_INPUT_PRICE_PER_TOKEN = {
    "gpt-4o-2024-08-06": 3.75 / 10**6,
    "gpt-4o-mini-2024-07-18": 0.3 / 10**6,
}

FINETUNING_MODEL_TO_OUTPUT_PRICE_PER_TOKEN = {
    "gpt-4o-2024-08-06": 15 / 10**6,
    "gpt-4o-mini-2024-07-18": 1.2 / 10**6,
}

FINETUNING_MODEL_TO_TRAINING_PRICE_PER_TOKEN = {
    "gpt-4o-2024-08-06": 25 / 10**6,
    "gpt-4o-mini-2024-07-18": 3 / 10**6,
}

DEFAULT_FINETUNING_EPOCHS = 4

CONSISTENT_TEMPERATURE = 0.2
CREATIVE_TEMPERATURE = 0.8

PUBMED_TOOL_NAME = "pubmed_search"
PUBMED_TOOL_DESCRIPTION = {
    "type": "function",
    "function": {
        "name": PUBMED_TOOL_NAME,
        "description": "Get abstracts or the full text of biomedical and life sciences articles from PubMed Central.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to use to search PubMed Central for scientific articles.",
                },
                "num_articles": {
                    "type": "integer",
                    "description": "The number of articles to return from the search query.",
                },
                "abstract_only": {
                    "type": "boolean",
                    "description": "Whether to return only the abstract of the articles.",
                },
            },
            "required": ["query", "num_articles"],
        },
    },
}
