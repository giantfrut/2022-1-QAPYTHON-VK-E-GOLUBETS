import pandas as pd
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--json", action="store_true")
args = parser.parse_args()
df = pd.read_csv('access.log',
                 sep=' ',
                 usecols=[0, 5, 6, 7],
                 names=['ip_addr', 'request', 'status', 'bytes'],
                 na_values='-',
                 header=None,
                 low_memory=False
                 )

df = df.fillna(0)
df['bytes'] = df['bytes'].astype('int')

new_df = df['request'].str.split(' ', expand=True)
new_df.columns = ['method', 'request', 'protocol']

df = df.drop(df.columns[[1]], axis=1)
final_df = pd.concat([df, new_df], axis=1)


def count_request(dataframe):
    return dataframe.shape[0]


def count_by_method(dataframe):
    return dataframe.method.value_counts()


def top10_requests(dataframe):
    return dataframe.request.value_counts().head(10)


def top5_users_error(dataframe):
    user_error_df = dataframe[['request', 'status', 'bytes', 'ip_addr']]
    return user_error_df.query('status > 400 and status < 500').sort_values('bytes', ascending=False).head(5)


def top5_server_error(dataframe):
    return dataframe.query('status >= 500').ip_addr.value_counts().head(5)


with open("report.txt", "w+") as f:
    print("Общее количество запросов:", count_request(final_df), sep="\n", file=f)
    print("\nОбщее количество запросов по типу:", file=f)
    print(count_by_method(final_df).to_string(), sep="\n", file=f)
    print("\nТоп 10 самых частых запросов:", file=f)
    print(top10_requests(final_df).to_string(), sep="\n", file=f)
    print("\nТоп 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой:", file=f)
    print(top5_users_error(final_df).to_string(index=False), sep="\n", file=f)
    print("\nТоп 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой", file=f)
    print(top5_server_error(final_df).to_string(), sep="\n", file=f)

if args.json:
    with open('report.json', 'w', ) as report_file:
        report_json = {'Total requests': count_request(final_df),
                       'Count requests types': count_by_method(final_df).to_dict(),
                       'Top 10 most frequent requests': top10_requests(final_df).to_dict(),
                       'Top 5 error 4xx by size': top5_users_error(final_df).to_dict('index'),
                       'Top 5 users with 5xx error': top5_server_error(final_df).to_dict()
                       }
        json.dump(report_json, report_file, ensure_ascii=False, indent=4)
