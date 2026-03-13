
import pandas as pd


def load_columns_c_to_y(path: str = 'fetal_health.xlsx') -> pd.DataFrame:
	"""Load columns C through Y from the given Excel file and return a cleaned DataFrame.

	This function reads the raw range first (no header), searches for the row
	that contains the column names (looks for 'record_id' header), then
	re-reads using that row as header so resulting DataFrame has proper columns.
	"""
	try:
		raw = pd.read_excel(path, usecols='A:W', engine='openpyxl', header=None)
	except ImportError as e:
		raise ImportError("openpyxl is required to read .xlsx files. Install it with: pip install openpyxl") from e

	header_row = None
	for i, row in raw.iterrows():
		# look for a cell that equals 'record_id' (case-insensitive) or 'baseline value'
		if row.astype(str).str.contains('record_id', case=False, na=False).any() or row.astype(str).str.contains('baseline value', case=False, na=False).any():
			header_row = i
			break

	if header_row is None:
		# fallback: treat first row as header
		header_row = 0

	# read again with correct header
	df = pd.read_excel(path, usecols='A:W', engine='openpyxl', header=header_row)
	# clean column names
	df.columns = [str(c).strip() for c in df.columns]
	return df


if __name__ == '__main__':
	path = 'fetal_health.xlsx'
	try:
		df = load_columns_c_to_y(path)
	except Exception as e:
		print('ERROR:', e)
	else:
		print('Loaded DataFrame with shape:', df.shape)
		print('Columns:', list(df.columns))
		print('\nFirst 5 rows:\n')
		print(df.head().to_string(index=False))

















