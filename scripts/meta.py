from datetime import datetime
from pytz import timezone


async def get_est_time():
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    eastern = timezone('US/Eastern')
    est_raw = datetime.now(eastern)
    return est_raw.strftime(fmt)


async def get_phx_time():
    fmt = '%Y-%m-%d %H:%M:%S %Z'
    phx = timezone('America/Phoenix')
    est_raw = datetime.now(phx)
    return est_raw.strftime(fmt)
