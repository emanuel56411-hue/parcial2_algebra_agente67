"""Recorrido mínimo de la interfaz publicada en Vercel con Playwright."""
import argparse

from playwright.sync_api import expect, sync_playwright


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="https://parcial2algebraagente.vercel.app")
    parser.add_argument("--browser", help="Ruta de Chromium/Brave; omitir para usar el de Playwright.")
    args = parser.parse_args()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=args.browser)
        page = browser.new_page(viewport={"width": 1440, "height": 960})
        page.goto(args.url, wait_until="networkidle")
        expect(page.get_by_role("heading", name="No solo llegues al resultado. Entiende cómo.")).to_be_visible()
        expect(page.get_by_role("heading", name="Define tu sistema")).to_be_visible()
        page.get_by_role("button", name="Resolver sistema").click()
        expect(page.get_by_text("Solución única", exact=True)).to_be_visible(timeout=30_000)
        expect(page.locator("#metric-det")).to_have_text("-83")
        page.get_by_role("tab", name="Procedimiento").click()
        page.locator("#method").select_option("gauss_jordan")
        page.get_by_role("button", name="Siguiente →").click()
        expect(page.locator("#step-label")).to_have_text("PASO 02")
        page.set_viewport_size({"width": 390, "height": 844})
        if page.evaluate("document.documentElement.scrollWidth > innerWidth + 2"):
            raise AssertionError("La página desborda horizontalmente en móvil")
        browser.close()
    print("Vercel: interfaz, cálculo, pasos y viewport móvil verificados")


if __name__ == "__main__":
    main()
