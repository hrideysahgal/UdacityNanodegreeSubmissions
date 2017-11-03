import sqlite3
import zipfile

import pandas as pd

from Utils import *
from players import *


def uncompress_and_open_sqlite():
  zip = zipfile.ZipFile(INPUTFILE_DIR + INPUTZIPFILE)
  zip.extractall(path=INPUTFILE_DIR)
  conn = sqlite3.connect(INPUTFILE_DIR + DATABASENAME)
  return conn


def execute_query_print_results(conn, sql_query):
  cur = conn.cursor()
  cur.execute(sql_query)
  rows = cur.fetchall()
  for row in rows:
    print row


def desc_table(table_df, table_name):
  print SEPARATOR
  print "For table " + table_name + " there are " + str(table_df.shape[0]) + \
        " entries with " + str(table_df.shape[1]) + " features"
  print table_df.columns.tolist()
  print SEPARATOR


def home_advantage(matches_df, conn):
  # TODO: Convert to DataFrama and Plot
  country_id_to_num_matches = matches_df[['country_id', 'result_label']].copy()
  grouped_df = country_id_to_num_matches.\
    groupby(['country_id'], as_index=False).agg({'result_label':'count'}).rename(columns={'result_label': 'matches_per_country'})

  win_df = country_id_to_num_matches[country_id_to_num_matches['result_label'] == 'HOME_WIN']
  grouped_home_df = win_df. \
    groupby(['country_id'], as_index=False).agg({'result_label':'count'}).rename(columns={'result_label': 'home_wins_per_country'})
  join_df = pd.merge(grouped_df, grouped_home_df, on='country_id',
                            how='outer')
  join_df['percentage_home_win']= join_df.apply(
      lambda r: np.true_divide(r['home_wins_per_country'], r['matches_per_country']) * 100., axis=1)

  countries_df = sql_to_dataframe(conn, select_all_query_table("Country"))
  join_df_name = pd.merge(countries_df, join_df, left_on = 'id', right_on='country_id',
                          how='outer')
  return join_df_name[['name', 'percentage_home_win']]



if __name__ == '__main__':
  conn = uncompress_and_open_sqlite()
  matches_df = sql_to_dataframe(conn, select_all_query_table("Match"))
  home_advantage(matches_df=matches_df, conn=conn)
