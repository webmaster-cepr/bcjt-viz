def scrape(date="2016-12-01", transformation=True):
    """ main function to scrape and clean data to prepare for charting """
    
    import pandas as pd
    import datetime

    now = datetime.datetime.now()
    
    if (transformation == True):
        trans = "&transformation=pch"
    else:
        trans = ""

    states_group_one = {"AL":["SMU01000003000000001SA","ALCONS","SMS01000001000000001","SMS01000001500000001"],
    "AK":["AKMFG","AKCONS","AKNRMN","SMS02000001500000001"],
    "AZ":["AZMFG","AZCONS","AZNRMN","SMS04000001500000001"],
    "AR":["ARMFG","ARCONS","ARNRMN","SMS05000001500000001"],
    "CA":["CAMFG","CACONS","CANRMN","SMS06000001500000001"],
    "CO":["COMFG","COCONS","CONRMN","SMS08000001500000001"],
    "CT":["CTMFG","CTCONS","SMS09000001000000001","SMS09000001500000001"],
    "DC": ["SMU11000003000000001SA","","","SMS11000001500000001"],
    "DE":["DEMFG","","","SMS10000001500000001"],
    "FL":["FLMFG","FLCONS","SMU12000001000000001SA","SMS12000001500000001"],
    "GA":["GAMFG","GACONS","","SMS13000001500000001"],
    "HI":["HIMFG","","","SMS15000001500000001"]
    }
    
    states_group_two = {"ID":["IDMFG","IDCONS","IDNRMN","SMS16000001500000001"],
        "IL":["ILMFG","ILCONS","SMS17000001000000001","SMS17000001500000001"],
        "IN":["INMFG","INCONS","SMS18000001000000001","SMS18000001500000001"],
        "IA":["IAMFG","IACONS","IANRMN","SMS19000001500000001"],
        "KS":["KSMFG","KSCONS","KSNRMN","SMS20000001500000001"],
        "KY":["KYMFG","KYCONS","KYNRMN","SMS21000001500000001"],
        "LA":["LAMFG","LACONS","SMS22000001000000001","SMS22000001500000001"],
        "ME":["MEMFG","MECONS","MENRMN","SMS23000001500000001"],
        "MD":["MDMFG","SMU24000002000000001SA","SMU24000001000000001SA","SMS24000001500000001"],
        "MA":["MAMFG","MACONS","MANRMN","SMS25000001500000001"],
        "MI":["MIMFG","MICONS","MINRMN","SMS26000001500000001"],
        "MN":["MNMFG","MNCONS","MNNRMN","SMS27000001500000001"]
    }
    
    states_group_three = { "MS":["MSMFG","MSCONS","SMS28000001000000001","SMS28000001500000001"],
        "MO":["MOMFG","MOCONS","SMS29000001000000001","SMS29000001500000001"],
        "MT":["MTMFG","MTCONS","MTNRMN","SMS30000001500000001"],
        "NE":["NEMFG","SMU31000002000000001SA","SMU31000001000000001SA","SMS31000001500000001"],
        "NV":["NVMFG","NVCONS","NVNRMN","SMS32000001500000001"],
        "NH":["NHMFG","NHCONS","SMS33000001000000001","SMS33000001500000001"],
        "NJ":["NJMFG","NJCONS","SMS34000001000000001","SMS34000001500000001"],
        "NM":["NMMFG","NMCONS","NMNRMN","SMS35000001500000001"],
        "NY":["NYMFG","NYCONS","NYNRMN","SMS36000001500000001"],
        "NC":["NCMFG","NCCONS","SMS37000001000000001","SMS37000001500000001"],
        "ND":["NDMFG","NDCONS","NDNRMN","SMS38000001500000001"],
        "OH":["OHMFG","OHCONS","OHNRMN","SMS39000001500000001"],
    }
    
    states_group_four = { "OK":["OKMFG","OKCONS","OKNRMN","SMS40000001500000001"],
        "OR":["ORMFG","ORCONS","ORNRMN","SMS41000001500000001"],
        "PA":["PAMFG","PACONS","PANRMN","SMS42000001500000001"],
        "RI":["RIMFG","RICONS","SMS44000001000000001","SMS44000001500000001"],
        "SC":["SCMFG","SCCONS","SMU45000001000000001SA","SMS45000001500000001"],
        "SD":["SDMFG","","","SMS46000001500000001"],
        "TN":["TNMFG","","","SMS47000001500000001"],
        "TX":["TXMFG","TXCONS","TXNRMN","SMS48000001500000001"],
        "UT":["UTMFG","UTCONS","UTNRMN","SMS49000001500000001"],
        "VT":["VTMFG","VTCONS","SMS50000001000000001","SMS50000001500000001"],
        "VA":["VAMFG","VACONS","VANRMN","SMS51000001500000001"],
        "WA":["WAMFG","WACONS","WANRMN","SMS53000001500000001"]
    }
    
    states_group_five = { "WV":["WVMFG","WVCONS","WVNRMN","SMS54000001500000001"],
        "WI":["WIMFG","WICONS","WINRMN","SMS55000001500000001"],
        "WY":["WYMFG","WYCONS","WYNRMN","SMS56000001500000001"]
    }
    
    states_groups = states_group_one.copy()
    states_groups.update(states_group_two)
    states_groups.update(states_group_three)
    states_groups.update(states_group_four)
    states_groups.update(states_group_five)
    
    base_link = "https://fred.stlouisfed.org/graph/fredgraph.csv?mode=fred&id="
    
    mfg_links = []
    cons_links = []
    mine_links = []
    cons_mine_links = []
    all_jobs_links = []
    
    mfg_one = mfg_two = mfg_three = mfg_four = mfg_five = base_link
    cons_one = cons_two = cons_three = cons_four = cons_five = base_link
    mine_one = mine_two = mine_three = mine_four = mine_five = base_link
    cons_mine_one = cons_mine_two = cons_mine_three = cons_mine_four = cons_mine_five = base_link
    all_jobs_one = all_jobs_two = all_jobs_three = all_jobs_four = all_jobs_five = base_link
    
    # magic of appending states to abbreviations here
    
    def add_links(state_group,l=[]):
        """ function to create, concatenate links for scraping """
        for key,value in state_group.items():
            if str(value[0]) != "":
                l[0] = l[0] + str(value[0]) + "%2C"
            if str(value[1]) != "":
                l[1] = l[1] + str(value[1]) + "%2C"
            if str(value[2]) != "":
                l[2] = l[2] + str(value[2]) + "%2C"
            if str(value[3]) != "":
                l[3] = l[3] + str(value[3]) + "%2C"
            if str(value[0]) != "" and str(value[3]) != "":
                l[4] = l[4] + str(value[0]) + "_" + str(value[3]) + "%2C"
            
        mfg_links.append(l[0] + trans + "%2C" * len(state_group))
        cons_links.append(l[1] + trans)
        mine_links.append(l[2] + trans)
        cons_mine_links.append(l[3] + trans)
        all_jobs_links.append(l[4] + "&transformation=" + "lin_lin%2C" * len(state_group) +
                                "&fml=" + "a%2Bb%2C" * len(state_group) + "&fgst=" + (trans[-3:] + "%2C") * len(state_group))
            
    add_links(states_group_one,l=[mfg_one,cons_one,mine_one,cons_mine_one, all_jobs_one])
    add_links(states_group_two,l=[mfg_two,cons_two,mine_two,cons_mine_two, all_jobs_two])
    add_links(states_group_three,l=[mfg_three,cons_three,mine_three,cons_mine_three, all_jobs_three])
    add_links(states_group_four,l=[mfg_four,cons_four,mine_four,cons_mine_four, all_jobs_four])
    add_links(states_group_five,l=[mfg_five,cons_five,mine_five,cons_mine_five, all_jobs_five])
    
    links = mfg_links + cons_links + mine_links + cons_mine_links + all_jobs_links
    print(links)
    
    # DATA FRAME INITIALIZATION
    
    dat = pd.DataFrame()
    x = 0

    for link in links:
        try:
            temp = pd.read_csv(link)
        except:
            print("Oops! Could not reach " + link + ".")
        if x > 0:
            dat = pd.concat([dat,temp.iloc[:,1:]], axis=1)
        else:
            dat = pd.concat([dat,temp], axis=1)
        x = x + 1
        
    dat = pd.melt(dat, id_vars=['DATE'], var_name='state_code', value_name='value')
    
    # END DATA FRAME

    # cleaning dat
    dat['DATE'] = pd.to_datetime(dat['DATE'])
    dat = dat[dat['DATE'] >= date]
    dat.index = range(1, len(dat) + 1)

    dat['code'] = ""
    dat['category'] = ""
    
    code_ext = "_PCH" if len(trans) > 0 else ""
    
    # states column from state codes
    for x in range(0,len(dat)):
        for key, value in states_groups.items():
            if dat.iloc[x,1] == str(value[0]) + code_ext:
                dat.iloc[x,3] = key
                dat.iloc[x,4] = "Manufacturing"
            
            if dat.iloc[x,1] == str(value[1]) + code_ext:
                dat.iloc[x,3] = key
                dat.iloc[x,4] = "Construction"

            if dat.iloc[x,1] == str(value[2]) + code_ext:
                dat.iloc[x,3] = key
                dat.iloc[x,4] = "Mining and Logging"

            if dat.iloc[x,1] == str(value[3]) + code_ext:
                dat.iloc[x,3] = key
                dat.iloc[x,4] = "Mining, Logging and Construction"
            
            if dat.iloc[x,1] == str(value[0]) + "_" + str(value[3]):
                dat.iloc[x,3] = key
                dat.iloc[x,4] = "All"
            
    mfg_na = set(states_groups.keys()).difference(set(dat[dat['category']=="Manufacturing"]['code']))
    cons_na = set(states_groups.keys()).difference(set(dat[dat['category']=="Construction"]['code']))
    mine_na = set(states_groups.keys()).difference(set(dat[dat['category']=="Mining and Logging"]['code']))
    cons_mine_na = set(states_groups.keys()).difference(set(dat[dat['category']=="Mining, Logging and Construction"]['code']))
    all_jobs_na = set(states_groups.keys()).difference(set(dat[dat['category']=="All"]['code']))
    
    # solving the nas by date issue
    date_unique = dat.DATE.unique()
    
    def add_nas(df,na_set,category):
        """ function to identify and assign null values to missing states """
        for s in list(na_set):
            for n in range(0,len(date_unique)):
                df = df.append(pd.DataFrame([[date_unique[n],s + code_ext,None,s,category]], columns=df.columns.values))

        return df
    
    # dat = add_nas(dat,mfg_na,"Manufacturing")
    dat = add_nas(dat,cons_na,"Construction")
    dat = add_nas(dat,mine_na,"Mining and Logging")
    # dat = add_nas(dat,mfg_na,"Mining, Logging and Construction")
    
    dat = dat.rename(columns={'DATE':'date'})
    
    # set any strings as floats, round-up values
    dat['value'] = dat['value'].apply(lambda x: x == None if x == '.' else x)
    dat['value'] = dat['value'].apply(lambda x: float(x) if type(x) == str else x)
    dat['value'] = dat['value'].apply(lambda x: round(x,2) if type(x) == float else None)
    
    # sort by date
    dat = dat.sort_values(by='date')
    
    dat.to_json("data/jobs-by-state-"+ trans[-3:] + "-" + str(now.year) + "-" + str(now.month) + ".json", orient="records")
    return dat
    
def rollit(df):
    """ extracting three month medians """  
    import pandas as pd 
    import numpy as np
    import datetime

    now = datetime.datetime.now()    
    
    # establishing dates available in data
    dates = df.date.unique()
    length_of_time = len(dates)
    most_recent_month = dates[length_of_time-1:]
    
    # limit to three-month median
    months_in_ns = 2629800000000000
    avail_months = length_of_time -3
    earliest_month = most_recent_month - (months_in_ns * avail_months)

    # ranking the dataframe by category, state and date
    df_ranked = df.sort_values(['category','code','date'])
    
    # rolling median over three months
    df_ranked['three-month-median'] = pd.rolling_apply(df_ranked['value'], 3, np.median)
    
    # remove months where three-month median could not be applied
    df_ranked = df_ranked[df_ranked.date>earliest_month[0]]
    
    # drop the 'value' column and rename the three-month-median column 'value' for highcharts
    df_ranked = df_ranked.drop('value', 1)
    df_ranked.rename(columns={'three-month-median':'value'}, inplace=True)
    
    df_ranked.to_json("data/jobs-by-state-three-month-median-" + str(now.year) + "-" + str(now.month) + ".json", orient="records")
    return df_ranked
