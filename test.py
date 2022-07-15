import pandas as pd
import numpy as np

df = pd.DataFrame([1,2,np.nan])
print(df)

a = df[df.notnull()]
print(df.notnull())
print(a)