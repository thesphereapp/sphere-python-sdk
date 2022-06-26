import enum


class TransferPurpose(enum.Enum):
    PURCHASE_PROPERTY = "verification.transfers.purpose.purchase.property"
    PAY_BILLS = "verification.transfers.purpose.pay.bills"
    PAY_MORTGAGE = "verification.transfers.purpose.mortgage"
    STUDYING_EXPENSES = "verification.transfers.purpose.pay.tuition"
    SENDING_TO_FAMILY = "verification.transfers.purpose.send.to.family"
    LIVING_EXPENSES = "verification.transfers.purpose.living.expenses"
    OTHER = "verification.transfers.purpose.other"


class TransferPurposeSubTransferPurpose(enum.Enum):
    INTERPRETATION_SERVICE = "verification.sub.transfers.purpose.pay.interpretation.service"
    TRANSLATION_SERVICE = "verification.sub.transfers.purpose.pay.translation.service"
    HUMAN_RESOURCE_SERVICE = "verification.sub.transfers.purpose.pay.human.resource.service"
    ESTATE_AGENCY_SERVICE = "verification.sub.transfers.purpose.pay.estate.agency.service"
    SOFTWARE_DEVELOPMENT_SERVICE = "verification.sub.transfers.purpose.pay.software.development.service"
    WEB_DESIGN_OR_DEVELOPMENT_SERVICE = "verification.sub.transfers.purpose.pay.web.design.or.development.service"
    DRAFTING_LEGAL_SERVICE = "verification.sub.transfers.purpose.pay.drafting.legal.service"
    LEGAL_RELATED_CERTIFICATION_SERVICE = "verification.sub.transfers.purpose.pay.legal.related.certification.service"
    ACCOUNTING_SERVICE = "verification.sub.transfers.purpose.pay.accounting.service"
    TAX_SERVICE = "verification.sub.transfers.purpose.pay.tax.service"
    ARCHITECTURAL_DECORATION_DESIGN_SERVICE = "verification.sub.transfers.purpose.pay.architectural.decoration.design.service"
    ADVERTISING_SERVICE = "verification.sub.transfers.purpose.pay.advertising.service"
    MARKET_RESEARCH_SERVICE = "verification.sub.transfers.purpose.pay.marget.research.service"
    EXHIBITION_BOOTH_SERVICE = "verification.sub.transfers.purpose.pay.exhibition.booth.service"
