import csv

def fetch_data_from_csv(file_name):
    """
    Fetch data from csv
    :param file_name:
    :return: data set
    """
    with open(file_name, 'rU') as csv_file:
        csv_reader = csv.reader(csv_file)
        credentials_list = list(csv_reader)
    return credentials_list

USER_CREDENTIALS = fetch_data_from_csv('credentials.csv')