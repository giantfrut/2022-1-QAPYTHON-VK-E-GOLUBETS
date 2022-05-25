import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from model.models import Base, UserErrors, TotalRequests, FrequentRequests, ServerErrors, CountTypes


class MysqlClient:

    def __init__(self, user, password, db_name, host='127.0.0.1', port=3306):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name

        self.connection = None
        self.engine = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url, encoding='utf8')
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def create_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database if EXISTS {self.db_name}', fetch=False)
        self.execute_query(f'CREATE database {self.db_name}', fetch=False)

    def create_total_requests_table(self):
        if not inspect(self.engine).has_table('TotalRequests'):
            Base.metadata.tables['TotalRequests'].create(self.engine)

    def create_count_types_table(self):
        if not inspect(self.engine).has_table('CountTypes'):
            Base.metadata.tables['CountTypes'].create(self.engine)

    def create_frequent_requests_table(self):
        if not inspect(self.engine).has_table('FrequentRequests'):
            Base.metadata.tables['FrequentRequests'].create(self.engine)

    def create_user_errors_table(self):
        if not inspect(self.engine).has_table('UserErrors'):
            Base.metadata.tables['UserErrors'].create(self.engine)

    def create_server_errors_table(self):
        if not inspect(self.engine).has_table('ServerErrors'):
            Base.metadata.tables['ServerErrors'].create(self.engine)

    def execute_query(self, query, fetch=True):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def prepare_total_requests(self, df):
        entry = TotalRequests(count=df)
        self.session.add(entry)
        self.session.commit()

    def prepare_count_types(self, df):
        for row in df.itertuples():
            entry = CountTypes(method=row.method, count=row.count)
            self.session.add(entry)
        self.session.commit()

    def prepare_frequent_requests(self, df):
        for row in df.itertuples():
            entry = FrequentRequests(request=row.request, count=row.count)
            self.session.add(entry)
        self.session.commit()

    def prepare_user_errors(self, df):
        for row in df.itertuples():
            entry = UserErrors(ip_addr=row.ip_addr, request=row.request,
                               status=row.status, bytes=row.bytes)
            self.session.add(entry)
        self.session.commit()

    def prepare_server_errors(self, df):
        for row in df.itertuples():
            entry = ServerErrors(ip_addr=row.ip_addr, count=row.count)
            self.session.add(entry)
        self.session.commit()
