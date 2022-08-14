from django_rich_logging.logging import DjangoRequestHandler


def test_add_column_headers_default():
    handler = DjangoRequestHandler()
    assert len(handler.table.columns) == 5


def test_add_column_headers_custom():
    # check that init added one column
    handler = DjangoRequestHandler(columns=[{"header": "test1"}])
    assert len(handler.table.columns) == 1

    # reset table columns
    handler.table.columns = []

    handler._add_column_headers()
    assert len(handler.table.columns) == 1
