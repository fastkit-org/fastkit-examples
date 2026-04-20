import asyncio
import random
import sys
import os

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from fastkit_core.database import init_async_database, get_async_db_manager, AsyncRepository
from fastkit_core.config import ConfigManager

# All related models must be imported before SQLAlchemy mapper initializes.
from modules.clients.models import Clients  # noqa
from modules.invoices.models import Invoice  # noqa
from modules.invoice_items.models import InvoiceItem  # noqa
from modules.products.models import Product  # noqa

configuration = ConfigManager(modules=['app', 'database'])
init_async_database(configuration)

CATEGORIES = [
    ("WEB",  "Web Development",      "Webentwicklung",         "Desarrollo web"),
    ("API",  "API Development",       "API-Entwicklung",        "Desarrollo API"),
    ("MOB",  "Mobile Development",    "Mobile Entwicklung",     "Desarrollo móvil"),
    ("CLD",  "Cloud Services",        "Cloud-Dienste",          "Servicios cloud"),
    ("DEV",  "DevOps",                "DevOps",                 "DevOps"),
    ("DSN",  "Design",                "Design",                 "Diseño"),
    ("SEO",  "SEO & Marketing",       "SEO & Marketing",        "SEO y Marketing"),
    ("CON",  "Consulting",            "Beratung",               "Consultoría"),
    ("SUP",  "Support",               "Support",                "Soporte"),
    ("SEC",  "Security",              "Sicherheit",             "Seguridad"),
    ("DAT",  "Data & Analytics",      "Daten & Analytik",       "Datos y análisis"),
    ("AI",   "AI & Machine Learning", "KI & Maschinelles Lernen","IA y aprendizaje"),
    ("INT",  "Integrations",          "Integrationen",          "Integraciones"),
    ("TST",  "Testing & QA",          "Testing & QA",           "Testing y QA"),
    ("DOC",  "Documentation",         "Dokumentation",          "Documentación"),
    ("TRN",  "Training",              "Training",               "Capacitación"),
    ("MIG",  "Migration",             "Migration",              "Migración"),
    ("AUD",  "Audit",                 "Audit",                  "Auditoría"),
    ("OPT",  "Optimization",          "Optimierung",            "Optimización"),
    ("UX",   "UX Research",           "UX-Forschung",           "Investigación UX"),
]

SERVICE_TIERS = [
    ("basic",       "Basic",       "Basis",       "Básico",      0.5),
    ("standard",    "Standard",    "Standard",    "Estándar",    1.0),
    ("professional","Professional","Professionell","Profesional", 2.0),
    ("enterprise",  "Enterprise",  "Enterprise",  "Empresarial", 4.0),
    ("premium",     "Premium",     "Premium",     "Premium",     6.0),
]

BASE_PRICES = [99, 149, 199, 299, 399, 499, 599, 799, 999, 1299, 1499, 1999, 2499, 2999, 3999]

BATCH_SIZE = 1_000
TOTAL = 100_000


def _generate_products(count: int) -> list[dict]:
    products = []
    for i in range(1, count + 1):
        cat_code, cat_en, cat_de, cat_es = random.choice(CATEGORIES)
        tier_slug, tier_en, tier_de, tier_es, multiplier = random.choice(SERVICE_TIERS)
        base_price = random.choice(BASE_PRICES)
        price = round(base_price * multiplier, 2)
        slug = f"{cat_code.lower()}-{tier_slug}-{i:06d}"
        sku = f"SVC-{cat_code}-{i:06d}"

        products.append({
            "sku": sku,
            "slug": slug,
            "name": {
                "en": f"{cat_en} — {tier_en} Package {i:06d}",
                "de": f"{cat_de} — {tier_de} Paket {i:06d}",
                "es": f"{cat_es} — Paquete {tier_es} {i:06d}",
            },
            "description": {
                "en": f"{tier_en} tier {cat_en.lower()} service package. Includes standard deliverables and support.",
                "de": f"{tier_de}-Tier {cat_de.lower()} Servicepaket. Enthält Standardleistungen und Support.",
                "es": f"Paquete de servicio {cat_es.lower()} de nivel {tier_es}. Incluye entregables estándar y soporte.",
            },
            "price": price,
            "stock": 999,
            "is_active": random.random() > 0.05,  # 95% active
        })
    return products


class ProductSeeder:
    def run(self) -> None:
        asyncio.run(self._seed())

    async def _seed(self) -> None:
        manager = get_async_db_manager()
        async with manager.session() as session:
            repo = AsyncRepository(Product, session)

            existing = await repo.count()
            if existing >= TOTAL:
                print(f"  → ProductSeeder: skipped ({existing} products already exist)")
                return

            remaining = TOTAL - existing
            print(f"  → ProductSeeder: generating {remaining} products in batches of {BATCH_SIZE}...")

            data = _generate_products(remaining)

            for batch_start in range(0, len(data), BATCH_SIZE):
                batch = data[batch_start:batch_start + BATCH_SIZE]
                await repo.create_many(batch)
                inserted = min(batch_start + BATCH_SIZE, len(data))
                print(f"     {inserted}/{remaining} inserted...")

            print(f"  → ProductSeeder: done — {remaining} products inserted")
