""" Provides the default database instantiation """

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
import os
import contextlib
from sqlalchemy import MetaData


Base = declarative_base()


def initialise(
    file_based, sqlite_dir, clean_db=False, test=False, project_id=None
) -> Session:
    """initialises the database

    Args:
        file_based (bool): true if the data will be stored in an sqlite file,
        otherwise an in-memory db will be created.
        sqlite_dir (str): directory to store the sqlite file, if needed.
        clean_db (bool, optional): delete any existing database with matching
        params. Defaults to False.
        test (bool, optional): Whether the db is being created as part of an
        automated test. Defaults to False.
        project_id (int, optional): Unique id for the project. Defaults to None.

    Returns:
        Session:
    """

    make_dir_if_not_exist(sqlite_dir)

    if file_based:
        sql_path = make_database_file_path(sqlite_dir, test, project_id)
        engine = create_engine(f"sqlite:///{sql_path}")
    else:  # in memory
        engine = create_engine("sqlite:///")

    session = sessionmaker(bind=engine)
    if clean_db:
        # next line will clean in-memory databases too
        remove_database_file(sqlite_dir, test, project_id)
        # clean_database(engine)
        Base.metadata.create_all(engine)
        session().commit()
    return session()


def make_dir_if_not_exist(sqlite_dir):
    """creates a directory if one doesn't exist

    Args:
        sqlite_dir (str):
    """
    if not os.path.exists(sqlite_dir):
        os.makedirs(sqlite_dir)


def clean_database(engine):
    
    MetaData().bind = engine
    MetaData().drop_all(engine)
    MetaData().create_all(engine)

    # con = engine.connect()
    # trans = con.begin()
    # for name, table in MetaData().tables.items():
    #     table.delete()
    #     con.execute(table.delete())
    # trans.commit()
    #
    #
    # meta = MetaData()
    # for table in reversed(meta.sorted_tables):
    #     # print('Clear table %s' % table)
    #     engine.execute(table.delete())
    #
    # meta = MetaData()
    # with contextlib.closing(engine.connect()) as con:
    #     trans = con.begin()
    #     for table in reversed(meta.sorted_tables):
    #         con.execute(table.delete())
    #     trans.commit()


def remove_database_file(sqlite_dir, test, project_id=None) -> None:
    """deletes an existing db file if one exists
    """
    file_path = make_database_file_path(sqlite_dir, test, project_id)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except PermissionError as e:
            print(f"Could not delete previous database file {sqlite_dir},  {str(e)}")


def make_database_file_path(sqlite_path, test, project_id=None) -> str:
    """calculates the file path of the sqlite database, based on params

    Args:
        sqlite_path (str):
        test (bool):
        project_id (int, optional): Defaults to None.

    Returns:
        str: path to database file, including the file name and ext.
    """
    file_name = "pyconcodese.db"
    if test:
        file_name = f"test-{file_name}"
    if project_id is not None:
        file_name = f".{project_id}-{file_name}"
    return os.path.join(sqlite_path, file_name)
