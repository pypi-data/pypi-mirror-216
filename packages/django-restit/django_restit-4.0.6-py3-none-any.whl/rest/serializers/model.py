import datetime
import time
import math
from decimal import Decimal
from django.db import models
from itertools import chain
from rest import helpers
from objict import objict
__MY_CACHE__ = objict()


def serialize(instance, graph):
    if isinstance(graph, str):
        graph = instance.getGraph(graph)
    return to_dict_from_graph(instance, graph)


def to_dict_from_graph(instance, graph):
    fields = graph.get("fields", [])
    extra = graph.get("extra", [])
    exclude = graph.get("exclude", [])
    recurse_into = graph.get("recurse_into", [])
    return to_dict(instance, fields=fields, extra=extra, exclude=exclude, recurse_into=recurse_into)


def to_dict(instance, fields=None, extra=[], exclude=[], recurse_into=[]):
    data = {}
    fields = get_fields(instance) if not fields else fields
    recursed = []
    for f in chain(fields, extra, recurse_into):
        fin, fout = (f[0], f[1]) if isinstance(f, (list, tuple)) else (f, f)
        if fin in exclude:
            continue
        if "." in fin:
            top = fin.split('.')[0]
            if top in recursed:
                continue
            recursed.append(top)
            fin = fout = top
        if fin.startswith("generic__") and hasattr(instance, "restGetGenericRelation"):
            fin = fin.split("__")[1]
            obj = get_generic_value(instance, fin, fout)
            if obj is not None:
                data[fin] = obj
                id_key = f"{fin}_id"
                if id_key in data:
                    del data[id_key]
            continue
        value = get_field_value(instance, fin)
        if isinstance(value, models.Model):
            if fin not in recursed:
                recursed.append(fin)
            sfields = get_model_fields(fin, chain(fields, extra, recurse_into))
            if sfields:
                data[fout] = to_dict(value, sfields)
            elif hasattr(value, "pk"):
                data[fout] = value.pk
                # FIXME we should use _id when not showing full model
                # data[f"{fout}_id"] = value.pk
            continue
        if isinstance(value, models.Manager):
            if fin not in recursed:
                recursed.append(fin)
            sfields = get_model_fields(fin, chain(fields, extra, recurse_into))
            if __MY_CACHE__.cs is None:
                __MY_CACHE__.cs = helpers.importModule("rest.serializers.collection")
            data[fout] = __MY_CACHE__.cs.to_list(value.all(), fields=sfields)["data"]
            continue
        try:
            data[fout] = serialize_value(value if not callable(value) else value())
        except Exception as err:
            data[fout] = str(err)
            helpers.log_exception(fout)
    return data


def serialize_value(value):
    if isinstance(value, (str, int, float)):
        return value
    if isinstance(value, (tuple, list)):
        return [serialize_value(v) for v in value]
    elif isinstance(value, dict):
        return {key: serialize_value(val) for key, val in value.items()}
    elif isinstance(value, datetime.datetime):
        # return int(time.mktime(value.timetuple()))
        return time.mktime(value.timetuple())
    elif isinstance(value, datetime.date):
        return value.strftime("%Y/%m/%d")
    elif isinstance(value, float) and math.isnan(value):
        return 0.0
    elif isinstance(value, Decimal):
        return float(value) if not value.is_nan() else 0.0
    return value


def get_generic_value(instance, key, graph="generic"):
    obj = None
    try:
        obj = instance.restGetGenericRelation(key)
    except Exception as err:
        print(err)
        return None
    if key == graph:
        graph = "generic"
    data = to_dict_from_graph(obj, obj.getGraph(graph))
    data["model"] = getattr(instance, key)
    return data


def get_field_value(instance, key):
    if isinstance(instance, dict):
        return instance.get(key, None)
    return getattr(instance, key) if hasattr(instance, key) else None


def get_model_fields(name, fields):
    skey = f"{name}."
    slen = len(skey)
    output = []
    for f in fields:
        if isinstance(f, (list, tuple)):
            if (f[0].startswith(skey)):
                output.append((f[0][slen:], f[1]))
        elif f.startswith(skey):
            output.append(f[slen:])
    return output
    # return [(f[0][f[0].find(".")+1:], f[1]) if isinstance(f, (list, tuple)) else f[f.find(".")+1:] for f in fields if f[0].startswith(skey)]


def get_fields(qset, model=None):
    fields = None
    if isinstance(qset, dict):
        return list(qset.keys())
    elif hasattr(qset, '_meta'):
        fields = qset._meta.fields
    elif hasattr(qset, 'model'):
        fields = qset.model._meta.fields
    elif hasattr(qset, 'keys'):
        return list(qset.keys())
    elif model and hasattr(model, '_meta'):
        fields = model._meta.fields
    return [f.name for f in fields] if fields else None
