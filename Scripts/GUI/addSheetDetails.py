import pandas as pd

d = pd.DataFrame(None, columns=["a",'b', 'c'])

d= d.append(
    pd.Series([1,2,3], index=d.columns),
    ignore_index=True
)