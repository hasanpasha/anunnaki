from anunnaki.data.data import Data


def test_table_exist():
    with Data() as data:
        result = data.create_extension_table()
        assert not result.succeed


def test_table_list():
    with Data() as data:
        result = data.list_extensions()
        assert result
