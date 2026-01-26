"""Fast API APP - Translate Support Lang: (EN, JA, ZH)"""

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .config import SUPPORTED_LANGUAGES, SUPPORTED_PAIRS
from .models import (
    LanguageInfo,
    SupportedLanguageResponse,
    TranslateRequest,
    TranslateResponse,
)
from .services import TranslatorService , StartupService

### App Initialization ###
app = FastAPI(
    title="Mad Fast_Translate",
    description="A FastAPI App - Translate Support Lang: (EN, JA, ZH)."
)

### Startup Events ###
@app.on_event("startup")
def startup_event():
    StartupService.install_missing_models()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

translator = TranslatorService()


### Routes ###
@app.get("/", 
         tags=["Info"], 
         summary="App Info & Supported Languages", 
         description="Return App Info & Supported Languages.")

def root():
    return {
        "name": "Mad FastTranslate",
        "version": "0.1.0",
        "supported_languages": SUPPORTED_LANGUAGES,
        "docs": "/docs",
    }


@app.get("/languages",
         response_model=SupportedLanguageResponse, 
         tags=["Info"], 
         summary="Get Supported Languages & Translation Pairs", 
         description="Return Supported Languages & Supported Translation Pairs.")

def get_languages():
    languagues = [
        LanguageInfo(code=code, name=name)
        for code, name in SUPPORTED_LANGUAGES.items()
    ]
    return SupportedLanguageResponse(
        languages=languagues,
        pairs_count=len(SUPPORTED_PAIRS)
    )


@app.post("/translate", 
          response_model=TranslateResponse, 
          tags=["Translate"], 
          summary="Translate Text",
          description="Translate Text From one Language To Another.")

def translate(req: TranslateRequest):
    if not req.text.strip():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Text cannot be empty")

    from_lang = req.from_lang or translator.detect_language(req.text)
    translator.validate_language(from_lang)
    translator.validate_language(req.to_lang)

    if from_lang == req.to_lang:
        return TranslateResponse(
            detected_lang=from_lang,
            translated_text=req.text,
            from_lang=from_lang,
            to_lang=req.to_lang,
            char_count=len(req.text)
        )


    translator.validate_pair(from_lang, req.to_lang)
    translated = translator.translate_text(req.text, from_lang, req.to_lang)

    return TranslateResponse(
        detected_lang=from_lang,
        translated_text=translated,
        from_lang=from_lang,
        to_lang=req.to_lang,
        char_count=len(translated)
    )


#### Main Entry Point ####
def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
