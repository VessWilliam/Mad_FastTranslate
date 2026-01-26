"""Configuration For Supported Languages"""


SUPPORTED_LANGUAGES = {
    "en": "English",
    "ja": "Japanese",
    "zh": "Chinese",
}

SUPPORTED_PAIRS = {
    (src , tgt) 
    for src in SUPPORTED_LANGUAGES
    for tgt in SUPPORTED_LANGUAGES
    if src != tgt
}

REQUIRED_TRANSLATIONS = list(SUPPORTED_PAIRS)