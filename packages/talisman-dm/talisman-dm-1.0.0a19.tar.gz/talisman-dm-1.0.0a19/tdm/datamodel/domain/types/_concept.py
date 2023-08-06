from dataclasses import dataclass

from tdm.abstract.datamodel import AbstractDomainType, Identifiable


@dataclass(frozen=True)
class AbstractConceptType(Identifiable, AbstractDomainType):
    pass


@dataclass(frozen=True)
class ConceptType(AbstractConceptType):
    pass


@dataclass(frozen=True)
class DocumentType(AbstractConceptType):
    pass


#  following classes could be removed after v0 support stop

@dataclass(frozen=True)
class AccountType(AbstractConceptType):
    pass


@dataclass(frozen=True)
class PlatformType(AbstractConceptType):
    pass
