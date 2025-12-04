"""
Elasticsearch Query Builder
------------------------------------

This module provides  building Elasticsearch queries in a structured and reusable way.
"""

class ESQuery:
    """Base class for all query components."""

    def to_dict(self):
        raise NotImplementedError


class Match(ESQuery):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def to_dict(self):
        return {"match": {self.field: self.value}}


class Term(ESQuery):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def to_dict(self):
        return {"term": {self.field: self.value}}


class Range(ESQuery):
    def __init__(self, field, **kwargs):
        self.field = field
        self.kwargs = kwargs

    def to_dict(self):
        return {"range": {self.field: self.kwargs}}


class Bool(ESQuery):
    def __init__(self, must=None, should=None, filter=None, must_not=None):
        self.must = must or []
        self.should = should or []
        self.filter = filter or []
        self.must_not = must_not or []

    def to_dict(self):
        result = {"bool": {}}

        if self.must:
            result["bool"]["must"] = [q.to_dict() for q in self.must]
        if self.should:
            result["bool"]["should"] = [q.to_dict() for q in self.should]
        if self.filter:
            result["bool"]["filter"] = [q.to_dict() for q in self.filter]
        if self.must_not:
            result["bool"]["must_not"] = [q.to_dict() for q in self.must_not]

        return result


class QueryBuilder:
    """Utility façade for easier query generation."""

    @staticmethod
    def match(field, value):
        return Match(field, value)

    @staticmethod
    def term(field, value):
        return Term(field, value)

    @staticmethod
    def range(field, **kwargs):
        return Range(field, **kwargs)

    @staticmethod
    def boolean(must=None, should=None, filter=None, must_not=None):
        return Bool(must, should, filter, must_not)
