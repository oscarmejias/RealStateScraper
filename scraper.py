import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from playwright.async_api import async_playwright, expect
import asyncio
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime
import random

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
            # Simular movimiento del mouse aleatorio antes de buscar filtros
            await self.page.mouse.move(
                random.randint(100, 500), random.randint(100, 500)
            )
            await self.page.wait_for_timeout(random.randint(1000, 2000))

            # Intento 1: Por el data-test-id específico
            filter_button = self.page.locator(
                "[data-test-id='search-components_filter-bar_advanced-filters-button']"
            )
            await filter_button.wait_for(state="visible")
            await filter_button.hover()
            await self.page.wait_for_timeout(random.randint(500, 1000))
            await filter_button.click()
            logger.info("Filters opened")
        except:
            logger.info("Filters not found, trying to find them in different ways")
            try:
                # Simular movimiento del mouse aleatorio antes del segundo intento
                await self.page.mouse.move(
                    random.randint(100, 500), random.randint(100, 500)
                )
                await self.page.wait_for_timeout(random.randint(1000, 2000))

                # Intento 2: Por el span dentro del botón
                filter_button = self.page.locator(
                    "button span:has-text('Filtros')"
                ).first
                await filter_button.wait_for(state="visible")
                await filter_button.hover()
                await self.page.wait_for_timeout(random.randint(500, 1000))
                await filter_button.click()
                logger.info("Filters opened")
            except:
                logger.info("Filters not found, trying to find them in different ways")
                # Simular movimiento del mouse aleatorio antes del tercer intento
                await self.page.mouse.move(
                    random.randint(100, 500), random.randint(100, 500)
                )
                await self.page.wait_for_timeout(random.randint(1000, 2000))

                # Intento 3: Por el botón que contiene el SVG y el texto
                filter_button = self.page.locator(
                    "button:has(svg):has-text('Filtros')"
                ).first
                await filter_button.wait_for(state="visible")
                await filter_button.hover()
                await self.page.wait_for_timeout(random.randint(500, 1000))
                await filter_button.click()
                logger.info("Filters opened")

        # Esperar a que la página se estabilice después de abrir filtros
        await self.page.wait_for_timeout(random.randint(2000, 3000))
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
        # Abrir sección de filtros con comportamiento humano
        await self.open_filters()

        # Simular scroll aleatorio dentro del panel de filtros
        await self.page.mouse.wheel(0, random.randint(100, 300))
        await self.page.wait_for_timeout(random.randint(500, 1500))

        # Aplicar cada filtro con comportamiento humano
        for key, value in {
            "property_type": property_type,
            "property_subtype": property_subtype,
            "price_min": price_min,
            "price_max": price_max,
            "living_surface_min": living_surface_min,
            "living_surface_max": living_surface_max,
            "plot_surface_min": plot_surface_min,
            "plot_surface_max": plot_surface_max,
            "total_surface_min": total_surface_min,
            "total_surface_max": total_surface_max,
            "rooms_min": rooms_min,
            "rooms_max": rooms_max,
            "bedrooms_min": bedrooms_min,
            "bedrooms_max": bedrooms_max,
            "bathrooms_min": bathrooms_min,
            "bathrooms_max": bathrooms_max,
            "construction_year_min": construction_year_min,
            "construction_year_max": construction_year_max,
        }.items():
            if value is not None:
                try:
                    # Simular movimiento del mouse antes de cada filtro

                    await self.page.wait_for_timeout(200)

                    if key == "property_type":
                        dropdown = self.page.locator(
                            "[data-test-id='search-components_advanced-filters_property-type-filter_button']"
                        )
                        await dropdown.wait_for(state="visible")
                        await dropdown.hover()
                        await self.page.wait_for_timeout(200)
                        await dropdown.click()

                        # Escribir el valor letra por letra
                        for char in value:
                            await self.page.keyboard.type(
                                char, delay=random.randint(50, 150)
                            )
                        await self.page.wait_for_timeout(200)
                        await self.page.keyboard.press("Enter")
                        await self.page.wait_for_timeout(random.randint(500, 1000))

                    elif key == "property_subtype":
                        dropdown = self.page.locator(
                            "[data-test-id='search-components_advanced-filters_property-sub-type-filter_button']"
                        )
                        await dropdown.wait_for(state="visible")
                        await dropdown.hover()
                        await self.page.wait_for_timeout(200)
                        await dropdown.click()

                        # Escribir el valor letra por letra
                        for char in value:
                            await self.page.keyboard.type(
                                char, delay=random.randint(50, 150)
                            )
                        await self.page.wait_for_timeout(200)
                        await self.page.keyboard.press("Enter")
                        await self.page.wait_for_timeout(random.randint(500, 1000))

                    elif key in ["price_min", "price_max"]:
                        field = self.page.locator(
                            f"[data-test-id='search-components_advanced-filters_price-filter_input-{'min' if key == 'price_min' else 'max'}']"
                        )
                        await field.fill(str(value))
                        await self.page.wait_for_timeout(200)

                    elif key in ["living_surface_min", "living_surface_max"]:
                        field = self.page.locator(
                            f"[data-test-id='search-components_advanced-filters_living-surface-filter_input-{'min' if key == 'living_surface_min' else 'max'}']"
                        )
                        await field.fill(str(value))
                        await self.page.wait_for_timeout(200)

                    elif key in ["plot_surface_min", "plot_surface_max"]:
                        field = self.page.locator(
                            f"[data-test-id='search-components_advanced-filters_plot-surface-filter_input-{'min' if key == 'plot_surface_min' else 'max'}']"
                        )
                        await field.fill(str(value))
                        await self.page.wait_for_timeout(200)

                    elif key in ["total_surface_min", "total_surface_max"]:
                        field = self.page.locator(
                            f"[data-test-id='search-components_advanced-filters_total-surface-filter_input-{'min' if key == 'total_surface_min' else 'max'}']"
                        )
                        await field.fill(str(value))
                        await self.page.wait_for_timeout(200)

                    elif key in ["rooms_min", "rooms_max"]:
                        field = self.page.locator(
                            f"[data-test-id='search-components_advanced-filters_rooms-filter_input-{'min' if key == 'rooms_min' else 'max'}']"
                        )
                        await field.fill(str(value))
                        await self.page.wait_for_timeout(200)

                    elif key in ["bedrooms_min", "bedrooms_max"]:
                        field = self.page.locator(
                            f"[data-test-id='search-components_advanced-filters_bedrooms-filter_input-{'min' if key == 'bedrooms_min' else 'max'}']"
                        )
                        await field.fill(str(value))
                        await self.page.wait_for_timeout(200)

                    elif key in ["bathrooms_min", "bathrooms_max"]:
                        field = self.page.locator(
                            f"[data-test-id='search-components_advanced-filters_bathrooms-filter_input-{'min' if key == 'bathrooms_min' else 'max'}']"
                        )
                        await field.fill(str(value))
                        await self.page.wait_for_timeout(200)

                    elif key in ["construction_year_min", "construction_year_max"]:
                        field = self.page.locator(
                            f"[data-test-id='search-components_advanced-filters_construction-year-filter_input-{'min' if key == 'construction_year_min' else 'max'}']"
                        )
                        await field.fill(str(value))
                        await self.page.wait_for_timeout(200)

                except Exception as e:
                    logger.warning(f"Error al aplicar filtro {key}: {str(e)}")
                    continue

        # Simular comportamiento humano antes de hacer clic en "Done"
        await self.page.mouse.move(random.randint(100, 500), random.randint(100, 500))
        await self.page.wait_for_timeout(random.randint(1000, 2000))

        # Click "Done" button to apply filters
        done_button = self.page.locator(
            "[data-test-id='search-components_advanced-filters_submit-button']"
        )
        await done_button.hover()
        await self.page.wait_for_timeout(random.randint(500, 1000))
        await done_button.click()

        # Esperar a que los filtros se apliquen
        await self.page.wait_for_timeout(random.randint(2000, 4000))
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
        # Configuración optimizada del navegador con evasión de detección
        browser = await playwright.chromium.launch(
            headless=True,  # Mantener visible para debugging
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",  # Ocultar webdriver
                "--disable-infobars",
                "--window-size=920,480",
                "--start-maximized",
            ],
        )

        # Configuración del contexto con evasión de detección
        context = await browser.new_context(
            viewport={"width": 920, "height": 480},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            java_script_enabled=True,
            ignore_https_errors=True,
            bypass_csp=True,
            permissions=["geolocation"],
            geolocation={
                "latitude": 4.6097,
                "longitude": -74.0817,
            },  # Coordenadas de Bogotá
            locale="es-CO",
        )

        # Configurar timeouts más largos para simular comportamiento humano
        context.set_default_timeout(60000)
        context.set_default_navigation_timeout(60000)

        page = await context.new_page()

        # Inyectar scripts para evadir detección
        await page.add_init_script(
            """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            window.chrome = {
                runtime: {}
            };
        """
        )

        try:
            logger.info("Starting scraper")
            await page.goto(INITIAL_URL, wait_until="domcontentloaded")

            # Simular movimientos aleatorios del mouse
            await page.mouse.move(random.randint(100, 500), random.randint(100, 500))
            await page.wait_for_timeout(random.randint(1000, 2000))

            logger.info(f"Entered {INITIAL_URL}")

            # Manejar cookies con retraso aleatorio
            try:
                cookie_popup = page.locator("#didomi-popup")
                if await cookie_popup.is_visible():
                    await page.wait_for_timeout(random.randint(1000, 2000))
                    cookie_button = page.locator("#didomi-notice-agree-button")
                    await cookie_button.hover()
                    await page.wait_for_timeout(random.randint(500, 1000))
                    await cookie_button.click()
                    logger.info("Cookie banner aceptado")
                    await cookie_popup.wait_for(state="hidden")
            except Exception as e:
                logger.info(f"No se encontró el banner de cookies: {str(e)}")

            # Buscar y llenar el campo de búsqueda con retrasos
            search_input = page.locator(".sc-7856fc0a-2.foWFcA")
            await search_input.wait_for(state="visible")
            await search_input.hover()
            await page.wait_for_timeout(random.randint(500, 1000))

            # Escribir la ubicación letra por letra
            for char in location:
                await search_input.type(char, delay=random.randint(100, 300))
                await page.wait_for_timeout(random.randint(50, 150))

            logger.info("Campo de búsqueda completado")

            # Simular comportamiento humano antes de hacer clic
            search_button = page.locator(".sc-a6c22956-0.fMdhBy.sc-7856fc0a-4.kUdQjI")
            await search_button.wait_for(state="visible")
            await search_button.hover()
            await page.wait_for_timeout(random.randint(500, 1000))

            # Hacer clic y esperar a que la navegación se complete
            async with page.expect_navigation(wait_until="domcontentloaded"):
                await search_button.click()
            logger.info("Botón de búsqueda clickeado")

            # Esperar a que la página se estabilice con tiempo aleatorio
            await page.wait_for_timeout(random.randint(2000, 4000))
            await page.wait_for_load_state("networkidle", timeout=60000)

            # Simular scroll aleatorio
            for _ in range(3):
                await page.mouse.wheel(0, random.randint(100, 300))
                await page.wait_for_timeout(random.randint(500, 1500))

            # Crear una instancia del FilterManager
            filter_manager = FilterManager(page)
            logger.info("filter manager instanciated")

            # Esperar antes de aplicar filtros
            await page.wait_for_timeout(random.randint(2000, 4000))

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
            await page.wait_for_load_state("networkidle", timeout=30000)

            # Obtener numero de propiedades encontradas
            logger.info("waiting for properties to load")
            try:
                # Esperar al contenedor principal de propiedades
                property_container = page.locator(".sc-e5f1eba3-3.cGSWBa")
                await property_container.wait_for(state="visible")

                # Usar un selector más específico para las cards
                property_cards = property_container.locator("article")

                # Verificar si encontramos artículos
                count = await property_cards.count()
                logger.info(f"Número de artículos encontrados: {count}")

                if count == 0:
                    logger.warning("No se encontraron propiedades")
                    return results

                # Procesar las propiedades
                for i in range(count):
                    try:
                        card = property_cards.nth(i)

                        # Verificar si es una propiedad que nos interesa
                        price_element = card.locator(
                            "[data-test-id$='search-components_result-card_price']"
                        )
                        if not await price_element.is_visible():
                            logger.info(
                                f"Propiedad {i+1} no tiene precio visible, saltando..."
                            )
                            continue

                        # Extraer datos básicos
                        property_data = {}

                        # Extraer precio
                        property_data["price"] = await price_element.inner_text()

                        # Extraer ubicación si existe
                        location_element = card.locator("[data-test-id$='_location']")
                        if await location_element.is_visible():
                            property_data["location"] = (
                                await location_element.inner_text()
                            )

                        # Extraer título si existe
                        headline_element = card.locator("[data-test-id$='_headline']")
                        if await headline_element.is_visible():
                            property_data["headline"] = (
                                await headline_element.inner_text()
                            )

                        # Solo agregar estos campos si existen
                        bedrooms_element = card.locator("[data-test-id$='-bedrooms']")
                        if await bedrooms_element.is_visible():
                            property_data["bedrooms"] = (
                                await bedrooms_element.inner_text()
                            )

                        bathrooms_element = card.locator("[data-test-id$='-bathrooms']")
                        if await bathrooms_element.is_visible():
                            property_data["bathrooms"] = (
                                await bathrooms_element.inner_text()
                            )

                        # Intentar obtener la URL si existe
                        link_element = card.locator("a").first
                        if await link_element.is_visible():
                            property_data["url"] = await link_element.get_attribute(
                                "href"
                            )

                        # Limpiar datos
                        property_data = {
                            k: v.strip() if isinstance(v, str) else v
                            for k, v in property_data.items()
                            if v
                        }

                        # Validar datos mínimos (precio y al menos ubicación o título)
                        if property_data.get("price") and (
                            property_data.get("location")
                            or property_data.get("headline")
                        ):
                            results.append(property_data)
                            logger.info(f"Propiedad {i+1} procesada exitosamente")
                        else:
                            logger.info(
                                f"Propiedad {i+1} no cumple con los datos mínimos requeridos"
                            )

                    except Exception as e:
                        logger.error(f"Error procesando propiedad {i+1}: {str(e)}")
                        continue

                    # Pequeña pausa entre propiedades
                    if i % 5 == 0:
                        await page.wait_for_timeout(200)

            except Exception as e:
                logger.error(f"Error al procesar propiedades: {str(e)}")
                raise

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
