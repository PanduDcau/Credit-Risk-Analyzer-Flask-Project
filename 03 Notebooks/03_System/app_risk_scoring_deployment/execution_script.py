#!/usr/bin/env python
# coding: utf-8

# # EXECUTION SCRIPT

# NOTE: This training code must be run using exactly the same environment in which it was created.
#
# The environment can be created using `pf_riskcoring.yml` file which was created during the set up phase of the project. It can be found in the folder '01_Documents'.
#
# Copy `pf_riskcoring.yml` file to the directory and using the terminal or anaconda prompt execute:
#
# ```
# conda env create --file pf_riskcoring.yml --name project_name
# ```

import numpy as np
import pandas as pd
import pickle
from janitor import clean_names

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

def create_x_pd(df):
    temp = df.copy()
    # Deleting features
    temp.drop(columns=['installment', 'interest_rate'],inplace=True)
    return(temp)


def run_models(df):
    # Data quality + X,y creation
    x_pd = create_x_pd(data_quality(df))
    x_ead_lgd = data_quality(df)

    # Loading execution pipes
    with open('03_Notebooks/03_System/app_risk_scoring_deployment/pipe_execution_pd.pickle', mode='rb') as file:
       pipe_execution_pd = pickle.load(file)

    with open('03_Notebooks/03_System/app_risk_scoring_deployment/pipe_execution_ead.pickle', mode='rb') as file:
       pipe_execution_ead = pickle.load(file)

    with open('03_Notebooks/03_System/app_risk_scoring_deployment/pipe_execution_lgd.pickle', mode='rb') as file:
       pipe_execution_lgd = pickle.load(file)

    # Execution
    pred_pd = pipe_execution_pd.predict_proba(x_pd)[:,1]
    pred_ead = np.clip(pipe_execution_ead.predict(x_ead_lgd),0,1)
    pred_lgd = np.clip(pipe_execution_lgd.predict(x_ead_lgd),0,1)

    # Results - Expected Loss (EL)
    EL = pd.DataFrame({'principal':x_pd.loan_amount,
                       'probability_of_default':pred_pd,
                       'exposure_at_default':pred_ead,
                       'loss_given_default':pred_lgd})

    EL['expected_loss'] = round(EL.probability_of_default * EL.principal * EL.exposure_at_default * EL.loss_given_default,2)

    return(EL)
