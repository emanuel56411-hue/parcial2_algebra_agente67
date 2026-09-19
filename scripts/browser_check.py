"""Comprueba una web YA iniciada y conserva capturas reales.

python scripts/browser_check.py --url http://localhost:8501 --browser /ruta/al/navegador
Requiere playwright. No inicia ni detiene el servidor Streamlit.
"""
import argparse
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scenarios import SCENARIOS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8501")
    parser.add_argument("--browser", help="Ejecutable Chromium/Brave; si se omite usa Chromium de Playwright.")
    args = parser.parse_args()
    output = ROOT / "docs/screenshots"
    output.mkdir(parents=True, exist_ok=True)
    checks = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=args.browser)
        context = browser.new_context(viewport={"width": 1440, "height": 1050}, device_scale_factor=1)
        page = context.new_page()
        page.goto(args.url)
        expect(page.get_by_role("heading", name="Cada resultado, con su procedimiento.")).to_be_visible(timeout=30000)
        expect(page.get_by_role("button", name="Resolver sistema")).to_be_enabled()
        page.screenshot(path=str(output / "01_inicio.png"), full_page=True)

        def scenario(key):
            name, description = SCENARIOS[key]
            selector = page.get_by_role("combobox", name="Escenario", exact=True)
            selector.click()
            selector.fill(name)
            page.get_by_role("option", name=name, exact=True).click()
            expect(page.get_by_text(description, exact=True)).to_be_visible()
            expect(page.locator(f".st-key-editor_Escenarios_{key}")).to_be_visible()
            expect(page.get_by_role("heading", name="02 · Resultado del análisis")).to_have_count(0)
            page.get_by_role("button", name="Resolver sistema").click()
            expect(page.get_by_role("heading", name="02 · Resultado del análisis")).to_be_visible(timeout=15000)
            expect(page.get_by_test_id("stException")).to_have_count(0)

        scenario("compatible")
        expect(page.get_by_text("Solución única", exact=True)).to_be_visible()
        page.get_by_role("heading", name="02 · Resultado del análisis").scroll_into_view_if_needed()
        page.screenshot(path=str(output / "02_plan_compatible.png"), full_page=True)
        checks.append("Escenario compatible y gráfico visibles")
        page.get_by_role("tab", name="Tutor IA", exact=True).click()
        expect(page.get_by_role("heading", name="Pregunta sobre tu resultado")).to_be_visible()
        expect(page.get_by_test_id("stChatInput")).to_be_visible()
        page.screenshot(path=str(output / "02b_tutor_ia.png"), full_page=True)
        checks.append("Tutor IA visible sin enviar consultas a OpenAI")
        page.get_by_role("tab", name="Procedimiento", exact=True).click()
        page.get_by_test_id("stSelectbox").nth(1).get_by_role("combobox").click()
        page.get_by_role("option", name="Gauss-Jordan", exact=True).click()
        page.locator(".st-key-next_gauss_jordan").get_by_role("button").click()
        expect(page.get_by_text("PASO 02", exact=False)).to_be_visible()
        page.get_by_role("heading", name="02 · Resultado del análisis").scroll_into_view_if_needed()
        page.screenshot(path=str(output / "03_procedimiento.png"), full_page=True)
        checks.append("Navegación de operaciones Gauss-Jordan")
        page.get_by_role("tab", name="Resumen", exact=True).click()
        scenario("scarcity")
        expect(page.get_by_text("Plan de producción inalcanzable por restricción de materias primas.", exact=True)).to_be_visible()
        page.screenshot(path=str(output / "04_escasez.png"), full_page=True)
        checks.append("Alerta de escasez visible")
        scenario("singular")
        expect(page.get_by_text("Sin solución", exact=True)).to_be_visible()
        page.screenshot(path=str(output / "05_singular.png"), full_page=True)
        checks.append("Diagnóstico incompatible visible")
        scenario("infinite")
        expect(page.get_by_text("Infinitas soluciones", exact=True)).to_be_visible()
        page.screenshot(path=str(output / "06_infinitas.png"), full_page=True)
        checks.append("Familia paramétrica visible")
        page.set_viewport_size({"width": 390, "height": 844})
        page.screenshot(path=str(output / "07_movil.png"), full_page=True)
        if page.evaluate("document.documentElement.scrollWidth > innerWidth + 2"):
            raise AssertionError("La página desborda horizontalmente en móvil")
        checks.append("Viewport móvil sin desbordamiento de la página")
        browser.close()
    (ROOT / "docs/logs/browser.json").write_text(json.dumps({"passed": True, "checks": checks}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("Verificaciones del navegador:", len(checks))


if __name__ == "__main__":
    main()
