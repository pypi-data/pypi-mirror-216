# flake8: noqa

try:
    from .chains.data_dict import DataDictChain
    from .chains.enrich import embed, enrich
except ImportError as e:
    raise ImportError(
        "datarobotx.llm requires additional dependencies; consider using `pip install datarobotx[llm]`"
    ) from e
