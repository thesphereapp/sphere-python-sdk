from pydantic import BaseModel, Field


class EurRecipient(BaseModel):
    # TODO: add more fields
    # TODO: add example
    id: int = Field(alias="id")


# https://api-docs.transferwise.com/#recipient-accounts-create
class GbpRecipient(BaseModel):
    # TODO: add more fields
    id: int = Field(alias="id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "id": 13967081,
                    "business": None,
                    "profile": 9000,
                    "accountHolderName": "Ann Johnson",
                    "currency": "GBP",
                    "country": "GB",
                    "type": "sort_code",
                    "details": {
                        "address": {
                            "country": None,
                            "countryCode": None,
                            "firstLine": None,
                            "postCode": None,
                            "city": None,
                            "state": None
                        },
                        "email": None,
                        "legalType": "PRIVATE",
                        "accountNumber": "28821822",
                        "sortCode": "231470",
                        "abartn": None,
                        "accountType": None,
                        "bankgiroNumber": None,
                        "ifscCode": None,
                        "bsbCode": None,
                        "institutionNumber": None,
                        "transitNumber": None,
                        "phoneNumber": None,
                        "bankCode": None,
                        "russiaRegion": None,
                        "routingNumber": None,
                        "branchCode": None,
                        "cpf": None,
                        "cardNumber": None,
                        "idType": None,
                        "idNumber": None,
                        "idCountryIso3": None,
                        "idValidFrom": None,
                        "idValidTo": None,
                        "clabe": None,
                        "swiftCode": None,
                        "dateOfBirth": None,
                        "clearingNumber": None,
                        "bankName": None,
                        "branchName": None,
                        "businessNumber": None,
                        "province": None,
                        "city": None,
                        "rut": None,
                        "token": None,
                        "cnpj": None,
                        "payinReference": None,
                        "pspReference": None,
                        "orderId": None,
                        "idDocumentType": None,
                        "idDocumentNumber": None,
                        "targetProfile": None,
                        "taxId": None,
                        "iban": None,
                        "bic": None,
                        "IBAN": None,
                        "BIC": None,
                        "interacAccount": None
                    },
                    "user": 111,
                    "active": True,
                    "ownedByCustomer": True
                }
        }


class UsdRecipient(BaseModel):
    # TODO: add more fields
    # TODO: add example
    id: int = Field(alias="id")
