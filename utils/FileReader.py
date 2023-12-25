from ..config import SEP, HEADER, DROP_END_ROWS

import pandas as pd
import logging
import io

logger = logging.getLogger(__name__)


class FileReader:
    def __init__(self, sep=SEP, header=HEADER, drop_end_rows=DROP_END_ROWS):
        """
        Initializes FileReader with options for CSV parsing and dropping rows from the end.

        :param sep: Separator used in the CSV file. Defaults to ','.
        :param header: The row (0-indexed) to use as the header. Defaults to 3.
        :param drop_end_rows: Number of rows to drop from the end. Defaults to 1.
        """
        self.sep = sep
        self.header = header
        self.drop_end_rows = drop_end_rows

    def read_csv(self, file_path):
        """
        Reads a CSV file, automatically adjusting the header row if necessary.

        :param file_path: Path to the CSV file.
        :return: DataFrame if successful, raises an error otherwise.
        """
        try:
            df = self._try_read_csv(file_path, self.sep, self.header)
            if self._check_header(df):
                df = self._process_dataframe(df)
                logger.info(f'Successfully read and processed file with header at row {self.header}: {file_path}')
                return df

            # Try using the next line as the header
            df = self._try_read_csv(file_path, self.sep, self.header + 1)
            if self._check_header(df):
                df = self._process_dataframe(df)
                logger.info(f'Successfully read and processed file with header at row {self.header + 1}: {file_path}')
                return df

            # Use custom logic to try to read
            df = self._read_csv_custom_logic(file_path, self.sep, self.header + 1)
            return self._process_dataframe(df)

        except Exception as e:
            self._handle_error(f'Failed to correctly read file {file_path}: {e}')

    def _try_read_csv(self, file_path, sep, header):
        """
        Attempts to read a CSV file with the given header.

        :param file_path: Path to the CSV file.
        :param sep: Separator used in the CSV file.
        :param header: The row to use as the header.
        :return: DataFrame if successful, raises an error otherwise.
        """
        df = pd.read_csv(file_path, sep=sep, header=header)
        if self.drop_end_rows > 0:
            df = df.iloc[:-self.drop_end_rows]
        if df.empty:
            raise ValueError(f"File is empty or contains insufficient rows: {file_path}")
        return df

    @staticmethod
    def _check_header(df):
        """
        Checks if the DataFrame has a valid header.

        :param df: The DataFrame to check.
        :return: True if the header is valid, False otherwise.
        """
        unnamed_columns = [col for col in df.columns if 'Unnamed' in col]
        return len(unnamed_columns) < len(df.columns) / 2

    @staticmethod
    def _process_dataframe(df):
        """
        Processes the DataFrame:
        1. Checks if 'ID' column exists.
        2. Drops rows where 'ID' column is NaN.
        3. Checks if 'ID' values are incrementing as expected.

        :param df: The input DataFrame.
        :return: Processed DataFrame.
        """
        # Check if 'ID' column exists
        if 'ID' not in df.columns:
            raise ValueError("File exception: 'ID' column not found")

        # Drop rows where 'ID' column is NaN
        df = df.dropna(subset=['ID'])

        # Check if 'ID' values are incrementing as expected
        expected_ids = [f'T1P{i}' for i in range(1, len(df) + 1)]
        if not all(df['ID'].values == expected_ids):
            raise ValueError("File exception: 'ID' values are not incrementing as expected")

        return df

    def _read_csv_custom_logic(self, file_path, sep, header):
        """
        Reads a CSV file with custom logic for specific format issues.

        :param file_path: Path to the CSV file.
        :param sep: Separator used in the CSV file. Defaults to ','.
        :param header: The row (0-indexed) to use as the header. Defaults to 4.
        :return: DataFrame if successful, raises an error otherwise.
        """
        with open(file_path, 'r') as f:
            lines = f.readlines()
        if not lines:
            raise ValueError(f"File is empty: {file_path}")

        processed_lines = self._process_lines(lines, header)
        if not processed_lines:
            self._handle_error(f'Failed to process file: {file_path}')

        data = '\n'.join(processed_lines)
        df = pd.read_csv(io.StringIO(data), sep=sep)
        if self.drop_end_rows > 0:
            df = df.iloc[:-self.drop_end_rows]
        return df

    @staticmethod
    def _process_lines(lines, header):
        """
        Processes the lines of the file with custom logic.

        :param lines: The lines of the file.
        :param header: The header row index.
        :return: List of processed lines.
        """
        processed_lines = []
        for i, line in enumerate(lines[header + 1:]):
            parts = line.strip().split(',')
            if len(parts) > 20:
                parts[-2] = parts[-2] + ';' + parts[-1]
                del parts[-1]
                if len(parts) != 20:
                    logger.warning(
                        f'Line {i + header + 2} has an unexpected number of fields ({len(parts)} instead of 20).')
                    continue
            processed_lines.append(','.join(parts))
        return processed_lines

    @staticmethod
    def _handle_error(message):
        logger.error(message)
        raise ValueError(message)
