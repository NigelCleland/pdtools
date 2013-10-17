import pandas as pd

def series_merge(self, other, **kwds):
    """
    Merge two series together.
    A method applied to the pandas series class which adds the merge series
    functionality
    
    Usage
    -----
        df = s1.merge_series(s2)
    
    Parameters
    ----------
        self: Applied to a pandas Series class
        other: The series to be merged in.
        **kwds: Additional merge keyword arguments
    
    Returns
    -------
        df: A Pandas DataFrame containing the two series merged on their
            indices
    """
    
    if type(other) in (pd.core.series.Series, pd.core.series.TimeSeries):
        return pd.DataFrame({self.name: self}).merge(pd.DataFrame({other.name: 
               other}),left_index=True, right_index=True, **kwds)
    else:
        raise TypeError("Other must have type series, not", type(other))
        

def merge_series(self, series, **kwds):
    """
    Merge a Series into a DataFrame to create an additional column.
    May merge on either index or column of the DataFrame.
    
    Usage
    -----
        df2 = df1.merge_series(s1, left_index=True) # Index Merge
        df2 = df1.merge_series(s1, left_on="column") # Column merge
        
    Parameters
    ----------
        self: Pandas DataFrame object
        series: The series to be merged into the DataFrame
        **kwds: Additional keyword arguments
        
    Returns
    -------
        df: A new pandas DataFrame consisting of the old DataFrame
            with the series as a new column.
    """
    if type(series) in (pd.core.series.Series, pd.core.series.TimeSeries):
        return self.merge(pd.DataFrame({series.name: series}), 
               right_index=True, **kwds)
    else:
        raise TypeError("Other must have type series, not", type(other)) 
        
# Apply the two methods to the pandas classes on file import.
# These must be maintained at the bottom of the file
# Import usage as follows:
#   import pdtools OR
#   import pdtools.merging
pd.DataFrame.merge_series = merge_series
pd.Series.merge_series = series_merge

if __name__ == '__main__':
    pass
        
