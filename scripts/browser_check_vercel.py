"""Recorrido mínimo de la interfaz publicada en Vercel con Playwright."""
import argparse
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="https://parcial2algebraagente.vercel.app")
    parser.add_argument("--browser", help="Ruta de Chromium/Brave; omitir para usar el de Playwright.")
    parser.add_argument("--theme-only", action="store_true", help="Valida únicamente cambio y persistencia del tema.")
    args = parser.parse_args()
    output = Path(__file__).resolve().parents[1] / "docs/screenshots"
    output.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=args.browser)
        page = browser.new_page(viewport={"width": 1440, "height": 960})
        page.goto(args.url, wait_until="networkidle")
        page.evaluate("localStorage.setItem('techchip-theme', 'light')")
        page.reload(wait_until="networkidle")
        expect(page.get_by_role("heading", name="Del sistema matricial a una decisión defendible.")).to_be_visible()
        expect(page.get_by_role("heading", name="Define y resuelve el sistema")).to_be_visible()
        page.screenshot(path=str(output / "14_tailwind_escritorio_claro.png"), full_page=True)
        theme_toggle = page.locator("#theme-toggle")
        if not theme_toggle.count():
            theme_toggle = page.get_by_role("button", name="Cambiar tema")
        theme_toggle.click()
        page.get_by_role("menuitem", name="Oscuro").click()
        expect(page.locator("html")).to_have_class("dark")
        page.wait_for_timeout(300)
        page.screenshot(path=str(output / "16_tailwind_escritorio_oscuro.png"), full_page=True)
        page.reload(wait_until="networkidle")
        expect(page.locator("html")).to_have_class("dark")
        page.get_by_role("button", name="Cambiar tema").click()
        page.get_by_role("menuitem", name="Claro").click()
        expect(page.locator("html")).to_have_class("light")
        if args.theme_only:
            page.set_viewport_size({"width": 390, "height": 844})
            if page.evaluate("document.scrollingElement.scrollWidth > innerWidth + 2"):
                raise AssertionError("El selector de tema desborda horizontalmente en móvil")
            browser.close()
            print("Tema claro/oscuro, persistencia y viewport móvil verificados")
            return
        page.locator("#solve").click()
        expect(page.get_by_text("Solución única", exact=True).first).to_be_visible(timeout=30_000)
        expect(page.get_by_text("Prueba 2 · Comprobación por sustitución directa", exact=True)).to_be_visible()
        expect(page.get_by_text("E = max |A·X − B| = 0 < 10⁻⁶", exact=True)).to_be_visible()
        page.get_by_role("button", name="Siguiente").first.click()
        expect(page.get_by_text("Paso 2 de", exact=False)).to_be_visible()
        all_steps = page.get_by_role("switch", name="Ver todos los pasos")
        all_steps.check()
        expect(all_steps).to_be_checked()
        page.screenshot(path=str(output / "15_tailwind_procedimiento_claro.png"), full_page=False)
        page.get_by_role("button", name="Tutor IA").click()
        expect(page.get_by_role("dialog", name="Tutor de IA · Matrices")).to_be_visible()
        page.keyboard.press("Escape")

        def choose_scenario(label: str) -> None:
            selector = page.get_by_label("Escenario preparado")
            selector.click()
            page.get_by_role("option", name=label, exact=True).click()
            expect(selector).to_contain_text(label)
            page.locator("#solve").click()

        choose_scenario("Prueba 1 · Vector esperado")
        expect(page.get_by_text("E = max |A·X − B| = 0 < 10⁻⁶", exact=True)).to_be_visible(timeout=30_000)
        choose_scenario("Prueba 3 · Escasez B₃ = 100")
        expect(page.get_by_text("Plan de producción inalcanzable por restricción de materias primas", exact=False).first).to_be_visible(timeout=30_000)
        choose_scenario("Prueba 4A · Singular sin solución")
        expect(page.get_by_text("Prueba 4 · Verificación de singularidad por rangos", exact=True)).to_be_visible(timeout=30_000)
        expect(page.get_by_text("Los rangos distintos prueban que no existe solución.", exact=True)).to_be_visible()
        choose_scenario("Prueba 4B · Singular con infinitas")
        expect(page.get_by_text("Infinitas soluciones", exact=True).first).to_be_visible(timeout=30_000)
        expect(page.get_by_text("Los rangos iguales menores que n prueban que hay variables libres.", exact=True)).to_be_visible()

        page.set_viewport_size({"width": 390, "height": 844})
        page.evaluate("window.scrollTo(0, 0)")
        if page.evaluate("document.scrollingElement.scrollWidth > innerWidth + 2"):
            raise AssertionError("La página desborda horizontalmente en móvil")
        page.screenshot(path=str(output / "17_tailwind_movil_claro.png"), full_page=True)
        page.get_by_role("button", name="Cambiar tema").click()
        page.get_by_role("menuitem", name="Oscuro").click()
        expect(page.locator("html")).to_have_class("dark")
        page.wait_for_timeout(300)
        page.screenshot(path=str(output / "18_tailwind_movil_oscuro.png"), full_page=True)
        browser.close()
    print("Vercel: interfaz, cálculo, pasos y viewport móvil verificados")


if __name__ == "__main__":
    main()
