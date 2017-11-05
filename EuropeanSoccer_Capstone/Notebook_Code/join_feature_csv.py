import pandas as pd

feature_1_df = pd.read_csv('Data_Structures/num_player_stats.csv')
feature_2_df = pd.read_csv('Data_Structures/ALL_MATCH_FEATURES.csv')


JOIN_COLUMNS = ['match_api_id']

all_feature_df = pd.merge(feature_1_df, feature_2_df,  how='left',
                  left_on=JOIN_COLUMNS, right_on=JOIN_COLUMNS, suffixes=('', '_y'))
all_feature_df = all_feature_df[all_feature_df.columns.drop(list(all_feature_df.filter(regex='_y')))]

all_feature_df.to_csv('Data_Structures/ALL_MATCH_FEATURES.csv')