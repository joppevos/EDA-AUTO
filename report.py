from seaborn import load_dataset
import pandas
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# features = df.columns.tolist()
df = load_dataset('titanic')
feature = 'age'


class ColumnSummary:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def num_of_values(self):
        """ number of individual values"""
        return len(self.data.value_counts().to_list())

    def value_count_summary(self):
        """ summary of the value counts"""
        count = self.data.count()
        num_of_values = self.num_of_values()
        missing_values = df[feature].isna().sum()
        print(f'Total Values:\t{count}\nUnique values:\t{num_of_values}\nMissing values:\t{missing_values}')

    def type_for_operation(self):
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

    def statistics_summary(self):
        mean = self.mean()
        mode = self.mode()
        min = self.min()
        max = self.max()
        q1 = self.lower_quantile()
        q3 = self.upper_quantile()
        print(f"""mean:\t{mean}\nmode:\t{mode}""")

    def mean(self):
        return self.data.mean()

    def mode(self):
        return self.data.mode().values[0]

    def min(self):
        return self.data.min().values[0]

    def max(self):
        return self.data.max().values[0]

    def lower_quantile(self):
        return self.data.quantile(q=.25)

    def upper_quantile(self):
        return self.data.quantile(q=0.75)


summary = ColumnSummary(data=df[feature], name=feature)
# summary.statistics_summary()
print(summary.mode())
# summary.create_histogram()
# for every column
# for value in df.columns.value:
# show the first 4 values
# report the number of appereances
# type of dtype
# report a matplot graph
# statistical values. mean min, max, up, low, quartiles and outliers
# report NaN values
