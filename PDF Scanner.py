import argparse
import re
import glob

from datetime import datetime as dt
import pdfplumber
import pandas as pd

parser = argparse.ArgumentParser()



class pdfScraper:
    def __init__(self, files):
        arr_of_files = (glob.glob(files + '\*pdf'))
        self.files = arr_of_files
        self.row = ['Date', 'Description', 'Amount']
        self.check = re.compile(r'\A\d{2}/\d{2} \w+')

    def categorize(self, line):
        line = line.split()
        sub = ''.join(line[1:-2])

        del line[1:-2]

        line.insert(1, sub)

        line = line[: -2] + line[-2: -1]

        line[-1] = int(float(line[-1]))

        return line

    def scan(self):
        lines = []

        for file in self.files:
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    for line in text.split('\n'):
                        comp = self.check.search(line)
                        if comp:
                            line = line.replace(',', '')
                            retrievedLineArray = self.categorize(line)
                            lines.append(retrievedLineArray)
        return lines

if __name__ == '__main__':
    parser.add_argument(
        "--dir",
        default = '',
        help="The dictionary to scan pdfs from"
    )

    parser.add_argument(
        "--output",
        default='Extracted Bank Statement.csv'.format(dt.today().strftime('%Y%m%d'))
    )

    args = parser.parse_args()



    files = args.dir

    files = str(files)

    test = pdfScraper(files)

    df = pd.DataFrame(test.scan())
    df.columns = test.row

    output_file = args.output

    df.to_csv(output_file)



'''
df = pd.DataFrame(lines)
df.columns = Row

filtered_df = df[df['Description'].str.contains('withdrawal', case = False)]

print(filtered_df)

Total = filtered_df['Amount'].sum()

print(Total)



'''










