from fastkit_core.services import AsyncBaseCrudService
from .models import Invoice
from .repository import InvoiceAsyncRepository
from .schemas import InvoiceCreate, InvoiceUpdate, InvoiceResponse
from modules.invoice_items.repository import InvoiceItemRepository

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pathlib import Path
from fastkit_core.i18n import _


class InvoiceService(AsyncBaseCrudService[
    Invoice,
    InvoiceCreate,
    InvoiceUpdate,
    InvoiceResponse
]):
    def __init__(self, session):
        repository = InvoiceAsyncRepository(session)
        self.invoice_item_repository = InvoiceItemRepository(session)
        self.session = session
        super().__init__(repository, response_schema=InvoiceResponse)

    async def create_with_items(self, data: InvoiceCreate) -> InvoiceResponse:
        data_dict = data.model_dump()
        items_data = data_dict.pop('items', [])

        invoice = await self.repository.create(data=data_dict, commit=True)

        for item_data in items_data:
            item_data['invoice_id'] = invoice.id
            await self.invoice_item_repository.create(data=item_data, commit=True)

        await self.update(invoice.id, {
            'pdf_path': str(self.generate(invoice=invoice))
        })

        await self.session.refresh(invoice, attribute_names=['items'])

        return InvoiceResponse.model_validate(invoice)

    def generate(self, invoice: Invoice, templates_dir="templates", output_dir="storage/invoices") -> Path:
        filename = f"invoice-{invoice.id}.pdf"
        env = Environment(loader=FileSystemLoader(templates_dir))
        output_dir = Path(output_dir)
        env.globals['_'] = _
        output_dir.mkdir(parents=True, exist_ok=True)
        template = env.get_template("invoice.html")
        html_content = template.render(invoice=invoice)

        file_path = output_dir / filename
        HTML(string=html_content).write_pdf(target=str(file_path))

        return file_path