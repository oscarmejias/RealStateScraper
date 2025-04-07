import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from playwright.async_api import async_playwright, expect
import asyncio
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

#########################################################################
###############################QUERIES###################################
#########################################################################

INITIAL_URL = "https://www.engelvoelkers.com/co/es"

# Variable para la location de búsqueda
location = "Bogota, Colombia"

# Crear directorio para screenshots si no existe
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# Clase para manejar los filtros de propiedades
class FilterManager:
    def __init__(self, page):
        self.page = page

    async def open_filters(self):
        """Abre la sección de filtros si no está abierta"""
        try:
            # Intento 1: Por el data-test-id específico
            filter_button = self.page.locator(
                "[data-test-id='search-components_filter-bar_advanced-filters-button']"
            )
            await filter_button.wait_for(state="visible")
            await filter_button.click()
        except:
            try:
                # Intento 2: Por el span dentro del botón
                filter_button = self.page.locator(
                    "button span:has-text('Filtros')"
                ).first
                await filter_button.wait_for(state="visible")
                await filter_button.click()
            except:
                # Intento 3: Por el botón que contiene el SVG y el texto
                filter_button = self.page.locator(
                    "button:has(svg):has-text('Filtros')"
                ).first
                await filter_button.wait_for(state="visible")
                await filter_button.click()
        await self.page.wait_for_load_state("networkidle")

    async def apply_filters(
        self,
        property_type: Optional[str] = None,
        property_subtype: Optional[str] = None,
        price_min: Optional[str] = None,
        price_max: Optional[str] = None,
        living_surface_min: Optional[str] = None,
        living_surface_max: Optional[str] = None,
        plot_surface_min: Optional[str] = None,
        plot_surface_max: Optional[str] = None,
        total_surface_min: Optional[str] = None,
        total_surface_max: Optional[str] = None,
        rooms_min: Optional[str] = None,
        rooms_max: Optional[str] = None,
        bedrooms_min: Optional[str] = None,
        bedrooms_max: Optional[str] = None,
        bathrooms_min: Optional[str] = None,
        bathrooms_max: Optional[str] = None,
        construction_year_min: Optional[str] = None,
        construction_year_max: Optional[str] = None,
    ):
        """
        Applies property search filters based on provided parameters.
        All parameters are optional.

        Args:
            property_type: Main property type (e.g. "Viviendas")
            property_subtype: Property subtype (e.g. "Apartamento")
            price_min/max: Price range
            living_surface_min/max: Living surface range
            plot_surface_min/max: Plot surface range
            total_surface_min/max: Total surface range
            rooms_min/max: Number of rooms range
            bedrooms_min/max: Number of bedrooms range
            bathrooms_min/max: Number of bathrooms range
            construction_year_min/max: Construction year range

        """
        # Abrir sección de filtros
        await self.open_filters()

        # Apply property type
        if property_type:
            type_dropdown = self.page.locator(
                "[data-test-id='search-components_advanced-filters_property-type-filter_button']"
            )
            await type_dropdown.wait_for(state="visible")
            await type_dropdown.click()

            # Select specific option
            await self.page.keyboard.type(property_type)
            await self.page.keyboard.press("Enter")
            await self.page.wait_for_timeout(500)

        # Apply property subtype
        if property_subtype:
            subtype_dropdown = self.page.locator(
                "[data-test-id='search-components_advanced-filters_property-sub-type-filter_button']"
            )
            await subtype_dropdown.wait_for(state="visible")
            await subtype_dropdown.click()

            await self.page.keyboard.type(property_subtype)
            await self.page.keyboard.press("Enter")
            await self.page.wait_for_timeout(500)

        # Apply price range
        if price_min or price_max:
            if price_min:
                price_min_field = self.page.locator(
                    "[data-test-id='search-components_advanced-filters_price-filter_input-min']"
                )
                await price_min_field.fill(str(price_min))
                await self.page.wait_for_timeout(300)

            if price_max:
                price_max_field = self.page.locator(
                    "[data-test-id='search-components_advanced-filters_price-filter_input-max']"
                )
                await price_max_field.fill(str(price_max))
                await self.page.wait_for_timeout(300)

        # Apply living surface
        if living_surface_min or living_surface_max:
            if living_surface_min:
                min_input = self.page.locator(
                    "[data-test-id='search-components_advanced-filters_living-surface-filter_input-min']"
                )
                await min_input.fill(str(living_surface_min))
                await self.page.wait_for_timeout(300)

            if living_surface_max:
                max_input = self.page.locator(
                    "[data-test-id='search-components_advanced-filters_living-surface-filter_input-max']"
                )
                await max_input.fill(str(living_surface_max))
                await self.page.wait_for_timeout(300)

        # Apply plot surface
        if plot_surface_min or plot_surface_max:
            if plot_surface_min:
                min_input = self.page.locator(
                    "[data-test-id='search-components_advanced-filters_plot-surface-filter_input-min']"
                )
                await min_input.fill(str(plot_surface_min))
                await self.page.wait_for_timeout(300)

            if plot_surface_max:
                max_input = self.page.locator(
                    "[data-test-id='search-components_advanced-filters_plot-surface-filter_input-max']"
                )
                await max_input.fill(str(plot_surface_max))
                await self.page.wait_for_timeout(300)

        # Apply total surface
        if total_surface_min or total_surface_max:
            if total_surface_min:
                min_input = self.page.locator(
                    "[data-test-id='search-components_advanced-filters_total-surface-filter_input-min']"
                )
                await min_input.fill(str(total_surface_min))
                await self.page.wait_for_timeout(300)

            if total_surface_max:
                max_input = self.page.locator(
                    "[data-test-id='search-components_advanced-filters_total-surface-filter_input-max']"
                )
                await max_input.fill(str(total_surface_max))
                await self.page.wait_for_timeout(300)

        # Apply rooms
        if rooms_min or rooms_max:
            if rooms_min:
                min_input = self.page.locator(
                    "[data-test-id='search-components_advanced-filters_rooms-filter_input-min']"
                )
                await min_input.fill(str(rooms_min))
                await self.page.wait_for_timeout(300)

            if rooms_max:
                max_input = self.page.locator(
                    "[data-test-id='search-components_advanced-filters_rooms-filter_input-max']"
                )
                await max_input.fill(str(rooms_max))
                await self.page.wait_for_timeout(300)

        # Apply bedrooms
        if bedrooms_min or bedrooms_max:
            if bedrooms_min:
                min_input = self.page.locator(
                    "[data-test-id='search-components_advanced-filters_bedrooms-filter_input-min']"
                )
                await min_input.fill(str(bedrooms_min))
                await self.page.wait_for_timeout(300)

            if bedrooms_max:
                max_input = self.page.locator(
                    "[data-test-id='search-components_advanced-filters_bedrooms-filter_input-max']"
                )
                await max_input.fill(str(bedrooms_max))
                await self.page.wait_for_timeout(300)

        # Apply bathrooms
        if bathrooms_min or bathrooms_max:
            if bathrooms_min:
                min_input = self.page.locator(
                    "[data-test-id='search-components_advanced-filters_bathrooms-filter_input-min']"
                )
                await min_input.fill(str(bathrooms_min))
                await self.page.wait_for_timeout(300)

            if bathrooms_max:
                max_input = self.page.locator(
                    "[data-test-id='search-components_advanced-filters_bathrooms-filter_input-max']"
                )
                await max_input.fill(str(bathrooms_max))
                await self.page.wait_for_timeout(300)

        # Apply construction year
        if construction_year_min or construction_year_max:
            if construction_year_min:
                min_input = self.page.locator(
                    "[data-test-id='search-components_advanced-filters_construction-year-filter_input-min']"
                )
                await min_input.fill(str(construction_year_min))
                await self.page.wait_for_timeout(300)

            if construction_year_max:
                max_input = self.page.locator(
                    "[data-test-id='search-components_advanced-filters_construction-year-filter_input-max']"
                )
                await max_input.fill(str(construction_year_max))
                await self.page.wait_for_timeout(300)

        # Click "Done" button to apply filters
        done_button = self.page.locator(
            "[data-test-id='search-components_advanced-filters_submit-button']"
        )
        await done_button.click()
        await self.page.wait_for_load_state("networkidle")


#########################################################################
##############################SCRAPING###################################
#########################################################################


async def run_scraper(
    location: str,
    property_type: Optional[str] = None,
    property_subtype: Optional[str] = None,
    price_min: Optional[str] = None,
    price_max: Optional[str] = None,
    living_surface_min: Optional[str] = None,
    living_surface_max: Optional[str] = None,
    plot_surface_min: Optional[str] = None,
    plot_surface_max: Optional[str] = None,
    total_surface_min: Optional[str] = None,
    total_surface_max: Optional[str] = None,
    rooms_min: Optional[str] = None,
    rooms_max: Optional[str] = None,
    bedrooms_min: Optional[str] = None,
    bedrooms_max: Optional[str] = None,
    bathrooms_min: Optional[str] = None,
    bathrooms_max: Optional[str] = None,
    construction_year_min: Optional[str] = None,
    construction_year_max: Optional[str] = None,
) -> List[Dict[str, Any]]:
    results = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        )
        page = await context.new_page()

        try:
            logger.info("Starting scraper")
            await page.goto(INITIAL_URL)

            logger.info(f"Entered {INITIAL_URL}")

            # Botón de aceptar cookies
            try:
                # Esperar específicamente por el popup de Didomi
                cookie_popup = page.locator("#didomi-popup")
                if await cookie_popup.is_visible():
                    cookie_button = page.locator("#didomi-notice-agree-button")
                    await cookie_button.wait_for(state="visible")
                    await cookie_button.click()
                    logger.info("Cookie banner aceptado")
                    # Esperar a que el popup desaparezca completamente
                    await cookie_popup.wait_for(state="hidden")
                    await page.wait_for_load_state("networkidle")
            except Exception as e:
                logger.info(f"No se encontró el banner de cookies: {str(e)}")

            await page.wait_for_load_state("networkidle")

            # Buscar el campo de búsqueda
            search_input = page.locator(".sc-7856fc0a-2.foWFcA")
            await search_input.wait_for(state="visible")
            await search_input.fill(location)
            logger.info("Campo de búsqueda completado")
            await page.wait_for_timeout(2000)

            # Asegurarse de que el botón de búsqueda esté visible y clickeable
            search_button = page.locator(".sc-a6c22956-0.fMdhBy.sc-7856fc0a-4.kUdQjI")
            await search_button.wait_for(state="visible")
            await expect(search_button).to_be_enabled()
            await search_button.click()
            logger.info("Botón de búsqueda clickeado")

            # Esperar a que la navegación se complete
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(3000)

            # Crear una instancia del FilterManager
            filter_manager = FilterManager(page)
            logger.info("filter manager instanciated")

            # Aplicar filtros personalizados
            await filter_manager.apply_filters(
                property_type=property_type,
                property_subtype=property_subtype,
                price_min=price_min,
                price_max=price_max,
                living_surface_min=living_surface_min,
                living_surface_max=living_surface_max,
                plot_surface_min=plot_surface_min,
                plot_surface_max=plot_surface_max,
                total_surface_min=total_surface_min,
                total_surface_max=total_surface_max,
                rooms_min=rooms_min,
                rooms_max=rooms_max,
                bedrooms_min=bedrooms_min,
                bedrooms_max=bedrooms_max,
                bathrooms_min=bathrooms_min,
                bathrooms_max=bathrooms_max,
                construction_year_min=construction_year_min,
                construction_year_max=construction_year_max,
            )
            logger.info("filters applied")

            # Esperar a que la página cargue completamente
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(2000)

            # Obtener numero de propiedades encontradas
            logger.info("waiting for properties to load")
            try:
                property_cards = page.locator(".sc-e5f1eba3-3.cGSWBa article")

                # Verificar si encontramos artículos
                count = await property_cards.count()
                logger.info(f"Número de artículos encontrados: {count}")
            except Exception as e:
                logger.error(f"Error al buscar artículos: {str(e)}")

            # Esperar a que exista al menos un artículo
            await expect(property_cards).not_to_have_count(0)

            # Esperar a que al menos una card esté visible
            await property_cards.first.wait_for(state="visible")

            # Obtener el número total de cards
            count = await property_cards.count()
            print(f"\nSe encontraron {count} propiedades")

            # Iterar sobre cada card
            for i in range(count):
                card = property_cards.nth(i)

                # Verificar si el artículo tiene información útil
                try:
                    # Esperar a que el artículo tenga contenido relevante
                    await expect(card).not_to_have_class("sc-e5f1eba3-11 cBTUg")

                    await card.wait_for(state="visible")
                    logger.info(f"Card {i + 1}: {await card.is_visible()}")

                    # Verificar primero si el artículo tiene la información necesaria
                    price_element = card.locator(
                        "[data-test-id$='search-components_result-card_price']"
                    )
                    if not await price_element.is_visible():
                        continue

                    price = await price_element.inner_text()
                    location = await card.locator(
                        "[data-test-id$='_location']"
                    ).inner_text()
                    bedrooms = await card.locator(
                        "[data-test-id$='-bedrooms']"
                    ).inner_text()
                    bathrooms = await card.locator(
                        "[data-test-id$='-bathrooms']"
                    ).inner_text()
                    headline = await card.locator(
                        "[data-test-id$='_headline']"
                    ).inner_text()

                    # Solo procesar si tenemos al menos algunos datos
                    if any([price.strip(), location.strip(), headline.strip()]):
                        property_data = {
                            "location": location,
                            "headline": headline,
                            "price": price,
                            "bedrooms": bedrooms,
                            "bathrooms": bathrooms,
                        }

                        try:
                            # Intentar obtener el enlace usando el data-test-id del artículo
                            article_id = await card.get_attribute("data-test-id")
                            if article_id:
                                link_element = card.locator(
                                    f"[data-test-id='{article_id}'] a"
                                ).first
                                if await link_element.is_visible():
                                    link = await link_element.get_attribute("href")
                                    if link:
                                        property_data["url"] = link
                        except Exception as e:
                            print(f"No se pudo obtener el enlace: {str(e)}")

                        results.append(property_data)

                    # Modificar la ruta de los screenshots
                    await card.screenshot(
                        path=f"{SCREENSHOT_DIR}/property_{timestamp}_{i}.png"
                    )

                except Exception as e:
                    logger.info(
                        f"Saltando artículo {i + 1} por falta de información útil"
                    )
                    continue

        except Exception as e:
            logger.error(f"Error durante el scraping: {str(e)}")
            # Tomar screenshot del error
            await page.screenshot(path=f"{SCREENSHOT_DIR}/error_{timestamp}.png")
            raise
        finally:
            await context.close()
            await browser.close()

    return results


if __name__ == "__main__":
    # Ejemplo de uso directo del scraper
    async def main():
        results = await run_scraper(
            location="Bogota, Colombia",
            property_type="Apartamento",
            living_surface_min="1000",
            living_surface_max="10000",
            price_min="500000000",
            price_max="13000000000",
            rooms_min="3",
        )

        for prop in results:
            print("\nPropiedad encontrada:")
            for key, value in prop.items():
                print(f"{key}: {value}")

    # Ejecutar la función asíncrona
    asyncio.run(main())
