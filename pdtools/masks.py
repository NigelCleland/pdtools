import pandas as pd
import numpy as np
from itertools import izip

def eq_mask(self, key, value):
    """ Equality mask, return all rows where a column matches a value """
    return self[self[key] == value]
    
def ge_mask(self, key, value):
    """ Greater than or Equal to Mask, all rows where column is
        greater than the given value"""
    return self[self[key] >= value]
    
def gt_mask(self, key, value):
    """ Greater than mask, all rows where column is greater than a value"""
    return self[self[key] > value]
    
def le_mask(self, key, value):
    """ Less than or Equal to Mask"""
    return self[self[key] <= value]
    
def lt_mask(self, key, value):
    """ Less than Mask"""
    return self[self[key] < value]
    
def ne_mask(self, key, value):
    """ Not Equal to Mask """
    return self[self[key] != value]
    
def gen_mask(self, f):
    """ General purpose mask, pass a function """
    return self[f(self)]
    
def in_eqmask(self, key, values):
    """ A new in mask, e.g. multiple equality masks """
    l = (self.eq_mask(key, value) for value in values)
    return pd.concat(l).drop_duplicates()
    
def mix_eqmask(self, keys, values):
    """ Multiple columns, multiple values, equality considerations """
    l = (self.eq_mask(key, value) for key, value in izip(keys, values))
    return pd.concat(l).drop_duplicates()
    
def mixbool_mask(self, keys, bools, values):
    """ Multiple columns, booleans, values mask """
    bool_dict = {"eq": self.eq_mask, "ge": self.ge_mask, "le": self.le_mask,
                 "lt": self.lt_mask, "gt": self.gt_mask, "ne": self.ne_mask}
    l = (bool_dict[b](key, value) for b, key, value in izip(bools, keys, values))
    return pd.concat(l).drop_duplicates()
    
def bet_mask(self, key, values, inclusive=True):
    """ Return all rows where a column is between two values """
    if inclusive:
        return self.ge_mask(key, values[0]).le_mask(key, values[1])
    else:
        return self.gt_mask(key, values[0]).lt_mask(key, values[1])
        
def mask(self, key, values, how=""):
    """ General Mask, depreciated is not applied to the DataFrame """
    d = {"eq": self.eq_mask, "ne": self.ne_mask, "lt": self.lt_mask,
         "le": self.le_mask, "gt": self.gt_mask, "ge": self.ge_mask,
         "in": self.in_eqmask}
    return d[how](key, values)
    
def top_mask(self, key, percentile, sort=False):
    """ Return all rows in which a column is in the top x percentile """
    df = self.sort(columns=key)
    if sort:
        return df.ge_mask(key, np.percentile(df[key], 100 - percentile)) 
    else:
        return self.ge_mask(key, np.percentile(df[key], 100 -percentile))
        
def bot_mask(self, key, percentile, sort=False):
    """ Return all rows in which a column are in the bottom percentile """
    df = self.sort(columns=key)
    if sort:
        return df.le_mask(key, np.percentile(df[key], percentile))
    else:
        return self.le_mask(key, np.percentile(df[key], percentile))
        
def mid_mask(self, key, percentile, sort=False):
    """ Return values which satisfy the middle x% """
    df = self.sort(columns=key)
    p1 = np.percentile(df[key], 50 - percentile / 2.)
    p2 = np.percentile(df[key], 50 + percentile / 2.)
    if sort:
        return df.ge_mask(key, p1).le_mask(key, p2)
    else:
        return self.ge_mask(key, p1).le_mask(key, p2)
    
    
def apply_masks():
    
    pd.DataFrame.eq_mask = eq_mask
    pd.DataFrame.ge_mask = ge_mask
    pd.DataFrame.gt_mask = gt_mask
    pd.DataFrame.le_mask = le_mask
    pd.DataFrame.lt_mask = lt_mask
    pd.DataFrame.ne_mask = ne_mask
    pd.DataFrame.gen_mask = gen_mask
    pd.DataFrame.in_eqmask = in_eqmask
    pd.DataFrame.mix_eqmask = mix_eqmask
    pd.DataFrame.mixbool_mask = mixbool_mask
    pd.DataFrame.bet_mask = bet_mask
    #pd.DataFrame.mask = mask
    pd.DataFrame.top_mask = top_mask
    pd.DataFrame.bot_mask = bot_mask
    pd.DataFrame.mid_mask = mid_mask
    
    return pd.DataFrame
    
def seq_mask(self, value):
    """ Equality mask for series """
    return self[self == value]
    
def sgt_mask(self, value):
    """ Greater than mask for series """
    return self[self > value]
    
def sge_mask(self, value):
    """ Greater than or equal to mask for series"""
    return self[self >= value]
    
def sle_mask(self, value):
    """ Less than or equal to mask for series """
    return self[self <= value]
    
def slt_mask(self, value):
    """ Less than mask for series """
    return self[self < value]
    
def sne_mask(self, value):
    """ Return all values in which a series is not equal to a value"""
    return self[self != value]
    
def smask(self, value, how=""):
    d = {"ge": self.ge_mask, "le": self.le_mask, "eq": self.eq_mask, 
         "lt": self.lt_mask, "gt": self.gt_mask, "ne": self.ne_mask}
    return d[how](value)
    
def apply_series_masks():
    pd.Series.eq_mask = seq_mask
    pd.Series.gt_mask = sgt_mask
    pd.Series.ge_mask = sge_mask
    pd.Series.lt_mask = slt_mask
    pd.Series.le_mask = sle_mask
    pd.Series.ne_mask = sne_mask
    #pd.Series.mask = smask
    
    return pd.Series
        
        
# Global apply of all masks to be run on import
pd.DataFrame = apply_masks()
pd.Series = apply_series_masks()
        
if __name__ == '__main__':
    pass
