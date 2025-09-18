from dataclasses import dataclass
from decimal import Decimal
from crm.models import Company, Deal


@dataclass
class DealCreateDTO:
    title: str
    amount: Decimal
    stage: str
    company: Company


class DealsService:
    @staticmethod
    def create(user, dto: DealCreateDTO) -> Deal:
        return Deal.objects.create(
            user=user,
            company=dto.company,
            title=dto.title,
            amount=dto.amount,
            stage=dto.stage,
        )
