from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from scraper import run_scraper

app = FastAPI(title="Real Estate Scraper API")


class ScrapingRequest(BaseModel):
    location: str
    property_type: str | None = None
    property_subtype: str | None = None
    price_min: str | None = None
    price_max: str | None = None
    living_surface_min: str | None = None
    living_surface_max: str | None = None
    plot_surface_min: str | None = None
    plot_surface_max: str | None = None
    total_surface_min: str | None = None
    total_surface_max: str | None = None
    rooms_min: str | None = None
    rooms_max: str | None = None
    bedrooms_min: str | None = None
    bedrooms_max: str | None = None
    bathrooms_min: str | None = None
    bathrooms_max: str | None = None
    construction_year_min: str | None = None
    construction_year_max: str | None = None


@app.post("/scrape")
async def scrape_properties(request: ScrapingRequest):
    try:
        results = await run_scraper(
            location=request.location,
            property_type=request.property_type,
            property_subtype=request.property_subtype,
            price_min=request.price_min,
            price_max=request.price_max,
            living_surface_min=request.living_surface_min,
            living_surface_max=request.living_surface_max,
            plot_surface_min=request.plot_surface_min,
            plot_surface_max=request.plot_surface_max,
            total_surface_min=request.total_surface_min,
            total_surface_max=request.total_surface_max,
            rooms_min=request.rooms_min,
            rooms_max=request.rooms_max,
            bedrooms_min=request.bedrooms_min,
            bedrooms_max=request.bedrooms_max,
            bathrooms_min=request.bathrooms_min,
            bathrooms_max=request.bathrooms_max,
            construction_year_min=request.construction_year_min,
            construction_year_max=request.construction_year_max,
        )
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
