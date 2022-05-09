import pandas as pd


def count_request(dataframe):
    return dataframe.shape[0]


def count_by_method(dataframe):
    df = dataframe.method.value_counts().to_frame().reset_index()
    df.columns = ['method', 'count']
    return df


def top_requests(dataframe, entry=10):
    df = dataframe.request.value_counts().head(entry).to_frame().reset_index()
    df.columns = ['request', 'count']
    return df


def top_users_error(dataframe, entry=5):
    df = dataframe[['request', 'status', 'bytes', 'ip_addr']]
    df = df.query('status >= 400 and status < 500').sort_values('bytes', ascending=False).head(entry).reset_index()
    return df


def top_server_error(dataframe, entry=5):
    df = dataframe.query('status >= 500').ip_addr.value_counts().head(entry).to_frame().reset_index()
    df.columns = ['ip_addr', 'count']
    return df
