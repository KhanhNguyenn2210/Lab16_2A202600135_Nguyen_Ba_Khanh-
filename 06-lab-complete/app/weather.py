import httpx
from fastapi import HTTPException
from app.config import settings

async def get_weather(city: str) -> str:
    if not settings.openweather_api_key:
        return f"Thời tiết tại {city} là 25°C, trời nắng (Dữ liệu Mock vì thiếu API Key)."
        
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": settings.openweather_api_key,
        "units": "metric",
        "lang": "vi"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10.0)
            if response.status_code == 404:
                return f"Xin lỗi, tôi không tìm thấy thành phố '{city}'."
            response.raise_for_status()
            
            data = response.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            
            return f"Thời tiết tại {city} hiện tại là {temp}°C, {desc}, độ ẩm {humidity}%."
            
        except httpx.RequestError as e:
            return f"Đã xảy ra lỗi khi kết nối tới dịch vụ thời tiết: {str(e)}"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi hệ thống khi lấy thời tiết: {str(e)}")
