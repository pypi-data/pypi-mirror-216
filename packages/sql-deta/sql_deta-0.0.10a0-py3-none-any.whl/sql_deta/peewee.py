"""
"""

from typing import Iterable, List, Mapping, Sequence, Union

from deta import Base as DetaTable
from deta import Deta
from more_itertools import chunked

from peewee import Model as PeeweeModel


class PeeweeDetaMixin:
    """Mixin do magic"""

    class Meta:
        deta = None
        mirroring: bool = False

    def __del__(self):
        """destructor

        if Meta.mirroring is True:
            self.dump() to deta.Base(Meta.table_name)
        """
        # self._meta.get("mirroring", None)
        # print("destructor", self._meta.get("mirroring", None))
        # print("destructor", hasattr(self._meta, "mirroring"))
        if hasattr(self._meta, "mirroring") and self._meta.mirroring:
            self.dump()
        pass

    @classmethod
    def create_table(cls, safe=True, **options) -> None:
        super().create_table(safe=True, **options)
        if hasattr(cls._meta, "mirroring") and cls._meta.mirroring:
            cls.load()
        pass

    @classmethod
    def __deta_table__(cls) -> DetaTable:
        """
        return deta.Base(Meta.table_name)

        raise AttributeError
        """
        # print(cls._meta.deta.Base(cls._meta.table_name))
        try:
            return cls._meta.deta.Base(cls._meta.table_name)
        except Exception as e:
            print("`Meta.deta=deta.Deta(DETA_KEY)` require. Error:", e.message)
            raise AttributeError

    @classmethod
    def __put__(cls, __data: dict, key: str = None) -> None:
        """
        write 1 row to deta_table
        """
        key = str(key or __data[cls._meta.primary_key.name])
        __data.update(key=key)
        # print('PUT', cls._meta.table_name, cls._meta.primary_key.name, key, __data)
        # {k: v for k, v in self.__data__.items() if k in df}, key = str(self._pk)
        cls.__deta_table__().put(__data) if __data else ...
        pass

    @classmethod
    def __put_many__(cls, __data: Iterable = None) -> None:
        """
        write numerous rows to deta_table in chucnks of 25
        """
        __data = map(
            lambda item: dict(**item, key=str(item[cls._meta.primary_key.name])), __data
        )
        dt = cls.__deta_table__()
        map(lambda ch: dt.put_many, chunked(__data, 25))

        pass

    @classmethod
    def __get_many__(cls, __query=None) -> List[dict]:
        """
        @deprecated
        """
        dt = cls.__deta_table__()
        res = dt.fetch(query=__query, limit=1000, last=None)
        items = {}
        while True:
            items += res.items
            if res.last:
                res = dt.fetch(query=__query, limit=1000, last=res.last)
            else:
                break
        #   итератор в методе __fetch__
        return items

    @classmethod
    def __fetch__(cls, __query=None) -> Iterable:
        """bulk read rows from deta_table in chucnks of 1000

        return Rows Generator
        """
        dt = cls.__deta_table__()
        res = dt.fetch(query=__query, limit=1000, last=None)
        while True:
            yield from res.items  #   <-- return Generator
            if res.last:
                res = dt.fetch(query=__query, limit=1000, last=res.last)
            else:
                break
        pass

    @classmethod
    def load(cls) -> None:
        """
        upload from Deta to RDB
        """

        cls.insert_many(
            map(
                lambda item: dict(
                    item, **{cls._meta.primary_key.name: item.pop("key")}
                ),
                cls.__fetch__(),
            )
        ).execute()
        pass

    @classmethod
    def dump(cls) -> None:
        """
        unload from RDB to Deta
        """

        # cls.__put_many__(cls.select().dicts())
        cls.__put_many__((item for item in cls.select().dicts()))
        pass

    def save(self, force_insert=False, only=None) -> None:
        # pk_field = self._meta.primary_key
        # pk_value = self._pk
        # pk_deta = "key"

        ret = super().save(force_insert, only)

        if self._meta.primary_key is False:
            return ret

        df = only or self.dirty_fields
        if force_insert:
            __data = self.__data__.copy()
        else:
            __data = {k: v for k, v in self.__data__.items() if k in df}

        self.__put__(__data, key=str(self._pk))

        return ret

    """
    @classmethod
    def update(cls, __data=None, **update):
        df = cls.dirty_fields
        ret = super().update(__data, **update)
        print('UDTE', ret, ret.__dict__)
        if __data:
            pass
            cls.__put__(__data, key=ret._pk)

        return ret

    @classmethod
    def insert(cls, __data=None, **insert):
        return ModelInsert(cls, cls._normalize_data(__data, insert))

    @classmethod
    def insert_many(cls, rows, fields=None):
        return ModelInsert(cls, insert=rows, columns=fields)
    """

    pass


class PeeweeDetaModel(PeeweeDetaMixin, PeeweeModel):
    """ """

    @classmethod
    def insert_from(cls, query, fields):
        columns = [
            getattr(cls, field) if isinstance(field, basestring) else field
            for field in fields
        ]
        return ModelInsert(cls, insert=query, columns=columns)

    @classmethod
    def replace(cls, __data=None, **insert):
        return cls.insert(__data, **insert).on_conflict("REPLACE")

    @classmethod
    def replace_many(cls, rows, fields=None):
        return cls.insert_many(rows=rows, fields=fields).on_conflict("REPLACE")

    @classmethod
    def raw(cls, sql, *params):
        return ModelRaw(cls, sql, params)

    @classmethod
    def delete(cls):
        return ModelDelete(cls)

    @classmethod
    def create(cls, **query):
        inst = cls(**query)
        inst.save(force_insert=True)
        return inst

    @classmethod
    def bulk_create(cls, model_list, batch_size=None):
        pass

    @classmethod
    def bulk_update(cls, model_list, fields, batch_size=None):
        return n

    pass
