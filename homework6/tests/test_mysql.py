from model.models import TotalRequests, FrequentRequests, ServerErrors, CountTypes, UserErrors
from tests.base import MysqlBase
import pytest
from utils import log_analyzer


class TestMySql(MysqlBase):

    def test_total_requests(self, dataframe):
        df_total = log_analyzer.count_request(dataframe)
        self.mysql.prepare_total_requests(df_total)
        assert self.mysql.session.query(TotalRequests).count() == 1

    def test_count_types(self, dataframe):
        df = log_analyzer.count_by_method(dataframe)
        self.mysql.prepare_count_types(df)
        assert self.mysql.session.query(CountTypes).count() == df.shape[0]

    def test_frequent_requests(self, dataframe):
        df = log_analyzer.top_requests(dataframe)
        self.mysql.prepare_frequent_requests(df)
        assert self.mysql.session.query(FrequentRequests).count() == df.shape[0]

    def test_user_errors(self, dataframe):
        df = log_analyzer.top_users_error(dataframe)
        self.mysql.prepare_user_errors(df)
        assert self.mysql.session.query(UserErrors).count() == df.shape[0]

    def test_server_errors(self, dataframe):
        df = log_analyzer.top_server_error(dataframe)
        self.mysql.prepare_server_errors(df)
        assert self.mysql.session.query(ServerErrors).count() == df.shape[0]
