from collections import namedtuple
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from seaborn import load_dataset
from IPython.core.display import display, HTML

df = load_dataset('titanic')

class ColumnSummary:
    def __init__(self, data):
        self.data = data

    def statistic_summary(self):
        stats = namedtuple('stats', ['mean', 'mode', 'min', 'max', 'upper', 'lower'])
        if not self.dtype_is_object():
            return stats(round(self.mean(), 2), self.mode()[0], self.min(),
                         self.max(), round(self.q3(), 2), round(self.q1(), 2))
        else:
            return stats('', self.mode()[0], '', '', '', '')

    def num_of_values(self):
        """ number of unique values"""
        return len(self.data.dropna().unique())

    def missing_values(self):
        """ return number of missing values"""
        missing_values = self.data.isna().sum()
        if missing_values:
            fracture = missing_values/self.data.count()
            return f"N={missing_values},{round(fracture, 2)}%"
        else:
            return "No missing values"

    def dtype_is_object(self):
        if self.data.dtype in ('int64', 'float64', 'int32', 'float32'):
            return False
        else:
            return True

    def data_type(self):
        """:return string of datatype"""
        values = self.num_of_values()
        dtype = str(self.data.dtype)
        if dtype in ('int64', 'float64', 'int32', 'float32'):
            if values == 1:
                return f"{dtype}=single number"
            elif values == 2:
                return f"{dtype}=binary number"
            elif 2 < values <= 10:
                return f"{dtype}=category number"
            else:
                return f"{dtype}=continuous number"
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
            return str(dtype)

    def create_histogram(self, i):
        """
        create a distribution plot from data without missing values
        :param i: iteration for each histogram
        """
        fig, ax = plt.subplots(1, 1, figsize = (5, 5), dpi=100)
        sns.set(style="whitegrid")
        if self.dtype_is_object() or self.num_of_values() <= 10:
            sns.countplot(self.remove_nan_values())
        else:
            sns.distplot(self.remove_nan_values())
        # styling
        ax.set_xlabel('')
        ax.set_ylabel('')
        plt.rc('axes', labelsize=30)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=15)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=15)
        plt.savefig(f'hist_images/histogram{i}.png', bbox_inches='tight')

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
            if outliers == 0:
                return 'No outliers'
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

def create_html_layout(df):
    """ create html page to render out
    :param df: dataframe
    """
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
          <h4>Edas report: Exploratory data analysis</h4>
        </div>
        <div class="col-sm">
          <h3>Inspecting dataframe of size: {size}
        </div>
        <div class="col-sm">
          One of three columns
        </div>
        </div>
      </div>
    	<table class="table table-hover table-striped" style=".table">
          <thead>
            <tr>
              <th width="10%" align="left" scope="col">Variable Name</th>
              <th width="10%" align="left"  scope="col">Data Type</th>
              <th width="10%" align="left"  scope="col">Histogram</th>
              <th width="10%" align="left"  scope="col">Stats</th>
              <th width="10%" align="left"  scope="col">Missing NA</th>
              <th width="10%" align="left"  scope="col">Outliers</th>
            </tr>
          </thead>
          <tbody>""".format(size=df.size)
    end_page = """  
    </tbody>
    </table>
    </body>
    """
    rows_html = []
    for i, column in enumerate(df.columns):
        Summary = ColumnSummary(data=df[column])
        datatype = Summary.data_type()
        missing = Summary.missing_values()
        stats = Summary.statistic_summary()
        outliers = Summary.outliers()
        Summary.create_histogram(i)
        html = f"""
        <tr>
          <td width="10%" align="left"> {column}</td>
          <td width="10%" align="left"> {datatype}</td>
          <td><img class="img-fluid" src="hist_images/histogram{i}.png" style="width:400px"> </td>
          <td>mean: {stats.mean}<br>
              mode: {stats.mode}<br><br>
              min: {stats.min}<br>
              max: {stats.max}<br><br>
              lower-bound: {stats.lower}<br>
              upper-bound: {stats.upper}<br></td>
          <td>{missing}</td>
          <td>{outliers}</td>
        </tr>
        """
        rows_html.append(html)
        rows_html.append(html)

    merged_html = page + "".join(rows_html) + end_page
    return merged_html



with open("seenopsis_output.html", "w") as html_file:
    html_file.write(merged_html)
    html_file.close()