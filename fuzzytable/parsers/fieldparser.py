"""FieldParser objects do the hard work of figuring out a FieldPattern's best-fit Field."""

# --- Standard Library Imports ------------------------------------------------
from difflib import SequenceMatcher
from typing import List, Optional
import collections

# --- Intra-Package Imports ---------------------------------------------------
from fuzzytable import exceptions
from fuzzytable.patterns import FieldPattern
from fuzzytable.datamodel import Field
from fuzzytable.main.utils import get_repr

# --- Third Party Imports -----------------------------------------------------
# None


# The parser looks once at each field only once.
# It stores the field and it's match ratio here for later reference.
FieldRatio = collections.namedtuple("FieldRatio", "field ratio")


class FieldParser:

    def __init__(self, fieldpattern, fields):

        self.fieldpattern = fieldpattern
        self.fields = fields

        field_ratios = []
        for field in fields:
            ratio = self.calc_ratio(field)
            if ratio == 0:
                continue  # not a good match (ratio likely too low)
            field_ratio = FieldRatio(field, ratio)
            field_ratios.append(field_ratio)
        self.field_ratios = sorted(field_ratios, key=lambda fr: fr.ratio)  # ascending
        # Note: all fields in this list are potential good matches.

    @property
    def bestfit_ratio(self) -> float:
        """Return match ratio with the best-fitting of the remaining fields."""
        bestfit_fieldratio = self.get_bestfit_fieldratio()
        return 0.0 if bestfit_fieldratio is None else bestfit_fieldratio.ratio

    def get_bestfit_fieldratio(self) -> Optional[FieldRatio]:
        # Of all the remaining unmatched Fields, return the best-fit field/ratio tuple

        # Ratio is zero if there are no more fields available
        try:
            bestfit_fieldratio = self.field_ratios[-1]
        except IndexError:
            return None

        # If the best-match field is already taken,
        # remove it from the list and recurse back thru
        if bestfit_fieldratio.field.matched:
            self.field_ratios.pop()
            return self.get_bestfit_fieldratio()

        # Else, return the best-fit field/ratio tuple
        return bestfit_fieldratio

    def calc_ratio(self, field: Field) -> float:
        if self.fieldpattern.approximate_match:
            return self.get_best_ratio(self.fieldpattern.terms, [field.header], min_ratio=self.fieldpattern.min_ratio)
        else:
            for term in self.fieldpattern.terms:
                if term in field.header:
                    return 1.0
            return 0.0

    @staticmethod
    def row_ratio(fieldpatterns: List[FieldPattern], headers_string: str) -> float:
        """Calculate the average ratio for a potential header row"""
        if not fieldpatterns:
            return 0.0
        individual_ratios = (
            FieldParser.fieldpattern_ratio(fieldpattern, headers_string)
            for fieldpattern in fieldpatterns
        )
        total = sum(individual_ratios)
        average = total / len(fieldpatterns)
        return average

    @staticmethod
    def fieldpattern_ratio(fieldpattern: FieldPattern, headers_string: str) -> float:
        if fieldpattern.approximate_match:
            return FieldParser.get_best_ratio(fieldpattern.terms, [headers_string])
        else:
            for term in fieldpattern.terms:
                if term in headers_string:
                    return 1.0
        return 0.0

    @staticmethod
    def get_best_ratio(strings1: List[str], strings2: List[str], min_ratio=0.0) -> float:
        best_ratio = 0.0
        for string1 in strings1:
            for string2 in strings2:
                if string1 == string2:
                    return 1.0
                matcher = SequenceMatcher(None, string1, string2)
                if matcher.quick_ratio() < min_ratio:
                    continue
                ratio = matcher.ratio()
                if ratio < min_ratio:
                    continue
                else:
                    best_ratio = max(best_ratio, ratio)
        return best_ratio

    def assign_bestfit_field(self) -> None:
        bestfit_field: Field = self.get_bestfit_fieldratio().field
        bestfit_field.ratio = self.bestfit_ratio
        bestfit_field.name = self.name

        # Finally, mark as matched
        bestfit_field.matched = True
        self.fieldpattern.matched = True

    @property
    def still_seeking(self):
        if self.fieldpattern.matched:
            return False
        if self.get_bestfit_fieldratio() is None:
            return False
        return True

    @property
    def name(self):
        return self.fieldpattern.name  #pragma: no cover

    def __repr__(self):
        return get_repr(self)  # pragma: no cover

    # @staticmethod
    # def ensure_unique_field_names(fieldpatterns):
    #     counter = collections.Counter(fieldpattern.name for fieldpattern in fieldpatterns)
    #     for name in counter:
    #         if counter[name] > 1:
                # what message should this return?
    #             raise exceptions.InvalidFieldError