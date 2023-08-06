from enum import Enum


class DomainDictionary:
    """
    Domain Map
    """

    DOMAIN_MAP = {"seg": "SYSTEM"}

    @staticmethod
    def get(source_domain: str) -> str:
        return DomainDictionary.DOMAIN_MAP.get(source_domain, "")
