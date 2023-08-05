from time import time

import pytest  # noqa: pycharm
import pytest_asyncio
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_pg

from kaiju_tools.encoding import dumps
from kaiju_tools.tests.test_data_store import TestDataStore

from kaiju_db.services import SQLService, DatabaseMigrationService

__all__ = ['TestDatabaseService', 'TestMigrationService']


@pytest.mark.asyncio
@pytest.mark.docker
class TestDatabaseService:
    """Test postgres connector."""

    @pytest_asyncio.fixture
    async def _db(self, app, database_service, test_table):
        async with app.services:
            yield database_service

    async def test_connection(self, _db):
        result = await _db.fetchrow(sa.text('SELECT 1 as key;'))
        assert result['key'] == 1

    async def test_created_user(self, _db):
        result = await _db.fetchrow(sa.text('SELECT current_user as user;'))
        assert result['user'] == _db._user

    async def test_created_db(self, _db):
        result = await _db.fetchrow(sa.text('SELECT current_database() as db;'))
        assert result['db'] == _db._db

    async def test_created_extension(self, _db):
        result = await _db.fetchrow(sa.text('SELECT uuid_generate_v4() as uuid;'))
        assert result['uuid']

    async def test_created_table(self, _db, test_table):
        row_id = str(time())
        result = await _db.fetchval(sa.text(f'INSERT INTO {test_table.name} VALUES ({row_id}) RETURNING id;'))
        assert result == row_id


@pytest.mark.asyncio
@pytest.mark.docker
class TestMigrationService:
    """Test migrations."""

    @pytest.fixture
    def _migrations_file(self, migrations_file, test_table):
        migrations_file.write_text(
            dumps(
                [
                    DatabaseMigrationService.State(
                        id=0,
                        commands=[
                            'CREATE SEQUENCE test;',
                            f'ALTER TABLE {test_table.name} ADD COLUMN new_column INT DEFAULT 42;',
                        ],
                    ),
                    DatabaseMigrationService.State(
                        id=1, commands=[f'ALTER TABLE {test_table.name} ADD COLUMN new_column_2 BOOLEAN DEFAULT TRUE;']
                    ),
                ]
            )
        )
        return migrations_file

    @pytest_asyncio.fixture
    async def _migrations_service(self, app, migrations_service, test_table):
        async with app.services:
            yield migrations_service

    async def test_migrations(self, database_service, _migrations_service, _migrations_file, test_table):
        await database_service.execute(test_table.insert().values({'id': 'test'}))
        await _migrations_service.migrate(to_=0, migrations_file=str(_migrations_file))
        test_table.append_column(sa.Column('new_column', sa.INTEGER))
        value = await database_service.fetchval(test_table.select().with_only_columns(test_table.c.new_column))
        assert value == 42
        await _migrations_service.migrate(migrations_file=str(_migrations_file))
        test_table.append_column(sa.Column('new_column_2', sa.BOOLEAN))
        value = await database_service.fetchval(test_table.select().with_only_columns(test_table.c.new_column_2))
        assert value is True


@pytest.mark.asyncio
@pytest.mark.docker
class TestSQLService(TestDataStore):
    @pytest.fixture
    def _test_table(self, _row, test_table):
        row_id, _ = _row()
        test_table.append_column(sa.Column('uuid', sa_pg.UUID, primary_key=isinstance(row_id, tuple)))
        return test_table

    @pytest_asyncio.fixture
    async def _store(self, app, _test_table, mock_data_store, database_service):

        async with app.services:
            await database_service.execute(f'DROP TABLE IF EXISTS {_test_table.name};')

        class TestService(SQLService):
            table = _test_table

        service = TestService(app=app)
        app.services.add_service(service)

        async with app.services:
            yield service
            await database_service.execute(f'DROP TABLE {_test_table.name};')
