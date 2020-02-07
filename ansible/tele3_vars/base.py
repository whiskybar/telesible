import mysql.connector


class SQLVars:

    connections = {}
    cursors = {}

    def __init__(self, option_file, default_database):
        self.database = getattr(self, 'DATABASE', default_database)
        self.group = getattr(self, 'GROUP', self.__class__.__name__.lower())
        self.option_file = option_file

    def cursor(self, database=None):
        if not database:
            database = self.database
        try:
            return self.cursors[database]
        except KeyError:
            pass

        self.connections[database] = connection = mysql.connector.connect(
            option_files=self.option_file,
            database=database,
        )
        self.cursors[database] = result = connection.cursor()
        return result

    def execute(self, query, *args, database=None):
        result = self.cursor(database)
        result.execute(query, args)
        return result

    def single_query(self, *args, **kwargs):
        return [row[0] for row in self.execute(*args, **kwargs)]

    def mapping_query(self, *args, **kwargs):
        return dict(self.execute(*args, **kwargs))

    def raw_query(self, *args, **kwargs):
        return list(self.execute(*args, **kwargs))

    def annotated_query(self, header, *args, **kwargs):
        return [dict(zip(header, row)) for row in self.execute(*args, **kwargs)]

    def single(self, table, column, database=None):
        return self.single_query(f'SELECT {column} FROM {table}', database=database)

    def mapping(self, table, source, destination, database=None):
        return self.mapping_query(f'SELECT {source}, {destination} FROM {table}', database=database)

    def get_vars(self, loader, path, entities, cache=True):
        pass
