import pandas as pd
import numpy as np
from itertools import combinations

def get_pair(group):
    edges_set = set()
    for subgraph in group:
        edges_sub_graph = combinations(subgraph, 2)
        edges_set.update(edges_sub_graph)
        print("processing_data_done")
    return list(edges_set)


class Grouping_mw_irt:
    """
    This class is designed to process and group mass spectrometry data based on specific criteria. Upon initialization, the class accepts a pandas DataFrame, sorts it by molecular weight (MW), and resets its index.
    The method group_and_delete_duplicates groups values from a list based on a given tolerance. This grouping can be done either in Daltons ('Da') or parts per million ('ppm'). 
    The method identifies clusters of values that are close to each other within the specified tolerance.

    The grouper method groups values from an iterable based on a given iRT (indexed retention time) tolerance. It yields groups of consecutive values that are within the tolerance of each other.

    The irt_grouping method further refines the grouping process by sorting and grouping values based on both MW and iRT. It uses the irt_grouper method to group values based on iRT after sorting them.

    The primary method, group_sequences, orchestrates the entire grouping process. It first groups sequences based on MW using the group_and_delete_duplicates method. Then, it refines this grouping based on iRT using the my_attempt method. The final groups are then filtered to ensure uniqueness and are returned.

    Usage:
    mass_info = Grouping_MS1(data_frame)
    grouped_sequences = mass_info.group_sequences(tolerance1, tolerance2, unit='Da')


    Key Methods and Parameters:

    group_and_delete_duplicates(lst, tolerance1, unit): Groups values from lst based on tolerance1 and unit.
    irt_grouper(iterable, tolerance2): Groups values from iterable based on tolerance2.
    my_attempt(nested_list, tolerance2): Refines grouping of nested_list based on iRT using tolerance2.
    group_sequences(tolerance1, tolerance2, unit): Orchestrates the grouping process using tolerance1, tolerance2, and unit.
    The class provides a structured approach to group mass spectrometry data based on both molecular weight and indexed retention time, ensuring precise and meaningful groupings.
"""
    def __init__(self, data_frame):
        self.df = data_frame
        #self.df = self.df.drop_duplicates(subset=['Name'])
        self.df['index'] = self.df.index
        self.df = self.df.sort_values(by='MW')
        self.df = self.df.reset_index(drop=True)
    
    def group_and_delete_duplicates(self, lst, tolerance1, unit='Da'):
        if unit == 'ppm':
            tolerance1 = (tolerance1 / 1e6) * lst[0]
        groups = set()
        indices = list(range(len(lst)))
        indices.sort(key=lambda i: lst[i])
        for i in range(len(lst)):
            group = {indices[i]}
            for j in range(i+1, len(lst)):
                if lst[indices[j]] - lst[indices[i]] <= tolerance1:
                    group.add(indices[j])
                else:
                    break
            if not any(group.issubset(existing_group) for existing_group in groups):
                groups.add(frozenset(group))
        final_groups = [list(group) for group in groups]
        return final_groups
    
    def grouper(self, iterable, tolerance2):
        group = []
        for item in iterable:
            if not group or item - group[0] <= tolerance2:
                group.append(item)
            else:
                yield group
                group = [item]
        if group:
            yield group
    
    def irt_grouping(self, nested_list, tolerance2):
        my_group = []
        for k in range(len(nested_list)):
            prev = None
            group = []
            df_mw = np.array([el[1] for el in nested_list[k]])
            df_irt = np.array([el[2] for el in nested_list[k]])       
            df_irt_index = np.array([int(el[3]) for el in nested_list[k]])
            new_indexes = np.argsort(df_irt)
            df_mw_sorted = df_mw[new_indexes]
            df_irt_sorted = df_irt[new_indexes]
            df_irt_index_sorted = df_irt_index[new_indexes]
            group = list(self.grouper(df_irt_sorted, tolerance2))
            iter_index = iter(df_irt_index_sorted)
            result = [[next(iter_index) for _ in group] for group in group]
            my_group.append(result)
        return my_group
    
    def group_sequences(self, tolerance1, tolerance2, unit='Da'):
        groups = self.group_and_delete_duplicates(self.df.iloc[:, 1].tolist(), tolerance1, unit=unit)
        out = [[self.df.iloc[y].values.tolist() for y in x] for x in groups] 
        group = self.irt_grouping(out, tolerance2)

        fset = set()
        for sub_list in group:
            temp_set = set()
            for item in sub_list:
                temp_set.add(frozenset(item))
            fset |= temp_set

        group = sorted([list(x) for x in fset], key=lambda x: x[0])
        d = {}
        for i, l in enumerate(group):
            for v in l:
                d.setdefault(v, set()).add(i)

        group = [l for i, l in enumerate(group) if not set.intersection(*(d[x] for x in l)).difference({i})]
        print("Grouping Done")
        return group



