import os
import sys
import requests
import pandas as pd
from ratelimit import rate_limited

AMC_URL = 'https://api.sec.or.th/FundFactsheet/fund/amc'
FUND_URL = 'https://api.sec.or.th/FundFactsheet/fund/amc/{unique_id}'
CSV_FILENAME = 'sec-funds.csv'
CSV_ENCODING = 'utf-8'

headers = {
    'Ocp-Apim-Subscription-Key': os.getenv('SEC_OPEN_API_KEY', default=None)
}

fund_df_cols = [
    'proj_id',
    'proj_abbr_name',
    'proj_name_en',
    'proj_name_th',
    'unique_id'
]


# 5 calls/sec
class RateLimiter:
    def __init__(self, headers):
        self.headers = headers

    @rate_limited(1500, 300)
    def call_get_api(self, url):
        res = requests.get(url, headers=self.headers)
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f'Cannot request API', {str(e)})
            raise

        return res


limiter = RateLimiter(headers)

print('Requesting amc info')
res = requests.get(AMC_URL, headers=headers)
try:
    res.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f'Cannot request amc info {str(e)}')
    sys.exit(1)

amc = pd.read_json(res.content)

all_funds = pd.DataFrame(columns=fund_df_cols)

print('Requesting funds info')
for unique_id in amc.unique_id:
    try:
        res = limiter.call_get_api(FUND_URL.format(unique_id=unique_id))
        projects = pd.read_json(res.content)
        all_funds = all_funds.append(projects[fund_df_cols])
    except Exception:
        print(f'Cannot get funds for amc id {unique_id}')

print(f'There are in total {len(all_funds.index)} funds')

all_funds.to_csv(CSV_FILENAME, encoding=CSV_ENCODING, index=False)
print(f'csv file saved as {CSV_FILENAME}')
