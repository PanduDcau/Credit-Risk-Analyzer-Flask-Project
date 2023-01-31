#!/usr/bin/env python
# coding: utf-8

# # RETRAINING SCRIPT

# NOTE: This training code must be run using exactly the same environment in which it was created.
#
# The environment can be created using `pf_riskscoring.yml` file which was created during the set up phase of the project. It can be found in the folder '01_Documents'.
#
# Copy `pf_riskscoring.xml` file to the directory and using the terminal or anaconda prompt execute:
#
# ```
# conda env create --file pf_riskscoring.yml --name project_name
# ```

import numpy as np
import pandas as pd
import pickle
from janitor import clean_names
import warnings
warnings.filterwarnings("ignore")

# Functions
def data_quality(df):
    temp = df.copy()
    # Nulls
        # Imputation by value
    temp[['employment_title','employment_length']] = temp[['employment_title','employment_length']].fillna('Unknown')
    var_impute_zero = ['p_credit_cards_exceeding_75p','n_mortages','n_derogations']
    temp[var_impute_zero] = temp[var_impute_zero].fillna(0)
        # Imputation by median
    def impute_median(feature):
        if pd.api.types.is_integer_dtype(feature):
            return(feature.fillna(int(feature.median())))
        else:
            return(feature.fillna(feature.median()))
    var_impute_median = ['revolving_utilization','dti','n_credit_lines']
    temp[var_impute_median] = temp[var_impute_median].apply(impute_median)
    # Outliers
        # Groupping atypical categories
    temp['home_ownership'] = temp.home_ownership.replace(['ANY','OTHER','NONE'],'MORTGAGE')
    temp['purpose'] = temp.purpose.replace(['wedding','renewable_energy','educational'],'other')
        # Ad hoc winsorisation
    temp[['revolving_utilization','dti']] = temp[['revolving_utilization','dti']].clip(0,100)
    # Discretisation
    temp['p_credit_cards_exceeding_75p_disc'] = pd.cut(temp['p_credit_cards_exceeding_75p'],
                                                     [-float("inf"), 20, 80, float("inf")],
                                                     labels = ['00_Under_20p','01_20p_80p','02_Over_80p'])
    temp.drop(columns='p_credit_cards_exceeding_75p',inplace=True)
    return(temp)

def create_target_pd(df):
    temp = df.copy()
    # Creating target
    temp['target_pd'] = np.where(temp.status.isin(['Default',
                                                   'Charged Off',
                                                   'Does not meet the credit policy. Status:Charged Off']),1,0)
    # Deleting features
    temp.drop(columns=['status','amortised_amount','recovered_amount', 'installment', 'interest_rate'],inplace=True)
    # Features and target
    temp_x = temp.iloc[:,:-1]
    temp_y = temp.iloc[:,-1]
    return(temp_x,temp_y)

def create_target_ead(df):
    temp = df.copy()
    # Creating target
    temp['target_ead'] = (temp.loan_amount - temp.amortised_amount)/temp.loan_amount
    temp.target_ead.clip(0,1,inplace=True)
    # Deleting features
    temp.drop(columns=['status','amortised_amount','recovered_amount'],inplace=True)
    # Features and target
    temp_x = temp.iloc[:,:-1]
    temp_y = temp.iloc[:,-1]
    return(temp_x,temp_y)

def create_target_lgd(df):
    temp = df.copy()
    # Creating target
    temp['target_lgd'] = 1 - temp.recovered_amount/(temp.loan_amount - temp.amortised_amount)
    temp.target_lgd.fillna(0,inplace=True)
    temp.target_lgd.clip(0,1,inplace=True)
    # Deleting features
    temp.drop(columns=['status','amortised_amount','recovered_amount'],inplace=True)
    # Features and target
    temp_x = temp.iloc[:,:-1]
    temp_y = temp.iloc[:,-1]
    return(temp_x,temp_y)


# Data importation
project_path = '../..'
data_file_name = 'Loans.csv'
full_path = project_path + '/02_Data/01_Originals/' + data_file_name
df = pd.read_csv(full_path,sep=',')


# Final features
final_features = ['term','home_ownership','purpose','n_derogations','employment_length','scoring','annual_income','dti',
                  'installment','interest_rate','loan_amount','n_credit_lines','n_mortages','revolving_utilization',
                  'employment_title','income_verification','p_credit_cards_exceeding_75p','status','amortised_amount',
                  'recovered_amount']


# Data wrangling
df = clean_names(df).set_index('client_id')
df.columns = df.columns.str.replace('%','p').str.replace('nº','n')
df.drop_duplicates(inplace = True)
df = df[~df.index.isin(df.loc[df.annual_income>350000].index.values)]
df = df[final_features]


# Data quality + X,y creation
x_pd, y_pd = create_target_pd(data_quality(df))
x_ead, y_ead = create_target_ead(data_quality(df))
x_lgd, y_lgd = create_target_lgd(data_quality(df))


# Loading training pipes
name_pipe_training_pd = 'pipe_training_pd.pickle'
name_pipe_training_ead = 'pipe_training_ead.pickle'
name_pipe_training_lgd = 'pipe_training_lgd.pickle'
path_pipe_training_pd = project_path + '/04_Models/' + name_pipe_training_pd
path_pipe_training_ead = project_path + '/04_Models/' + name_pipe_training_ead
path_pipe_training_lgd = project_path + '/04_Models/' + name_pipe_training_lgd

with open(path_pipe_training_pd, mode='rb') as file:
   pipe_training_pd = pickle.load(file)

with open(path_pipe_training_ead, mode='rb') as file:
   pipe_training_ead = pickle.load(file)

with open(path_pipe_training_lgd, mode='rb') as file:
   pipe_training_lgd = pickle.load(file)


# Retraining
pipe_execution_pd = pipe_training_pd.fit(x_pd,y_pd)
pipe_execution_ead = pipe_training_ead.fit(x_ead,y_ead)
pipe_execution_lgd = pipe_training_lgd.fit(x_lgd,y_lgd)


# Saving retrained execution pipes
name_pipe_execution_pd = 'pipe_execution_pd.pickle'
name_pipe_execution_ead = 'pipe_execution_ead.pickle'
name_pipe_execution_lgd = 'pipe_execution_lgd.pickle'
path_pipe_ejecucion_pd = project_path + '/04_Models/' + name_pipe_execution_pd
path_pipe_ejecucion_ead = project_path + '/04_Models/' + name_pipe_execution_ead
path_pipe_ejecucion_lgd = project_path + '/04_Models/' + name_pipe_execution_lgd

with open(path_pipe_ejecucion_pd, mode='wb') as file:
   pickle.dump(pipe_execution_pd, file)

with open(path_pipe_ejecucion_ead, mode='wb') as file:
   pickle.dump(pipe_execution_ead, file)

with open(path_pipe_ejecucion_lgd, mode='wb') as file:
   pickle.dump(pipe_execution_lgd, file)
