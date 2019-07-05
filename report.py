from seaborn import load_dataset
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = load_dataset('titanic')
feature = 'age'


class ColumnSummary:
    def __init__(self, data):
        self.data = data

    def statistic_summary(self):
        if not self.dtype_is_object():
            return [f'Min: {self.min()}']


    def num_of_values(self):
        """ number of unique values"""
        return len(self.data.value_counts().to_list())

    def missing_values(self):
        """ return number of missing values"""
        missing_values = self.data.isna().sum()
        return missing_values

    def dtype_is_object(self):
        if self.data.dtype in ('int64', 'float64', 'int32', 'float32'):
            return False
        else:
            return True

    def data_type(self):
        """:return string of datatype"""
        values = self.num_of_values()
        if self.data.dtype in ('int64', 'float64', 'int32', 'float32'):
            if values == 1:
                return "single number"
            elif values == 2:
                return "binary number"
            elif 2 < values <= 10:
                return "category number"
            else:
                return "continuous number"
        elif self.data.dtype == 'object':
            if values == 1:
                return "single text"
            elif values == 2:
                return "binary text"
            elif 2 < values <= 10:
                return "category text"
            else:
                return "general text"
        else:
            return "general text"

    def create_histogram(self):
        """ create a distribution plot from data without missing values"""
        sns.distplot(self.remove_nan_values())

    def remove_nan_values(self):
        return self.data.dropna().copy()

    def outliers(self):
        """:return number of outliers 1.5x the interquartile range"""
        if not self.dtype_is_object():
            data_clean = self.remove_nan_values()
            q1 = self.q1()
            q3 = self.q3()
            iqr = self.q3()-self.q1()
            cut_off = iqr * 1.5
            lower, upper = q1 - cut_off, q3 + cut_off
            mask = data_clean.between(lower, upper)
            data_between = data_clean[mask]
            outliers = len(data_clean) - len(data_between)
            return outliers
        return 'No outliers'

    def mean(self):
        return self.data.mean()

    def mode(self):
        return self.data.mode()

    def min(self):
        return self.data.min()

    def max(self):
        return self.data.max()

    def q1(self):
        return self.data.quantile(q=.25)

    def q3(self):
        return self.data.quantile(q=0.75)

serie = pd.Series([100,30,25,5,1,1,1,1,1,1,1,10000])
# summary = ColumnSummary(data=df[feature])
page = """<!DOCTYPE html>
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="custom.css">
    <link href="custom.css" rel="stylesheet">
  </head>
</html>
<head>
	<meta charset="UTF-8">
</head>
<body>
  <div class="container">
  <div class="row">
    <div class="col-sm">
      <h4>Size of dataframe: 0</h4>
    </div>
    <div class="col-sm">
      One of three columns
    </div>
    <div class="col-sm">
      One of three columns
    </div>
    </div>
  </div>
	<table class="table table-hover table-striped" style=".table">
      <thead>
        <tr>
          <th width="10%" align="left" scope="col">Name</th>
          <th width="10%" align="left"  scope="col">Data Type</th>
          <th width="10%" align="left"  scope="col">Histogram</th>
          <th width="10%" align="left"  scope="col">Observations</th>
          <th width="10%" align="left"  scope="col">Stats</th>
          <th width="10%" align="left"  scope="col">Outliers</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td width="10%" align="left">atext</td>
          <td width="10%" align="left"> atext</td>
          <td><img class="img-fluid" src="https://i.stack.imgur.com/0VrsZ.png" style="width:400px"> </td>
          <td>
            <h5>mean:<br>mode:<br><br>min:<br>max:<br><br>lower bound:<br>upper bound:</h5>
          </td>
          <td>
            <h5>30 missing values<br></h5>
          </td>
          <td>outliers:<br>extreme outliers:</td>
        </tr>
"""
end_page = """  
</tbody>
</table>
</body>
"""
rows_html = []
for column in df.columns.to_list():
    Summary = ColumnSummary(data=df[column])
    datatype = Summary.data_type()
    missing = Summary.missing_values()
    stats = Summary.statistic_summary()
    outliers = Summary.outliers()
    html = f"""
    <tr>
      <td width="10%" align="left"> {column}</td>
      <td width="10%" align="left"> {datatype}</td>
      <td><img class="img-fluid" src="https://i.stack.imgur.com/0VrsZ.png" style="width:400px"> </td>
      <td>{missing}</td>
      <td>{stats}</td>
      <td>{outliers}</td>
    </tr>
    """
    rows_html.append(html)


merged_html = page + "".join(rows_html) + end_page
with open("seenopsis_output.html", "w") as html_file:
    html_file.write(merged_html)
    html_file.close()