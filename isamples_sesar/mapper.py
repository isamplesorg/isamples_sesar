from abc import ABC, abstractmethod
import typing

NOT_PROVIDED = "Not Provided"


class AbstractCategoryMapper(ABC):
    _destination: str

    @abstractmethod
    def matches(
        self,
        potential_match: str,
        auxiliary_match: typing.Optional[str] = None,
    ) -> bool:
        """Whether a particular String input matches this category mapper"""
        pass

    def append_if_matched(
        self,
        potential_match: str,
        auxiliary_match: typing.Optional[str] = None,
        categories_list: typing.List[str] = list(),
    ):
        if self.matches(potential_match, auxiliary_match):
            categories_list.append(self._destination)

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, destination):
        self._destination = destination


class AbstractCategoryMetaMapper(ABC):
    _categoriesMappers: list[AbstractCategoryMapper] = []

    @classmethod
    def categories(
        cls,
        source_category: str,
        auxiliary_source_category: typing.Optional[str] = None,
    ):
        categories: list[str] = []
        if source_category is not None:
            for mapper in cls._categoriesMappers:
                mapper.append_if_matched(
                    source_category, auxiliary_source_category, categories
                )
        if len(categories) == 0:
            categories.append(NOT_PROVIDED)
        return categories

    @classmethod
    def categories_mappers(cls) -> list[AbstractCategoryMapper]:
        return []

    def __init_subclass__(cls, **kwargs):
        cls._categoriesMappers = cls.categories_mappers()


class StringConstantCategoryMapper(AbstractCategoryMapper):
    """A mapper that always matches.  Use this as the end of the road."""

    def __init__(
        self,
        destination_category: str,
    ):
        self._destination = destination_category

    def matches(
        self,
        potential_match: str,
        auxiliary_match: typing.Optional[str] = None,
    ) -> bool:
        return True


class StringEqualityCategoryMapper(AbstractCategoryMapper):
    """A mapper that matches iff the potentialMatch exactly matches one of the list of predefined categories"""

    def __init__(
        self,
        categories: list[str],
        destination_category: str,
    ):
        categories = [keyword.lower() for keyword in categories]
        categories = [keyword.strip() for keyword in categories]
        self._categories = categories
        self._destination = destination_category

    def matches(
        self,
        potential_match: str,
        auxiliary_match: typing.Optional[str] = None,
    ) -> bool:
        return potential_match.lower().strip() in self._categories


class StringEndsWithCategoryMapper(AbstractCategoryMapper):
    """A mapper that matches if the potentialMatch ends with the specified string"""

    def __init__(self, ends_with: str, destination_category: str):
        self._endsWith = ends_with.lower().strip()
        self._destination = destination_category

    def matches(
        self,
        potential_match: str,
        auxiliary_match: typing.Optional[str] = None,
    ) -> bool:
        return potential_match.lower().strip().endswith(self._endsWith)


class StringOrderedCategoryMapper(AbstractCategoryMapper):
    """A mapper that runs through a list of mappers and chooses the first one that matches"""

    def __init__(self, submappers: typing.List[AbstractCategoryMapper]):
        self._submappers = submappers

    def matches(
        self,
        potential_match: str,
        auxiliary_match: typing.Optional[str] = None,
    ) -> bool:
        for mapper in self._submappers:
            if mapper.matches(potential_match, auxiliary_match):
                # Note that this isn't thread-safe -- we expect one of these objects per thread
                self.destination = mapper.destination
                return True
        return False


class StringPairedCategoryMapper(AbstractCategoryMapper):
    """A mapper that matches iff the potentialMatch matches both the primaryMatch and secondaryMatch"""

    def __init__(
        self,
        primary_match: str,
        auxiliary_match: str,
        destination_category: str,
    ):
        self._primaryMatch = primary_match.lower().strip()
        self._auxiliaryMatch = auxiliary_match.lower().strip()
        self._destination = destination_category

    def matches(
        self,
        potential_match: str,
        auxiliary_match: typing.Optional[str] = None,
    ) -> bool:
        return (
            potential_match is not None
            and auxiliary_match is not None
            and potential_match.lower().strip() == self._primaryMatch
            and auxiliary_match.lower().strip() == self._auxiliaryMatch
        )
