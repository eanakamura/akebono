import os
import re
from akebono.utils import (
    from_pickle,
    list_directory,
)
import akebono.settings as settings
import pandas as pd


def load_train_results(scenario_tag='latest', index_list='all'):
    dirpath = os.path.join(settings.operation_results_dir, scenario_tag)
    file_paths = list_directory(dirpath)
    result_paths = [
        fp for fp in file_paths
        if re.search('.+/train_result_[0-9]+\.pkl$', fp) is not None
    ]
    results = [
        from_pickle(rp)
        for rp in result_paths
    ]
    if not (isinstance(index_list, list) or index_list == 'all'):
        raise ValueError('index_list must be list type or str "all"')
    if not index_list == 'all':
        results = [r for r in results if r['index'] in index_list]

    # convert evaluate result to pandas.DataFrame
    for idx, r in enumerate(results):
        if 'evaluate' in r:
            results[idx]['evaluate']['metrics'] = pd.DataFrame([
                {o['name']:o['value'] for o in met}
                for met in r['evaluate']['metrics']
            ])
    return results