import pytest
from edas import Edas, ColumnSummary
from seaborn import load_dataset, get_dataset_names
import pandas as pd

def test_dataframe_input():
    """ test catch for non existing path """
    with pytest.raises(FileNotFoundError):
        Edas('nonexisting.csv')

def test