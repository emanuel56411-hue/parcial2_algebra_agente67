"""Recorrido mínimo de la interfaz publicada en Vercel con Playwright."""
import argparse
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="https://parcial2algebraagente.vercel.app")
    parser.add_argument("--browser", help="Ruta de Chromium/Brave; omitir para usar el de Playwright.")
    args = parser.parse_args()
    output = Path(__file__).resolve().parents[1] / "docs/screenshots"
    output.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=args.browser)
        page = browser.new_page(viewport={"width": 1440, "height": 960})
        page.goto(args.url, wait_until="networkidle")
        expect(page.get_by_role("heading", name="Decisiones operativas con evidencia matemática.")).to_be_visible()
        expect(page.get_by_role("heading", name="Define tu sistema")).to_be_visible()
        page.screenshot(path=str(output / "08_vercel_profesional.png"), full_page=False)
        page.get_by_role("button", name="Resolver sistema").click()
        expect(page.get_by_text("Solución única", exact=True)).to_be_visible(timeout=30_000)
        expect(page.locator("#metric-det")).to_have_text("-83")
        page.get_by_role("tab", name="Procedimiento").click()
        page.locator("#method").select_option("gauss_jordan")
        page.get_by_role("button", name="Siguiente →").click()
        expect(page.locator("#step-label")).to_have_text("PASO 02")
        page.get_by_role("button", name="Procedimiento completo").click()
        expect(page.locator("#all-steps .all-step")).to_have_count(39)
        page.locator("#all-steps").scroll_into_view_if_needed()
        page.screenshot(path=str(output / "09_vercel_procedimiento.png"), full_page=False)
        page.get_by_role("tab", name="Tutor IA").click()
        expect(page.get_by_role("heading", name="Consulta el análisis con IA")).to_be_visible()
        page.locator("#tab-tutor").scroll_into_view_if_needed()
        page.screenshot(path=str(output / "10_vercel_tutor.png"), full_page=False)
        deliverables = page.get_by_role("heading", name="Entregables del análisis")
        expect(deliverables).to_be_visible()
        page.locator("#deliverables").scroll_into_view_if_needed()
        expect(page.get_by_role("link", name="Informe técnico")).to_have_attribute(
            "href",
            "https://raw.githubusercontent.com/emanuel56411-hue/parcial2_algebra_agente67/main/docs/informe_tecnico_ieee.pdf",
        )
        page.screenshot(path=str(output / "12_vercel_entregables.png"), full_page=False)
        page.set_viewport_size({"width": 390, "height": 844})
        page.evaluate("window.scrollTo(0, 0)")
        if page.evaluate("document.documentElement.scrollWidth > innerWidth + 2"):
            raise AssertionError("La página desborda horizontalmente en móvil")
        page.screenshot(path=str(output / "11_vercel_movil.png"), full_page=False)
        browser.close()
    print("Vercel: interfaz, cálculo, pasos y viewport móvil verificados")


if __name__ == "__main__":
    main()
