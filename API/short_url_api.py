from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse

from DB.models import URLModel
from ALGORITHM.create_hash import HashUrl

app = FastAPI()

def get_url_model():
    return URLModel()

@app.post("/shorten")
async def shorten_url(
    url: str,
    url_model: URLModel = Depends(get_url_model)
):
    
    existing_urls = url_model.search_by_url(url)
    
    if existing_urls:
        return {
            "original_url": url,
            "short_code": existing_urls[0].url_shortcut,
            "short_url": f"http://домен_сервиса/{existing_urls[0].url_shortcut}",
            "message": "URL уже существует в базе",
            "id": existing_urls[0].id,
            "already_exists": True
        }
    
    short_code = HashUrl.short_hash_6_chars(url)

    if (short_code == 0): return {
        "Error Message": "Введена невалидная ссылка",
        "original_url": url

    }
        
    url_id = url_model.create(short_code, url)
    
    return {
        "id": url_id,
        "original_url": url,
        "short_code": short_code,
        "short_url": f"http://домен_сервиса/{short_code}"
    }


@app.get("/{code}")
async def redirect_to_url(
    code: str,
    url_model: URLModel = Depends(get_url_model)
):
    url_data = url_model.get_by_shortcut(code)
    
    if not url_data:
        raise HTTPException(
            status_code=404,
            detail=f"Код '{code}' не найден"
        )
    
    return RedirectResponse(url=url_data.url)
