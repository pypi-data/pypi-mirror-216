# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:10:02
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Database methods.
"""


from __future__ import annotations
from typing import Any, List, Tuple, Dict, Iterable, Optional, Literal, Union, ClassVar, NoReturn, overload
from re import findall
from sqlalchemy import create_engine as sqlalchemy_create_engine, text
from sqlalchemy.engine.base import Engine, Connection
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine.url import URL
from sqlalchemy.sql.elements import TextClause
from sqlalchemy.exc import OperationalError
from pandas import DataFrame

from .rbase import get_first_notnull
from .rtable import to_table
from .rmonkey import sqlalchemy_add_result_more_fetch, sqlalchemy_support_row_index_by_field
from .roption import ROption
from .rregular import search
from .rtext import rprint
from .rwrap import runtime, retry


__all__ = (
    "RResult",
    "REngine",
    "RConnection",
    "RExecute"
)


# Add more fetch methods to CursorResult object.
RResult = sqlalchemy_add_result_more_fetch()

# Support Row object of package sqlalchemy index by field name.
sqlalchemy_support_row_index_by_field()


class REngine(object):
    """
    Rey's `database engine` type, based on the package `sqlalchemy`.
    """

    # Values to be converted to "NULL".
    null_values: ClassVar[List] = ["", " ", b"", [], (), {}, set()]


    @overload
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        drivername: Optional[str] = None,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: float = 30.0,
        pool_recycle: Optional[int] = None,
        url: Optional[Union[str, URL]] = None,
        engine: Optional[Union[Engine, Connection]] = None,
        **query: str
    ) -> None: ...

    @overload
    def __init__(self, username: None, url: None, engine: None) -> NoReturn: ...

    @overload
    def __init__(self, password: None, url: None, engine: None) -> NoReturn: ...

    @overload
    def __init__(self, host: None, url: None, engine: None) -> NoReturn: ...

    @overload
    def __init__(self, port: None, url: None, engine: None) -> NoReturn: ...

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        drivername: Optional[str] = None,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: float = 30.0,
        pool_recycle: Optional[int] = None,
        url: Optional[Union[str, URL]] = None,
        engine: Optional[Union[Engine, Connection]] = None,
        **query: str
    ) -> None:
        """
        Build `database engine` instance.

        Parameters
        ----------
        host : Server host.
        port : Server port.
        username : Server user name.
        password : Server password.
        database : Database name in the server.
        drivername : Database backend and driver name.
            - `None` : Auto select and try.
            - `str` : Use this value.

        pool_size : Number of connections `keep open`.
        max_overflow : Number of connections `allowed overflow`.
        pool_timeout : Number of seconds `wait create` connection.
        pool_recycle : Number of seconds `recycle` connection.
            - `None` : Use database variable `wait_timeout` value.
            - `Literal[-1]` : No recycle.
            - `int` : Use this value.

        url: Get parameters from server `URL`, but preferred input parameters.
            Parameters include `username`, `password`, `host`, `port`, `database`, `drivername`, `query`.
        engine : Use existing `Engine` or `Connection` object, and get parameters from it.
            Parameters include `username`, `password`, `host`, `port`, `database`, `drivername`, `query`,
            `pool_size`, `max_overflow`, `pool_timeout`, `pool_recycle`.
        query : Server parameters.
        """

        # From existing Engine or Connection object.
        if engine is not None:

            ## Extract Engine object from Connection boject.
            if engine.__class__ == Connection:
                engine = engine.engine

            ## Extract parameters.
            params = self.extract_from_engine(engine)

            ## Set.
            self.drivername = params["drivername"]
            self.username = params["username"]
            self.password = params["password"]
            self.host = params["host"]
            self.port = params["port"]
            self.database = params["database"]
            self.query = params["query"]
            self.pool_size = params["pool_size"]
            self.max_overflow = params["max_overflow"]
            self.pool_timeout = params["pool_timeout"]
            self.pool_recycle = params["pool_recycle"]
            self.engine = engine

        # From parameters create.
        else:

            ## Extract parameters from URL.
            if url is not None:
                params = self.extract_from_url(url)
            else:
                params = dict.fromkeys(
                    (
                        "drivername",
                        "username",
                        "password",
                        "host",
                        "port",
                        "database",
                        "query"
                    )
                )

            ## Set parameters by priority.
            self.drivername = get_first_notnull(drivername, params["drivername"])
            self.username = get_first_notnull(username, params["username"], default="exception")
            self.password = get_first_notnull(password, params["password"], default="exception")
            self.host = get_first_notnull(host, params["host"], default="exception")
            self.port = get_first_notnull(port, params["port"], default="exception")
            self.database = get_first_notnull(database, params["database"])
            self.query = get_first_notnull(query, params["query"], default={"charset": "utf8"}, null_values=[None, {}])
            self.pool_size = pool_size
            self.max_overflow = max_overflow
            self.pool_timeout = pool_timeout

            ## Create Engine object.

            ### Set number of seconds recycle connection.
            if pool_recycle is None:
                self.pool_recycle = -1
                self.engine = self.create_engine()
                variables = self.variables
                self.pool_recycle = int(variables["wait_timeout"])
                self.engine.pool._recycle = int(variables["wait_timeout"])

            else:
                self.pool_recycle = pool_recycle
                self.engine = self.create_engine()


    def extract_from_url(self, url: Union[str, URL]) -> Dict[
        Literal["drivername", "username", "password", "host", "port", "database", "query"],
        Any
    ]:
        """
        Extract parameters from `URL` of string.

        Parameters
        ----------
        url : URL of string.

        Returns
        -------
        Extracted parameters.
        """

        # Extract.

        ## When str object.
        if url.__class__ == str:
            pattern = "^([\w\+]+)://(\w+):(\w+)@(\d+\.\d+\.\d+\.\d+):(\d+)[/]?([\w/]+)?[\?]?([\w&=]+)?$"
            result = search(pattern, url)
            if result is None:
                raise ValueError("the value of parameter 'url' is incorrect")
            (
                drivername,
                username,
                password,
                host,
                port,
                database,
                query_str
            ) = result
            if query_str is not None:
                pattern = "(\w+)=(\w+)"
                query_findall = findall(pattern, query_str)
                query = {key: val for key, val in query_findall}
            else:
                query = {}

        ## When URL object.
        elif url.__class__ == URL:
            drivername = url.drivername
            username = url.username
            password = url.password
            host = url.host
            port = url.port
            database = url.database
            query = dict(url.query)

        # Generate parameters.
        params = {
            "drivername": drivername,
            "username": username,
            "password": password,
            "host": host,
            "port": port,
            "database": database,
            "query": query
        }

        return params


    def extract_from_engine(self, engine: Union[Engine, Connection]) -> Dict[
        Literal[
            "drivername", "username", "password", "host", "port", "database", "query",
            "pool_size", "max_overflow", "pool_timeout", "pool_recycle"
        ],
        Any
    ]:
        """
        Extract parameters from `Engine` or `Connection` object.

        Parameters
        ----------
        engine : Engine or Connection object.

        Returns
        -------
        Extracted parameters.
        """

        ## Extract Engine object from Connection boject.
        if engine.__class__ == Connection:
            engine = engine.engine

        ## Extract.
        drivername = engine.url.drivername
        username = engine.url.username
        password = engine.url.password
        host = engine.url.host
        port = engine.url.port
        database = engine.url.database
        query = dict(engine.url.query)
        pool_size = engine.pool._pool.maxsize
        max_overflow = engine.pool._max_overflow
        pool_timeout = engine.pool._timeout
        pool_recycle = engine.pool._recycle

        # Generate parameters.
        params = {
            "drivername": drivername,
            "username": username,
            "password": password,
            "host": host,
            "port": port,
            "database": database,
            "query": query,
            "pool_size": pool_size,
            "max_overflow": max_overflow,
            "pool_timeout": pool_timeout,
            "pool_recycle": pool_recycle
        }

        return params


    @property
    def url(self) -> str:
        """
        Generate server `URL`.

        Returns
        -------
        Server URL.
        """

        # Generate URL.
        _url = f"{self.drivername}://{self.username}:{self.password}@{self.host}:{self.port}"

        # Add database path.
        if self.database is not None:
            _url = f"{_url}/{self.database}"

        # Add Server parameters.
        if self.query != {}:
            query = "&".join(
                [
                    f"{key}={val}"
                    for key, val in self.query.items()
                ]
            )
            _url = f"{_url}?{query}"

        return _url


    def create_engine(self, **kwargs) -> Engine:
        """
        Create database `Engine` object.

        Parameters
        ----------
        kwargs : Keyword parameters of create engine method.

        Returns
        -------
        Engine object.
        """

        # Handle parameters.
        if self.drivername is None:
            drivernames = ("mysql+mysqldb", "mysql+pymysql")
        else:
            drivernames = (self.drivername,)

        # Create Engine object.
        for drivername in drivernames:

            ## Set engine parameters.
            self.drivername = drivername
            engine_params = {
                "url": self.url,
                "pool_size": self.pool_size,
                "max_overflow": self.max_overflow,
                "pool_timeout": self.pool_timeout,
                "pool_recycle": self.pool_recycle,
                **kwargs
            }

            ## Try create.
            try:
                engine = sqlalchemy_create_engine(**engine_params)
            except ModuleNotFoundError:
                pass
            else:
                return engine

        # Throw exception.
        drivernames_str = " and ".join(
            [
                dirvername.split("+", 1)[-1]
                for dirvername in drivernames
            ]
        )
        raise ModuleNotFoundError(f"module {drivernames_str} not fund")


    @property
    def count(self) -> Tuple[int, int]:
        """
        Count number of `keep open` and `allowed overflow` connection.

        Returns
        -------
        Number of keep open and allowed overflow connection.
        """

        # Count.
        _overflow = self.engine.pool._overflow
        if _overflow < 0:
            keep_n = self.pool_size + _overflow
            overflow_n = 0
        else:
            keep_n = self.pool_size
            overflow_n = _overflow

        return keep_n, overflow_n


    def fill_data(
        self,
        data: Union[Dict, List[Dict]],
        sql: Union[str, TextClause],
    ) -> List[Dict]:
        """
        `Fill` missing data according to contents of `TextClause` object of package `sqlalchemy`, and filter out empty Dict.

        Parameters
        ----------
        data : Data set for filling.
        sql : SQL in method sqlalchemy.text format, or TextClause object.

        Returns
        -------
        Filled data.
        """

        # Handle parameters.
        if data.__class__ == dict:
            data = [data]
        if sql.__class__ == TextClause:
            sql = sql.text

        # Filter out empty Dict.
        data = [
            param
            for param in data
            if param != {}
        ]

        # Extract fill field names.
        pattern = "(?<!\\\):(\w+)"
        sql_keys = findall(pattern, sql)

        # Fill data.
        for param in data:
            for key in sql_keys:
                val = param.get(key)
                if val in self.null_values:
                    val = None
                param[key] = val

        return data


    def get_syntax(self, sql: Union[str, TextClause]) -> str:
        """
        Extract `syntax` type form SQL.

        Parameters
        ----------
        sql : SQL text or TextClause object.

        Returns
        -------
        SQL syntax type.
        """

        # Handle parameters.
        if sql.__class__ == TextClause:
            sql = sql.text

        # Extract.
        split_sql = sql.split(maxsplit=1)
        syntax_type = split_sql[0]
        syntax_type = syntax_type.upper()

        return syntax_type


    def is_multi_sql(self, sql: Union[str, TextClause]) -> bool:
        """
        Judge whether it is `multi segment SQL`.

        Parameters
        ----------
        sql : SQL text or TextClause object.

        Returns
        -------
        Judgment result.
        """

        # Handle parameters.
        if sql.__class__ == TextClause:
            sql = sql.text

        # Judge.
        if ";" in sql.rstrip()[:-1]:
            return True
        return False


    def executor(
        self,
        connection: Connection,
        sql: TextClause,
        data: List[Dict],
        report: bool
    ) -> RResult:
        """
        `SQL` executor.

        Parameters
        ----------
        connection : Connection object.
        sql : TextClause object.
        data : Data set for filling.
        report : Whether report SQL execute information.

        Returns
        -------
        Result object.
        """

        # Create Transaction object.
        with connection.begin():

            # Execute.

            ## Report.
            if report:
                result, report_runtime = runtime(connection.execute, sql, data, _return_report=True)
                report_info = (
                    f"{report_runtime}\n"
                    f"Row Count: {result.rowcount}"
                )
                if data == []:
                    rprint(report_info, sql, title="SQL")
                else:
                    rprint(report_info, sql, data, title="SQL")

            ## Not report.
            else:
                result = connection.execute(sql, data)

        return result


    def execute(
        self,
        sql: Union[str, TextClause],
        data: Optional[Union[List[Dict], Dict, CursorResult, DataFrame]] = None,
        report: bool = None,
        **kwdata: Any
    ) -> RResult:
        """
        Execute `SQL`.

        Parameters
        ----------
        sql : SQL in method `sqlalchemy.text` format, or `TextClause` object.
        data : Data set for filling.
        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.

        Returns
        -------
        Result object.
        """

        # Get parameters by priority.
        report = get_first_notnull(report, ROption.report_execute_info)

        # Handle parameters.
        if sql.__class__ == str:
            sql = text(sql)
        if data is None:
            data = [kwdata]
        else:
            if data.__class__ == dict:
                data = [data]
            elif isinstance(data, CursorResult):
                data = to_table(data)
            elif data.__class__ == DataFrame:
                data = to_table(data)
            else:
                data = data.copy()
            for param in data:
                param.update(kwdata)

        # Fill missing data.
        data = self.fill_data(data, sql)

        # Execute.

        ## Create Connection object.
        with self.engine.connect() as connection:

            ## Can retry.
            if not self.is_multi_sql(sql):
                result = retry(
                    self.executor,
                    connection,
                    sql,
                    data,
                    report,
                    _report="Database execute operational error",
                    _exception=OperationalError
                )

            ## Cannot retry.
            else:
                result = self.executor(connection, sql, data, report)

        return result


    def execute_select(
            self,
            table: str,
            database: Optional[str] = None,
            fields: Optional[Union[str, Iterable]] = None,
            where: Optional[str] = None,
            group: Optional[str] = None,
            having: Optional[str] = None,
            order: Optional[str] = None,
            limit: Optional[Union[int, str, List, Tuple]] = None,
            report: bool = None,
            **kwdata: Any
        ) -> RResult:
        """
        Execute `select` SQL.

        Parameters
        ----------
        table : Table name.
        database : Database name.
        fields : Select clause content.
            - `None` : Is `SELECT *`.
            - `str` : Join as `SELECT str`.
            - `Iterable[str]` : Join as `SELECT \`str\`, ...`.

        where : Clause `WHERE` content, join as `WHERE str`.
        group : Clause `GROUP BY` content, join as `GROUP BY str`.
        having : Clause `HAVING` content, join as `HAVING str`.
        order : Clause `ORDER BY` content, join as `ORDER BY str`.
        limit : Clause `LIMIT` content.
            - `Union[int, str]` : Join as `LIMIT int/str`.
            - `Union[List, Tuple]` with length of 1 or 2 `int/str` : Join as `LIMIT int/str [, int/str]`.

        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.

        Returns
        -------
        Result object.
        """

        # Get parameters by priority.
        database = get_first_notnull(database, self.database)

        # Generate SQL.
        sqls = []

        ## Part 'SELECT' syntax.
        if fields is None:
            fields = "*"
        elif fields.__class__ != str:
            fields = ",".join([f"`{field}`" for field in fields])
        sql_select = f"SELECT {fields}"
        sqls.append(sql_select)

        ## Part 'FROM' syntax.
        sql_from = f"FROM `{database}`.`{table}`"
        sqls.append(sql_from)

        ## Part 'WHERE' syntax.
        if where is not None:
            sql_where = f"WHERE {where}"
            sqls.append(sql_where)

        ## Part 'GROUP BY' syntax.
        if group is not None:
            sql_group = f"GROUP BY {group}"
            sqls.append(sql_group)

        ## Part 'GROUP BY' syntax.
        if having is not None:
            sql_having = f"HAVING {having}"
            sqls.append(sql_having)

        ## Part 'ORDER BY' syntax.
        if order is not None:
            sql_order = f"ORDER BY {order}"
            sqls.append(sql_order)

        ## Part 'LIMIT' syntax.
        if limit is not None:
            if limit.__class__ in (str, int):
                sql_limit = f"LIMIT {limit}"
            else:
                if len(limit) in (1, 2):
                    limit_content = ",".join([str(val) for val in limit])
                    sql_limit = f"LIMIT {limit_content}"
                else:
                    raise ValueError("The length of the parameter 'limit' value must be 1 or 2")
            sqls.append(sql_limit)

        sql = "\n".join(sqls)

        # Execute SQL.
        result = self.execute(sql, report=report, **kwdata)

        return result


    def execute_insert(
        self,
        data: Union[List[Dict], Dict, CursorResult, DataFrame],
        table: str,
        database: Optional[str] = None,
        duplicate: Optional[Literal["ignore", "update"]] = None,
        report: bool = None
    ) -> Optional[RResult]:
        """
        `Insert` the data of table in the datebase.

        Parameters
        ----------
        data : Insert data.
        table : Table name.
        database : Database name.
        duplicate : Handle method when constraint error.
            - `None` : Not handled.
            - `ignore` : Use `UPDATE IGNORE INTO` clause.
            - `update` : Use `ON DUPLICATE KEY UPDATE` clause.

        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        Returns
        -------
        None or result object.
            - `None` : When the data is empty.
            - `Result object` : When the data is not empty.
        """

        # Get parameters by priority.
        database = get_first_notnull(database, self.database)

        # Handle parameters.
        if data.__class__ == dict:
            data = [data]
        elif isinstance(data, CursorResult):
            data = to_table(data)
        elif data.__class__ == DataFrame:
            data = to_table(data)

        # If data is empty, not execute.
        if data in ([], [{}]):
            return

        # Generate SQL.
        first_row = data[0]
        fields_str = ",".join([f"`{field}`" for field in first_row])
        fields_str_position = ",".join(
            [
                value
                if value.__class__ == str and "(" in value
                else ":" + field
                for field, value in first_row.items()
            ]
        )
        if duplicate == "ignore":
            sql = (
                f"INSERT IGNORE INTO `{database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})"
            )
        elif duplicate == "update":
            update_content = ",".join([f"`{field}` = VALUES(`{field}`)" for field in first_row])
            sql = (
                f"INSERT INTO `{database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})\n"
                "ON DUPLICATE KEY UPDATE\n"
                f"{update_content}"
            )
        else:
            sql = (
                f"INSERT INTO `{database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})"
            )

        # Execute SQL.
        result = self.execute(sql, data, report)

        return result


    def execute_update(
        self,
        data: Union[List[Dict], Dict, CursorResult, DataFrame],
        table: str,
        database: Optional[str] = None,
        where_fields: Optional[Union[str, Iterable[str]]] = None,
        report: bool = None
    ) -> Optional[RResult]:
        """
        `Update` the data of table in the datebase.

        Parameters
        ----------
        data : Updated data.
        table : Table name.
        database : Database name.
        where_fields : Clause `WHERE` clause content.
            - `None` : The first key value pair of each item is judged.
            - `str` : This key value pair of each item is judged.
            - `Iterable[str]` : Multiple judged, `and` relationship.

        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        Returns
        -------
        None or result object.
            - `None` : When the data is empty.
            - `Result object` : When the data is not empty.
        """

        # Get parameters by priority.
        database = get_first_notnull(database, self.database)

        # Handle parameters.
        if data.__class__ == dict:
            data = [data]
        elif isinstance(data, CursorResult):
            data = to_table(data)
        elif data.__class__ == DataFrame:
            data = to_table(data)

        # If data is empty, not execute.
        if data in ([], [{}]):
            return

        # Generate SQL.
        data_flatten = {}
        sqls = []
        if where_fields is None:
            no_where = True
        else:
            no_where = False
            if where_fields.__class__ == str:
                where_fields = [where_fields]
        for index, row in enumerate(data):
            for key, val in row.items():
                index_key = f"{index}_{key}"
                data_flatten[index_key] = val
            if no_where:
                for key in row:
                    where_fields = [key]
                    break
            set_content = ",".join(
                [
                    f"`{key}` = {val}"
                    if val.__class__ == str and "(" in val
                    else f"`{key}` = :{index}_{key}"
                    for key, val in row.items()
                    if key not in where_fields
                ]
            )
            where_content = "\n    AND ".join(
                [
                    f"`{field}` = {val}"
                    if val.__class__ == str and "(" in val
                    else f"`{field}` = :{index}_{field}"
                    for field, val in [
                        (field, row[field])
                        for field in where_fields
                    ]
                ]
            )
            sql = (
                f"UPDATE `{database}`.`{table}`\n"
                f"SET {set_content}\n"
                f"WHERE {where_content}"
            )
            sqls.append(sql)
        sqls = ";\n".join(sqls)

        # Execute SQL.
        result = self.execute(sqls, data_flatten, report)

        return result


    def execute_delete(
        self,
        table: str,
        database: Optional[str] = None,
        where: Optional[str] = None,
        report: bool = None,
        **kwdata: Any
    ) -> RResult:
        """
        `Delete` the data of table in the datebase.

        Parameters
        ----------
        table : Table name.
        database : Database name.
        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.

        Returns
        -------
        Result object.
        """

        # Get parameters by priority.
        database = get_first_notnull(database, self.database)

        # Generate SQL.
        sqls = []

        ## Part 'DELETE' syntax.
        sql_delete = f"DELETE FROM `{database}`.`{table}`"
        sqls.append(sql_delete)

        ## Part 'WHERE' syntax.
        if where is not None:
            sql_where = f"WHERE {where}"
            sqls.append(sql_where)

        sql = "\n".join(sqls)

        # Execute SQL.
        result = self.execute(sql, report=report, **kwdata)

        return result


    @overload
    def execute_exist(
        self,
        table: str,
        database: Optional[str] = None,
        where: Optional[str] = None,
        count: bool = False,
        report: bool = None,
        **kwdata: Any
    ) -> Union[bool, int]: ...

    @overload
    def execute_exist(
        self,
        count: Literal[False]
    ) -> bool: ...

    @overload
    def execute_exist(
        self,
        count: Literal[True]
    ) -> int: ...

    def execute_exist(
        self,
        table: str,
        database: Optional[str] = None,
        where: Optional[str] = None,
        count: bool = False,
        report: bool = None,
        **kwdata: Any
    ) -> Union[bool, int]:
        """
        `Count` records.

        Parameters
        ----------
        table : Table name.
        database : Database name.
        where : Match condition, `WHERE` clause content, join as `WHERE str`.
            - `None` : Match all.
            - `str` : Match condition.

        count : Whether return match count, otherwise return whether it exist.
        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.

        Returns
        -------
        CursorResult object of alsqlchemy package.
        """

        # Get parameters.
        if count:
            limit = None
        else:
            limit = 1

        # Execute.
        result = self.execute_select(table, database, "1", where=where, limit=limit, report=report, **kwdata)

        # Returns.
        rowcount = result.rowcount
        if count:
            return rowcount
        else:
            return rowcount != 0


    @property
    def databases(self) -> Dict[str, List[str]]:
        """
        Get dictionary of `databases` and `tables`.

        Returns
        -------
        Dictionary of databases and tables
        """

        # Get database list.

        ## Generate SQL.
        sql = "SHOW DATABASES"

        ## Execute SQL.
        result = self.execute(sql)

        # Get table list of database.
        database_dict = {}
        for database, in result:
            sql = f"USE {database}"
            self.execute(sql)
            sql = "SHOW TABLES"
            result = self.execute(sql)
            database_dict[database] = [row for row, in result]

        return database_dict


    @property
    def variables(self) -> Dict[str, str]:
        """
        Get `variables` of database.

        Returns
        -------
        Variables of database.
        """

        # Generate SQL.
        sql = "SHOW VARIABLES"

        # Execute SQL.
        result = self.execute(sql)

        # Convert dictionary.
        variables = result.fetch_dict()

        return variables


    @variables.setter
    def variables(self, params: Dict[str, Union[str, float]]) -> None:
        """
        Update `variables` of database.

        Parameters
        ----------
        params : Update parameter key value pairs.
        """

        # Generate SQL.
        sqls = [
            "SET %s = %s" % (
                key,
                (
                    val
                    if val.__class__ in (int, float)
                    else "'%s'" % val
                )
            )
            for key, val in params.items()
        ]
        sqls = ";\n".join(sqls)

        # Execute SQL.
        self.execute(sqls)


    @property
    def global_variables(self) -> Dict[str, str]:
        """
        Get `global variables` of database.

        Returns
        -------
        Global variables of database.
        """

        # Generate SQL.
        sql = "SHOW GLOBAL VARIABLES"

        # Execute SQL.
        result = self.execute(sql)

        # Convert dictionary.
        variables = result.fetch_dict()

        return variables


    @global_variables.setter
    def global_variables(self, params: Dict[str, Union[str, float]]) -> None:
        """
        Update `global variables` of database.

        Parameters
        ----------
        params : Update parameter key value pairs.
        """

        # Generate SQL.
        sqls = [
            "SET GLOBAL %s = %s" % (
                key,
                (
                    val
                    if val.__class__ in (int, float)
                    else "'%s'" % val
                )
            )
            for key, val in params.items()
        ]
        sqls = ";\n".join(sqls)

        # Execute SQL.
        self.execute(sqls)


    @property
    def status(self) -> Dict[str, str]:
        """
        Get `status` of database.

        Returns
        -------
        Status of database.
        """

        # Generate SQL.
        sql = "SHOW STATUS"

        # Execute SQL.
        result = self.execute(sql)

        # Convert dictionary.
        status = result.fetch_dict()

        return status


    @property
    def global_status(self) -> Dict[str, str]:
        """
        Get `global status` of database.

        Returns
        -------
        Global status of database.
        """

        # Generate SQL.
        sql = "SHOW GLOBAL STATUS"

        # Execute SQL.
        result = self.execute(sql)

        # Convert dictionary.
        status = result.fetch_dict()

        return status


    def connect(self) -> RConnection:
        """
        Build `database connection` instance.
        """

        # Build.
        rconnection = RConnection(
            self.engine.connect(),
            self
        )

        return rconnection


    @property
    def exe(self) -> RExecute:
        """
        Build `database execute` instance.

        Examples
        --------
        Select.
        >>> exe = RExecute(rengine)
        >>> result = exe.database.table()

        Insert.
        >>> exe = RExecute(rengine)
        >>> result = exe.database.table + data

        Update.
        >>> exe = RExecute(rengine)
        >>> result = exe.database.table & data

        Delete.
        >>> exe = RExecute(rengine)
        >>> result = exe.database.table - data
        """

        # Build.
        rexecute = RExecute(self)

        return rexecute


class RConnection(REngine):
    """
    Rey's `database connection` type, based on the package `sqlalchemy`.
    """


    def __init__(
            self,
            connection: Connection,
            rengine: REngine
        ) -> None:
        """
        Build `database connection` instance.

        Parameters
        ----------
        connection : Connection object.
        rengine : REngine object.
        """

        # Set parameters.
        self.connection = connection
        self.rengine = rengine
        self.begin = None
        self.begin_count = 0
        self.drivername = rengine.drivername
        self.username = rengine.username
        self.password = rengine.password
        self.host = rengine.host
        self.port = rengine.port
        self.database = rengine.database
        self.query = rengine.query
        self.pool_recycle = rengine.pool_recycle


    def executor(
        self,
        connection: Connection,
        sql: TextClause,
        data: List[Dict],
        report: bool
    ) -> RResult:
        """
        `SQL` executor.

        Parameters
        ----------
        connection : Connection object.
        sql : TextClause object.
        data : Data set for filling.
        report : Whether report SQL execute information.

        Returns
        -------
        Result object.
        """

        # Create Transaction object.
        if self.begin_count == 0:
            self.rollback()
            self.begin = connection.begin()

        # Execute.

        ## Report.
        if report:
            result, report_runtime = runtime(connection.execute, sql, data, _return_report=True)
            report_info = (
                f"{report_runtime}\n"
                f"Row Count: {result.rowcount}"
            )
            if data == []:
                rprint(report_info, sql, title="SQL")
            else:
                rprint(report_info, sql, data, title="SQL")

        ## Not report.
        else:
            result = connection.execute(sql, data)

        # Count.
        syntax = self.get_syntax(sql)
        if syntax in ("UPDATE", "INSERT", "DELETE"):
            self.begin_count += 1

        return result


    def execute(
        self,
        sql: Union[str, TextClause],
        data: Optional[Union[List[Dict], Dict, CursorResult, DataFrame]] = None,
        report: bool = None,
        **kwdata: Any
    ) -> RResult:
        """
        Execute `SQL`.

        Parameters
        ----------
        sql : SQL in method `sqlalchemy.text` format, or `TextClause` object.
        data : Data set for filling.
        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.

        Returns
        -------
        Result object.
        """

        # Get parameters by priority.
        report = get_first_notnull(report, ROption.report_execute_info)

        # Handle parameters.
        if sql.__class__ == str:
            sql = text(sql)
        if data is None:
            data = [kwdata]
        else:
            if data.__class__ == dict:
                data = [data]
            elif isinstance(data, CursorResult):
                data = to_table(data)
            elif data.__class__ == DataFrame:
                data = to_table(data)
            else:
                data = data.copy()
            for param in data:
                param.update(kwdata)

        # Fill missing data.
        data = self.fill_data(data, sql)

        # Execute.

        ## Can retry.
        if self.begin_count == 0 and not self.is_multi_sql(sql):
            result = retry(
            self.executor,
            self.connection,
            sql,
            data,
            report,
            _report="Database execute operational error",
            _exception=OperationalError
        )

        ## Cannot retry.
        else:
            result = self.executor(self.connection, sql, data, report)

        return result


    def commit(self) -> None:
        """
        `Commit` cumulative executions.
        """

        # Commit.
        if self.begin is not None:
            self.begin.commit()
            self.begin = None
            self.begin_count = 0


    def rollback(self) -> None:
        """
        `Rollback` cumulative executions.
        """

        # Rollback.
        if self.begin is not None:
            self.begin.rollback()
            self.begin = None
            self.begin_count = 0


    def close(self) -> None:
        """
        `Close` database connection.
        """

        # Close.
        self.connection.close()


    def __del__(self) -> None:
        """
        `Close` database connection.
        """

        # Close.
        self.close()


class RExecute(object):
    """
    Rey's `database execute` type, based on the package `sqlalchemy`.

    Examples
    --------
    Select.
    >>> exe = RExecute(rengine)
    >>> result = exe.database.table()

    Insert.
    >>> exe = RExecute(rengine)
    >>> result = exe.database.table + data

    Update.
    >>> exe = RExecute(rengine)
    >>> result = exe.database.table & data

    Delete.
    >>> exe = RExecute(rengine)
    >>> result = exe.database.table - data
    """


    def __init__(self, rengine: Union[REngine, RConnection]) -> None:
        """
        Build `database execute` instance.

        Parameters
        ----------
        rengine : REngine object or RConnection object.
        """

        self.__rengine = rengine
        self.__database = None
        self.__table = None


    def __getattr__(self, name) -> Union[Any, RExecute]:
        """
        Get attribute or set database name or set table name.

        Parameters
        ----------
        name : Attribute name or database name or table name.
        """

        # Get attribute.
        if name in ("_RExecute__rengine", "_RExecute__database", "_RExecute__table"):
            return self.__dict__[name]

        # Set database name.
        if self.__database is None:
            self.__database = name

        # Set table name.
        elif self.__table is None:
            self.__table = name

        # Throw exception.
        else:
            raise AssertionError("usage error")

        return self


    def __call__(self, *fields: str) -> RResult:
        """
        `Select` the data of table in the datebase.

        Parameters
        ----------
        fields : Select field names.

        Returns
        -------
        Result object.
        """

        # Check parameters.
        if self.__database is None or self.__table is None:
            raise AssertionError("usage error")

        # Handle parameters.
        if fields == ():
            fields = None

        # Selete.
        result = self.__rengine.execute_select(
            self.__table,
            self.__database,
            fields
        )

        return result


    def __add__(self, data: Union[List[Dict], Dict, CursorResult, DataFrame]) -> RResult:
        """
        `Insert` the data of table in the datebase.

        Parameters
        ----------
        data : Insert data.

        Returns
        -------
        Result object.
        """

        # Check parameters.
        if self.__database is None or self.__table is None:
            raise AssertionError("usage error")

        # Insert.
        result = self.__rengine.execute_insert(
            data,
            self.__table,
            self.__database
        )

        return result


    def __and__(self, data: Union[List[Dict], Dict, CursorResult, DataFrame]) -> RResult:
        """
        `Update` the data of table in the datebase.

        Parameters
        ----------
        data : Updated data.

        Returns
        -------
        Result object.
        """

        # Check parameters.
        if self.__database is None or self.__table is None:
            raise AssertionError("usage error")

        # Insert.
        result = self.__rengine.execute_update(
            data,
            self.__table,
            self.__database
        )

        return result


    def __sub__(self, where: str) -> RResult:
        """
        `Delete` the data of table in the datebase.

        Parameters
        ----------
        where : Clause `WHERE` content, join as `WHERE str`.

        Returns
        -------
        Result object.
        """

        # Check parameters.
        if self.__database is None or self.__table is None:
            raise AssertionError("usage error")

        # Delete.
        result = self.__rengine.execute_delete(
            self.__table,
            self.__database,
            where
        )

        return result