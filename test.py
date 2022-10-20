import pandas as pd
import numpy as np

data = {
    '1': ['df','as abc','sdf','sdfg','as df', None],
    '2': ['dfa','abcs','sdf as','SAY TOTAL U.S. DOLLARS SIX HUNDRED FIFTY TWO SIXTY SEVEN CENTS ONLY','asdf asdf', 'asd']
}

d = {'key1': ['aaf'], 'key2': ['aaa'], 'key3': ['bbb']}

keys = [k for k, v in d.items() if v in 'aaa in']
print(keys)

if keys:
    print('YES')
# li = ['asd', 'fgd']
# df = pd.DataFrame(data)

# print(df['2'].str.contains('as|sd'))
# df = df.loc[df['2'].str.contains('as|total', regex = True, case = False)]
# print(df)


# ans_column = df.columns[df.eq('abcs').any()]
# ans_row = df[df.eq('abcs').any(1)]
# print(ans_column.values)
# print(ans_row.index.values)
# print(df[(ans_column.values[0])][ans_row.index.values[0]:])
# desc = df[(ans_column.values[0])][ans_row.index.values[0]:]
# desc_list = desc.tolist()
# desc_str = ' '.join(desc_list).split()
# print(desc_str)

# text = '''1
# 6000015667'''

# print(max(text.split()))

# print("____________________")
# re_pattern = 'as\:\s(.*)'

# print(df['1'].str.findall('as\s(.*)'))

# df = df.dropna()
# print(df)