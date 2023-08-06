from mbnk.utils.to_camel_case import to_camel_case


def data_builder(**kwargs):
    data = {}

    for kwarg in kwargs:
        key = kwarg.replace("timestamp", "")
        key = to_camel_case(key)
        value = kwargs.get(kwarg)
        data[key] = value

    return data
