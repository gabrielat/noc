# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Clickhouse models
# ----------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import, print_function
import hashlib
from collections import OrderedDict

# Third-party modules
import six

# NOC modules
from .fields import BaseField, NestedField
from .connect import connection
from noc.core.bi.query import to_sql, escape_field
from noc.config import config
from noc.sa.models.useraccess import UserAccess
from noc.sa.models.managedobject import ManagedObject
from noc.core.backport.time import perf_counter

__all__ = ["Model", "NestedModel"]


class ModelBase(type):
    def __new__(mcs, name, bases, attrs):
        cls = type.__new__(mcs, name, bases, attrs)
        cls._fields = {}
        cls._display_fields = OrderedDict()
        cls._model_field = {}
        cls._meta = ModelMeta(
            engine=getattr(cls.Meta, "engine", None),
            db_table=getattr(cls.Meta, "db_table", None),
            description=getattr(cls.Meta, "description", None),
            sample=getattr(cls.Meta, "sample", False),
            tags=getattr(cls.Meta, "tags", None),
            managed=getattr(cls.Meta, "managed", True),
        )
        for k in attrs:
            if isinstance(attrs[k], BaseField):
                attrs[k].contribute_to_class(cls, k)
                cls._model_field[k] = attrs[k]
                cls._model_field[k].name = k
        cls._fields_order = sorted(cls._fields, key=lambda x: cls._fields[x].field_number)
        for f in sorted(cls._model_field, key=lambda x: cls._model_field[x].field_number):
            cls._display_fields[f] = cls._model_field[f]
            cls._display_fields[f].name = f
        return cls


class ModelMeta(object):
    def __init__(
        self, engine=None, db_table=None, description=None, sample=False, tags=None, managed=True
    ):
        self.engine = engine
        self.db_table = db_table
        self.description = description
        self.sample = sample
        self.tags = tags
        self.managed = managed


class Model(six.with_metaclass(ModelBase)):
    class Meta(object):
        engine = None
        db_table = None
        description = None
        sample = False
        tags = None
        managed = True

    def __init__(self, **kwargs):
        self.values = kwargs

    @classmethod
    def _get_db_table(cls):
        return cls._meta.db_table

    @classmethod
    def _get_raw_db_table(cls):
        if config.clickhouse.cluster:
            return "raw_%s" % cls._meta.db_table
        else:
            return cls._meta.db_table

    @classmethod
    def wrap_table(cls, table_name):
        class WrapClass(Model):
            class Meta(object):
                db_table = table_name

        return WrapClass

    @classmethod
    def get_create_sql(cls):
        r = ["CREATE TABLE IF NOT EXISTS %s (" % cls._get_raw_db_table()]
        r += [",\n".join(cls._fields[f].get_create_sql() for f in cls._fields_order)]
        r += [") ENGINE = %s;" % cls._meta.engine.get_create_sql()]
        return "\n".join(r)

    @classmethod
    def get_create_distributed_sql(cls):
        """
        Get CREATE TABLE for Distributed engine
        :return:
        """
        return (
            "CREATE TABLE IF NOT EXISTS %s "
            "AS %s "
            "ENGINE = Distributed('%s', '%s', '%s')"
            % (
                cls._meta.db_table,
                cls._get_raw_db_table(),
                config.clickhouse.cluster,
                config.clickhouse.db,
                cls._get_raw_db_table(),
            )
        )

    @classmethod
    def to_json(cls, **kwargs):
        """
        Convert dict of kwargs to JSON-serializeable dict

        :param kwargs:
        :return:
        """
        return {f: cls._model_field[f].to_json(kwargs[f]) for f in kwargs}

    @classmethod
    def to_python(cls, row, **kwargs):
        r = {}
        for num, f in enumerate(cls._display_fields):
            # print(num, f)
            r[f] = cls._model_field[f].to_python(row[num])
        return r

    @classmethod
    def ensure_table(cls, connect=None):
        """
        Check table is exists
        :param connect:
        :return: True, if table has been altered, False otherwise
        """

        def ensure_columns(table_name):
            c = False
            # Alter when necessary
            existing = {}
            for name, type in ch.execute(
                """
                SELECT name, type
                FROM system.columns
                WHERE
                  database=%s
                  AND table=%s
                """,
                [config.clickhouse.db, table_name],
            ):
                existing[name] = type
            after = None
            for f in cls._fields_order:
                if f not in existing:
                    ch.execute(
                        post="ALTER TABLE %s ADD COLUMN %s AFTER %s"
                        % (table_name, cls._fields[f].get_create_sql(), after)
                    )
                    c = True
                if "." in f:
                    # For Nested field
                    c_type = "Array(%s)" % cls._fields[f].get_db_type()
                else:
                    c_type = cls._fields[f].get_db_type()
                if f in existing and existing[f] != c_type:
                    print(
                        "Warning! Type mismatch for column %s: %s <> %s" % (f, existing[f], c_type)
                    )
                    print(
                        "Set command manually: ALTER TABLE %s MODIFY COLUMN %s %s"
                        % (table_name, f, c_type)
                    )
                after = f
            return c

        changed = False
        if not cls._meta.managed:
            return False
        ch = connect or connection()
        if not ch.has_table(cls._get_raw_db_table()):
            # Create new table
            ch.execute(post=cls.get_create_sql())
            if config.clickhouse.cluster:
                # Create distributed
                ch.execute(post=cls.get_create_sql())
            changed = True
        else:
            changed |= ensure_columns(cls._get_raw_db_table())
        # Check for distributed table
        if config.clickhouse.cluster:
            if not ch.has_table(cls._meta.db_table):
                ch.execute(post=cls.get_create_distributed_sql())
                changed = True
            else:
                changed |= ensure_columns(cls._meta.db_table)
        return changed

    @classmethod
    def transform_query(cls, query, user):
        """
        Transform query, possibly applying access restrictions
        :param query:
        :param user:
        :return: query dict or None if access denied
        """
        if not user or user.is_superuser:
            return query  # No restrictions
        if query["datasource"].startswith("dictionaries."):
            return query  # To dictionaries
        # Get user domains
        domains = UserAccess.get_domains(user)
        # Resolve domains against dict
        mos_bi = [
            int(bi_id)
            for bi_id in ManagedObject.objects.filter(
                administrative_domain__in=domains
            ).values_list("bi_id", flat=True)
        ]
        filter = query.get("filter", {})
        dl = len(mos_bi)
        if not dl:
            return None
        elif dl == 1:
            q = {"$eq": [{"$field": "managed_object"}, mos_bi]}
        else:
            q = {"$in": [{"$field": "managed_object"}, mos_bi]}
        if filter:
            query["filter"] = {"$and": [query["filter"], q]}
        else:
            query["filter"] = q
        return query

    @classmethod
    def query(cls, query, user=None, dry_run=False):
        """
        Execute query and return result
        :param query: dict of
            "fields": list of dicts
                *expr -- field expression
                *alias -- resulting name
                *group -- nth field in GROUP BY expression, starting from 0
                *order -- nth field in ORDER BY expression, starting from 0
                *desc -- sort in descending order, if true
            "filter": expression
            "having": expression
            "limit": N -- limit to N rows
            "offset": N -- skip first N rows
            "sample": 0.0-1.0 -- randomly select rows
            @todo: group by
            @todo: order by
        :param user: User doing query
        :param dry_run: Do not query, only return it.
        :return:
        """
        # Get field expressions
        fields = query.get("fields", [])
        if not fields:
            return None
        transformed_query = cls.transform_query(query, user)
        fields_x = []
        aliases = []
        group_by = {}
        order_by = {}
        for i, f in enumerate(fields):
            if isinstance(f["expr"], six.string_types):
                default_alias = f["expr"]
                f["expr"] = {"$field": f["expr"]}
            else:
                default_alias = "f%04d" % i
            alias = f.get("alias", default_alias)
            if not f.get("hide"):
                aliases += [alias]
                fields_x += ["%s AS %s" % (to_sql(f["expr"], cls), escape_field(alias))]
            if "group" in f:
                group_by[int(f["group"])] = alias
            if "order" in f:
                if "desc" in f and f["desc"]:
                    order_by[int(f["order"])] = "%s DESC" % alias
                else:
                    order_by[int(f["order"])] = alias
        if transformed_query is None:
            # Access denied
            r = []
            dt = 0.0
            sql = ["SELECT %s FROM %s WHERE 0 = 1" % (", ".join(fields_x), cls._get_db_table())]
        else:
            # Get where expressions
            filter_x = to_sql(transformed_query.get("filter", {}))
            filter_h = to_sql(transformed_query.get("having", {}))
            # Generate SQL
            sql = ["SELECT "]
            sql += [", ".join(fields_x)]
            sql += ["FROM %s" % cls._get_db_table()]
            sample = query.get("sample")
            if sample:
                sql += ["SAMPLE %s" % float(sample)]
            if filter_x:
                sql += ["WHERE %s" % filter_x]
            # GROUP BY
            if group_by:
                sql += ["GROUP BY %s" % ", ".join(group_by[v] for v in sorted(group_by))]
            # HAVING
            if filter_h:
                sql += ["HAVING %s" % filter_h]
            # ORDER BY
            if order_by:
                sql += ["ORDER BY %s" % ", ".join(order_by[v] for v in sorted(order_by))]
            # LIMIT
            if "limit" in query:
                if "offset" in query:
                    sql += ["LIMIT %d, %d" % (query["offset"], query["limit"])]
                else:
                    sql += ["LIMIT %d" % query["limit"]]
            sql = " ".join(sql)
            # Execute query
            ch = connection()
            t0 = perf_counter()
            if dry_run:
                return sql
            r = ch.execute(sql)
            dt = perf_counter() - t0
        return {"fields": aliases, "result": r, "duration": dt, "sql": sql}


class NestedModel(Model):
    @classmethod
    def get_create_sql(cls):
        return ",\n".join(cls._fields[f].get_create_sql() for f in cls._fields_order)
