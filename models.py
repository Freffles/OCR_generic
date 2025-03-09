from dataclasses import dataclass, asdict
from typing import List

@dataclass
class LineItem:
    serviceDate: str
    serviceCode: str
    quantity: float
    unitPrice: float
    lineTotal: float
    serviceDescription: str

@dataclass
class Invoice:
    invoiceNumber: str
    invoiceDate: str
    dueDate: str
    totalAmount: float
    vendor: dict  # e.g., {"name": "Vendor Name"}
    participant: dict  # e.g., {"name": "Participant Name"}
    lineItems: List[LineItem]
