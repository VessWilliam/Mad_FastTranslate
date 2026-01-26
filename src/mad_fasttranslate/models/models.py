from pydantic import BaseModel, Field
from typing import List, Optional


class TranslateRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=50000,
        description="The text to be translated",
        examples=["Hello, World!", "こんにちは!", "你好!"],
    )
    to_lang: str = Field(
        ...,
        min_length=2,
        max_length=5,
        description="The target language code",
        examples=["ja", "en", "zh"],
    )
    from_lang: Optional[str] = Field(
        default=None,
        description="The source language (auto-detect if not provided)",
        examples=["en", "ja", "zh"],
    )


class TranslateResponse(BaseModel):
    detected_lang: str = Field(description="Detected Source Language")
    translated_text: str = Field(description="Translated Text")
    from_lang: str = Field(description="Source Language")
    to_lang: str = Field(description="Target Language")
    char_count: int = Field(description="Number Of Characters Translated")


class LanguageInfo(BaseModel):
    code: str = Field(description="Language code, e.g., 'en', 'ja', 'zh'")
    name: str = Field(description="Language name, e.g., 'English'")


class SupportedLanguageResponse(BaseModel):
    languages: List[LanguageInfo] = Field(description="List of supported languages")
    pairs_count: int  = Field(description="Number of supported translation pairs")
