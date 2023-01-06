from concurrent.futures import ThreadPoolExecutor
from itertools import chain

from ei.core import defaults


def bulk_action(fn, regions, account_ids):
    tasks = []
    with ThreadPoolExecutor(max_workers=defaults.CORES) as executor:
        for account_id in account_ids:
            for region in regions:
                tasks.append(executor.submit(fn, region, account_id))

    results = [t.result() for t in tasks]
    results = chain(*results)

    return results
