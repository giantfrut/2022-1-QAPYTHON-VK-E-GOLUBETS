import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from mysql.orm_models import UsersTest, Base


class MysqlClient:

    def __init__(self, user, password, db_name, host='0.0.0.0', port=3306):
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

    def create_admin(self):
        sql_create_user = "CREATE USER IF NOT EXISTS '%s'@'localhost' IDENTIFIED BY '%s';" % ("test_qa", "qa_test")
        # sql_grant_all = "GRANT ALL ON *.* TO '%s'@'localhost'" % "test_qa"
        self.execute_query(sql_create_user, fetch=False)
        # self.execute_query(sql_grant_all, fetch=False)
        self.execute_query(f'FLUSH PRIVILEGES', fetch=False)

    def create_test_users_table(self):
        if not inspect(self.engine).has_table('test_users'):
            Base.metadata.tables['test_users'].create(self.engine)

    def add_user_db(self, user):
        entry = UsersTest(
            name=user.name,
            surname=user.surname,
            middle_name=user.middle_name,
            username=user.username,
            password=user.password,
            email=user.email,
            access=user.access,
            active=1,
        )
        self.session.add(entry)
        self.session.commit()

    def prepare_test_users(self):

        entry = UsersTest(
            name='Evgenii',
            surname='Golubets',
            middle_name='QA',
            username='giantfrut',
            password='vkeducation',
            email='giantfrut@gmail.com',
            access=1,
            active=1
        )
        self.session.add(entry)
        self.session.commit()

    def execute_query(self, query, fetch=True):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchone()

    # def select_user(self, username):
    #     self.session.commit()
    #     # resp = self.session.query(UsersTest).filter_by(username=username).first()
    #     # Берем так и не выебываемся, пишем норм тесты
    #     entry = select(UsersTest).where(UsersTest.username == username)
    #     return self.execute_query(entry)

    def select_db(self, username):
        self.session.commit()
        return self.session.query(UsersTest).filter_by(username=username).first()

    # def delete_user_db(self):
    #     entry = UsersTest.filter_by(username='giantfrut').delete('giantfrut')
    #     self.execute_query(entry)
    #     self.session.commit()

