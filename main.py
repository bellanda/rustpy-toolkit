import polars as pl

from expression_lib import pig_latinnify

df = pl.DataFrame(
    {
        "convert": ["pig", "latin", "is", "silly"],
    }
)
out = df.with_columns(pig_latin=pig_latinnify("convert"))
print(out)
