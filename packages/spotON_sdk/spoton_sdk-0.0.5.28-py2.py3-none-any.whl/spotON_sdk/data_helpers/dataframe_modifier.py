import pandas as pd

def preprocess(df):
    df.index =  pd.to_datetime(df.index, utc=False)
    df = df.rename_axis('DateTime')
    df = df.rename(columns={"value":"Price"})
    df['Week'] = df.index.isocalendar().week
    df['Day'] = df.index.day
    df["Hour"] = df.index.hour

    # Calculate the daily average price and store it in a new DataFrame
    daily_avg = df.resample('D')['Price'].mean()

    # Merge the two DataFrames using the DateTime index with a left join
    merged_df = pd.merge(df, daily_avg, left_index=True, right_index=True, how='left', suffixes=('', '_daily_AVG'))

    # Forward fill the missing values in the 'EXXA Price_daily' column
    merged_df['Price_daily_AVG'].fillna(method='ffill', inplace=True)
    return merged_df

def add_priceRating(df):
    df['rating'] = df['Price'] - df['Price_daily_AVG']
    df['rating_rank'] = df.groupby(df.index.date)['rating'].rank(ascending=True)-1
    return df

def add_priceRatings(df):
    df['savings'] = df['Price'] - df['Price_daily_AVG']
    df['rating_rank'] = df.groupby(df.index.date)['savings'].rank(ascending=True)-1
    return df

def add_timeslot_savings(df):
    df['savings'] = df['Price'] - df['Price_daily_AVG']
    for timeslot_length in range(1,24):
        df[f"timeslot_{timeslot_length}H"] = df["savings"].rolling(timeslot_length).mean().shift(-timeslot_length+1)
    return df


def reduce_Filesize(df:pd.DataFrame):
    df["Price"] = df["Price"].astype('float16')
    df["Week"] = df["Week"].astype("int8")
    df["Day"] = df["Day"].astype("int8")
    df["Hour"] = df["Hour"].astype("int8")
    df["Price_daily_AVG"] = df["Price_daily_AVG"].astype('float16')
    df["savings"] = df["savings"].astype('float16')
    for timeslot_length in range(1,24):
        df[f"timeslot_{timeslot_length}H"] = df[f"timeslot_{timeslot_length}H"].astype('float16')
    return df