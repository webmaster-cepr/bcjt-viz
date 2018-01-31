# -*- coding: utf-8 -*-

def bls():
    """Pulls construction and manufacturing jobs data from the BLS """
    import pandas as pd
    import numpy as np
    import datetime
    
    now = datetime.datetime.now()
    last_year = datetime.datetime.now() - datetime.timedelta(days=365)
    
    us_state_abbrev = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY',
    }
    
    bls_dat = pd.read_excel('https://www.bls.gov/web/laus/table3x.xlsx', skiprows=5, skip_footer=154)

    # complete cases
    bls_dat = bls_dat.dropna(axis=0, how='all')
    
    bls_dat.columns = ['state_name','2016-12-01_total','2017-10-01_total','2017-11-01_total','2017-12-01_total',
                       '2016-12-01_construction','2017-10-01_construction','2017-11-01_construction','2017-12-01_construction',                 '2016-12-01_manufacturing','2017-10-01_manufacturing','2017-11-01_manufacturing','2017-12-01_manufacturing']
    
    # remove parentheses notes from state, translate to abbrevs
    bls_dat['state_name'] = bls_dat['state_name'].str.replace(r"\(.*\)","")
    bls_dat['state'] = bls_dat['state_name'].map(us_state_abbrev)
    bls_dat = bls_dat.drop(['state_name'], axis=1)


    bls_clean = pd.melt(bls_dat, id_vars='state')
    
    # removing nas coded as an mdash
    bls_clean.loc[bls_clean['value']==u'–','value'] = np.NaN
    bls_clean = bls_clean.dropna(axis=0, how='any')    
    
    # convert variable to datetime and create category columns
    bls_clean['date'] = bls_clean['variable'].str.extract('^(.*)(?=_)',expand=True)
    bls_clean['date'] = pd.to_datetime(bls_clean['date'])
    bls_clean = bls_clean[bls_clean['date'] > last_year]
    
    bls_clean['category'] = bls_clean['variable'].str.extract(r'_(.*)',expand=True)
    bls_clean['category'] = bls_clean['category'].str.title()

    bls_clean = bls_clean.drop(['variable'], axis=1)
    
    bls_clean = bls_clean[bls_clean['category'] != 'Total']
    # Adjust Construction category for DE, DC, HI, MD, NE, SD, TN
    combined_states = ['DE', 'DC', 'HI', 'MD', 'NE', 'SD', 'TN']
    
    bls_clean.loc[(bls_clean['state'].isin(combined_states)) & (bls_clean['category']=="Construction"),'category'] = 'Mining, Logging and Construction'    
    
    return bls_clean

def compare(primary,comparison):
    """Compares the BLS dataframe in bls() with another dataframe"""
    import pandas as pd
    
    df1 = primary
    df1 = df1.reset_index(drop=True)
    
    df2 = pd.read_json(comparison)
        
    df2 = df2[df2['category'].isin(df1['category'])]
    df2 = df2[df2['date'].isin(df1['date'])]
    df2 = df2.drop(['state_code'],axis=1)
    df2 = df2.rename(index=str, columns={"code": "state"})
    df2 = df2.reset_index(drop=True)
    df2 = df2[['state','value','date','category']]
       
    def get_different_rows(source_df, new_df):
        """Returns just the rows from the new dataframe that differ from the source dataframe"""
        merged_df = source_df.merge(new_df, indicator=True, how='outer')
        changed_rows_df = merged_df[merged_df['_merge'] == 'right_only']
        return changed_rows_df.drop('_merge', axis=1)
    
    return get_different_rows(df2,df1)