import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from playwright.async_api import async_playwright
import asyncio
from typing import Optional, List, Dict, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

#########################################################################
###############################QUERIES###################################
#########################################################################

INITIAL_URL = "https://www.engelvoelkers.com/co/es"

# Variable para la location de búsqueda
location = "Bogota, Colombia"


# Clase para manejar los filtros de propiedades
class FilterManager:
    def __init__(self, page):
        self.page = page
        self.timeout = 10000  # Aumentar timeout a 10 segundos

    async def open_filters(self):
        """Abre la sección de filtros si no está abierta"""
        try:
            # Intento 1: Por el data-test-id específico
            filter_button = self.page.locator(
                "[data-test-id='search-components_filter-bar_advanced-filters-button-active']"
            )
            await filter_button.wait_for(state="visible", timeout=self.timeout)
            await filter_button.click()

        except Exception as e:
            logger.warning(f"Intento 1 de abrir filtros falló: {str(e)}")
            try:
                # Intento 2: Por el span dentro del botón
                filter_button = self.page.locator(
                    "[data-test-id='search-components_filter-bar_advanced-filters-button']"
                )
                await filter_button.wait_for(state="visible", timeout=self.timeout)
                await filter_button.click()
            except Exception as e:
                logger.warning(f"Intento 2 de abrir filtros falló: {str(e)}")
                try:
                    # Intento 3: Por el botón que contiene el SVG y el texto
                    filter_button = self.page.locator(
                        "button:has(svg):has-text('Filtros')"
                    ).first
                    await filter_button.wait_for(state="visible", timeout=self.timeout)
                    await filter_button.click()
                except Exception as e:
                    logger.error(f"Intento 3 de abrir filtros falló: {str(e)}")
                    raise Exception("No se pudo abrir la sección de filtros")

        await self.page.wait_for_load_state("networkidle", timeout=self.timeout)

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
            await type_dropdown.wait_for(state="visible", timeout=5000)
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
            await subtype_dropdown.wait_for(state="visible", timeout=5000)
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
    max_retries = 3
    retry_count = 0
    timeout = 60000  # 60 segundos

    while retry_count < max_retries:
        try:
            logger.info(f"Intento {retry_count + 1} de {max_retries}")
            async with async_playwright() as playwright:
                logger.info("Iniciando navegador...")
                browser = await playwright.chromium.launch(
                    headless=True,
                    args=[
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-accelerated-2d-canvas",
                        "--disable-gpu",
                        "--window-size=1920x1080",
                    ],
                )

                context = await browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                )

                page = await context.new_page()

                try:
                    # Configurar manejo de errores de página
                    page.on(
                        "pageerror",
                        lambda err: logger.error(f"Error en la página: {err}"),
                    )
                    page.on(
                        "console",
                        lambda msg: logger.debug(f"Consola del navegador: {msg.text}"),
                    )

                    logger.info(f"Intentando acceder a {INITIAL_URL}")
                    response = await page.goto(INITIAL_URL, wait_until="networkidle")

                    if not response:
                        raise Exception("No se recibió respuesta al cargar la página")

                    if response.status != 200:
                        raise Exception(
                            f"Error al cargar la página. Código de estado: {response.status}"
                        )

                    logger.info("Página cargada exitosamente")

                    # Verificar si hay un banner de cookies
                    try:
                        logger.info("Verificando banner de cookies...")
                        cookie_button = page.locator(
                            "[id='didomi-notice-agree-button']"
                        )
                        if await cookie_button.is_visible():
                            logger.info("Cerrando banner de cookies...")
                            await cookie_button.click()
                            await page.wait_for_load_state("networkidle")
                    except Exception as e:
                        logger.warning(
                            f"No se encontró banner de cookies o hubo error al cerrarlo: {str(e)}"
                        )

                    # Buscar y llenar el campo de búsqueda
                    logger.info("Buscando campo de búsqueda...")
                    await page.wait_for_selector(
                        "input[placeholder='Ciudad, distrito, código postal o ID de E&V']",
                        state="visible",
                        timeout=timeout,
                    )
                    search_input = page.get_by_placeholder(
                        "Ciudad, distrito, código postal o ID de E&V"
                    )

                    logger.info(f"Escribiendo ubicación: {location}")
                    await search_input.fill("")  # Limpiar el campo primero
                    await search_input.type(location, delay=100)  # Escribir más lento
                    await page.wait_for_timeout(2000)

                    # Buscar y hacer clic en el botón de búsqueda
                    logger.info("Buscando botón de búsqueda...")
                    search_button = page.locator(
                        "button[class='sc-a6c22956-0 fMdhBy sc-7856fc0a-4 kUdQjI']"
                    )

                    if not await search_button.is_visible():
                        raise Exception("No se encontró el botón de búsqueda")

                    logger.info("Haciendo clic en el botón de búsqueda...")

                    # Esperar a que la navegación se complete después del clic
                    async with page.expect_navigation(
                        wait_until="networkidle", timeout=timeout
                    ) as navigation_info:
                        await search_button.click()

                    # Verificar si la navegación fue exitosa
                    navigation_response = await navigation_info.value
                    if not navigation_response:
                        raise Exception("La navegación después del clic no fue exitosa")

                    logger.info("Navegación completada después del clic de búsqueda")

                    # Esperar a que los resultados estén visibles
                    await page.wait_for_selector(
                        "div.sc-e5f1eba3-2", state="visible", timeout=timeout
                    )
                    logger.info("Contenedor de resultados encontrado")

                    # Crear una instancia del FilterManager
                    filter_manager = FilterManager(page)

                    # Aplicar filtros personalizados
                    logger.info("Aplicando filtros...")
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

                    # Esperar a que la página cargue completamente
                    await page.wait_for_load_state("networkidle")
                    await page.wait_for_timeout(2000)

                    # Obtener todas las cards de propiedades
                    logger.info("Buscando cards de propiedades...")
                    property_cards = page.locator(
                        "div.sc-e5f1eba3-2.hRrPnI article[data-test-id^='search-components_result-card_']"
                    )

                    # Esperar a que al menos una card esté visible
                    await property_cards.first.wait_for(
                        state="visible", timeout=timeout
                    )

                    # Obtener el número total de cards
                    count = await property_cards.count()
                    logger.info(f"Se encontraron {count} propiedades")

                    # Iterar sobre cada card
                    for i in range(count):
                        try:
                            card = property_cards.nth(i)
                            logger.info(f"Procesando propiedad {i + 1} de {count}")

                            # Verificar primero si el artículo tiene la información necesaria
                            price_element = card.locator("[data-test-id$='_price']")
                            if not await price_element.is_visible():
                                logger.warning(
                                    f"Propiedad {i + 1} no tiene precio visible, saltando..."
                                )
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

                            property_data = {
                                "location": location,
                                "headline": headline,
                                "price": price,
                                "bedrooms": bedrooms,
                                "bathrooms": bathrooms,
                            }

                            try:
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
                                logger.warning(
                                    f"No se pudo obtener el enlace para la propiedad {i + 1}: {str(e)}"
                                )

                            results.append(property_data)
                            logger.info(f"Propiedad {i + 1} procesada exitosamente")

                        except Exception as e:
                            logger.error(
                                f"Error al procesar la propiedad {i + 1}: {str(e)}"
                            )
                            continue

                    return results

                except Exception as e:
                    logger.error(f"Error durante el scraping: {str(e)}")
                    # Tomar una captura de pantalla para diagnóstico
                    try:
                        screenshot_path = f"error_attempt_{retry_count + 1}.png"
                        await page.screenshot(path=screenshot_path, full_page=True)
                        logger.info(
                            f"Captura de pantalla guardada como {screenshot_path}"
                        )

                        # También guardar el HTML para diagnóstico
                        html_path = f"error_attempt_{retry_count + 1}.html"
                        await page.content().then(
                            lambda content: open(html_path, "w").write(content)
                        )
                        logger.info(f"HTML guardado como {html_path}")
                    except Exception as screenshot_error:
                        logger.error(
                            f"Error al guardar diagnóstico: {str(screenshot_error)}"
                        )
                    raise

                finally:
                    await browser.close()

        except Exception as e:
            retry_count += 1
            logger.warning(f"Intento {retry_count} fallido: {str(e)}")
            if retry_count == max_retries:
                logger.error("Se agotaron los intentos de scraping")
                raise Exception(f"Error después de {max_retries} intentos: {str(e)}")
            await asyncio.sleep(5)  # Esperar antes de reintentar


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
