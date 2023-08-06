import inspect


def append_doc(o):
    _doc = ""
    for _ in o:
        _doc += inspect.getdoc(_) + "\n"
        for _n, _o in inspect.getmembers(_):
            if not _n.startswith("_") and inspect.isfunction(_o):
                _signature = inspect.signature(_o)
                _params = list(_signature.parameters.keys())
                _func_name = _n + "(" + ", ".join(_params) + ")"
                _doc += _func_name + "\n"
                _doc += inspect.getdoc(_o) + "\n"
                del _signature, _params, _func_name
                _doc += "\n"
        _doc += "\n"
    return _doc
