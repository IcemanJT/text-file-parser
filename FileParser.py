# Author: Jeremi Torój
# Date: 27/05/2024

import pandas as pd
import re
import json
from flatten_json import flatten


class FileParser:

    def process(self, file):
        filename = file.filename
        if filename.endswith('.txt'):
            return self._process_txt_file(file)
        elif filename.endswith('.csv'):
            return self._process_csv_file(file)
        elif filename.endswith('.json'):
            return self._process_json_file(file)
        else:
            raise ValueError('Invalid file format')

    @staticmethod
    def _process_json_file(file):
        data = json.load(file)
        #  flatten() returns dictionary with all nested keys as one level keys but maintains the original structure
        flat_data = flatten(data)

        summary = {
            'flat_data': flat_data,
            'keys': list(flat_data.keys()),
            'values': list(flat_data.values()),
            'num_keys': len(flat_data),
            'num_values': len(flat_data.values()),
            'unique_values': len(set(flat_data.values())),
        }

        return summary

    @staticmethod
    def _process_csv_file(file):
        df = pd.read_csv(file)

        summary = {
            "num_rows": len(df),
            "num_columns": len(df.columns),
            #  nunique() returns number of unique values in each column
            "unique_values": {col: df[col].nunique() for col in df.columns},
            #  describe() returns basic statistics for each column
            #  std - standard deviation
            "categorical_column_stats": df.describe(include=['object']).to_dict(),
            "numerical_column_stats": df.describe().to_dict(),
        }

        return summary

    @staticmethod
    def _process_txt_file(file):
        content = file.read().decode('utf-8')

        num_rows = content.count('\n')
        num_words = len(re.findall(r'\w+', content))
        num_chars = len(content)
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        #  I assume that phone number has 9/10 digits and can be separated by space or dash and may have country code
        phone_pattern = r'(\+\d{1,3}\s?)?(\d{3}[\s-]?\d{3}[\s-]?\d{3,4})'
        matched_numbers = re.findall(phone_pattern, content)
        phone_numbers = [''.join(match) for match in matched_numbers]

        urls = re.findall(r'(https?://\S+)', content)

        summary = {
            'num_rows': num_rows,
            'num_words': num_words,
            'num_chars': num_chars,
            'emails': emails,
            'phone_numbers': phone_numbers,
            'urls': urls,
        }

        return summary
