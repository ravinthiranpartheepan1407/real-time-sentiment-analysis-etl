import pandas as pd


def convert_csv_to_json(csv_file_path, json_file_path):
    df = pd.read_csv(csv_file_path, encoding='utf-8')
    df.to_json(json_file_path, orient='records', lines=True, force_ascii=False, default_handler=str)


if __name__ == "__main__":
    csv_path = "./dataset/archive/customer_reviews.csv"
    json_path = "./dataset/archive/output.json"

    convert_csv_to_json(csv_path, json_path)
