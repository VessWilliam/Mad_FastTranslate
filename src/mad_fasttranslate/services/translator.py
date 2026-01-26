"""Translate Service"""

from argostranslate import translate
from fastapi import HTTPException
from langdetect import DetectorFactory, detect
from ..config import SUPPORTED_LANGUAGES, SUPPORTED_PAIRS

DetectorFactory.seed = 0


class TranslatorService:
    @staticmethod
    def detect_language(text: str) -> str:
        try:
            detected = detect(text)

            if detected.startswith("zh"):
                detected = "zh"

            print(f"[Translator Service] Detected Language : {detected}")
            return detected
        except Exception as e:
            raise HTTPException(status_code=400, 
                                detail=f"Language detection failed : {str(e)}")

    @staticmethod
    def validate_language(lang: str) -> None:
        if lang not in SUPPORTED_LANGUAGES:
            raise HTTPException(
                400, f"Language '{lang}' not supported. Use: en, ja, zh"
            )

    @staticmethod
    def validate_pair(from_lang: str, to_lang: str) -> None:
        if (from_lang, to_lang) not in SUPPORTED_PAIRS:
            raise HTTPException(
                400, f"Translation pair '{from_lang} -> {to_lang}'not supported."
            )

    @staticmethod
    def translate_text(text: str, from_lang: str, to_lang: str) -> str:
        try:
          TranslatorService.validate_language(from_lang)
          TranslatorService.validate_language(to_lang)
          TranslatorService.validate_pair(from_lang, to_lang)
            
          installed_languages = translate.get_installed_languages()
            
            # Get the source language object
          from_lang_obj = next((l for l in installed_languages if l.code == from_lang), None)
            
            # Get the target language object
          to_lang_obj = next((l for l in installed_languages if l.code == to_lang), None)
            
          if not from_lang_obj or not to_lang_obj:
                raise HTTPException(
                    status_code=500,
                    detail=f"No Translation Model installed for `{from_lang} -> {to_lang}`")
            
            # Get the translation object from source to target (pass Language object)
          translation = from_lang_obj.get_translation(to_lang_obj)
            
          if not translation:
                raise HTTPException(
                    status_code=500,
                    detail=f"No Translation Model installed for `{from_lang} -> {to_lang}`")
            
            # Perform the translation
          return translation.translate(text)
           
        except HTTPException:
                 raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"translation failed : {str(e)}"
            )
