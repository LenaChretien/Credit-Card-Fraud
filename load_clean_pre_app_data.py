import numpy as np
import pandas as pd
from scipy import stats


pre_app = pd.read_csv('credit_previous_application.csv')
pre_app = pre_app.drop(['NAME_YIELD_GROUP', 'PRODUCT_COMBINATION',
       'DAYS_FIRST_DRAWING', 'DAYS_FIRST_DUE', 'DAYS_LAST_DUE_1ST_VERSION',
       'DAYS_LAST_DUE', 'DAYS_TERMINATION', 'NFLAG_INSURED_ON_APPROVAL','SELLERPLACE_AREA','NAME_TYPE_SUITE'],axis = 1)


pre_app = pre_app.drop(['AMT_DOWN_PAYMENT','RATE_DOWN_PAYMENT',
                        'RATE_INTEREST_PRIVILEGED','RATE_INTEREST_PRIVILEGED'],axis = 1)


filter_df = pre_app[['AMT_ANNUITY']]
z = np.abs(stats.zscore(filter_df))
outliers_annuity = np.where(z > 2)


filter_df = pre_app[['AMT_APPLICATION']]
z = np.abs(stats.zscore(filter_df))
outliers_app = np.where(z > 2)


filter_df = pre_app[['AMT_CREDIT']]
z = np.abs(stats.zscore(filter_df))
outliers_credit = np.where(z > 2)


filter_df = pre_app[['AMT_GOODS_PRICE']]
z = np.abs(stats.zscore(filter_df))
outliers_goods = np.where(z > 2)

comb_outliers = np.unique(np.concatenate((outliers_annuity[0], outliers_app[0],outliers_credit[0],\
                                          outliers_goods[0]), axis =0),0)

pre_app_filter = pre_app.drop(pre_app.index[comb_outliers],axis = 0)




bins = [0,35000,55000,100000,350000,1000000000]
slot = ['Low income','lower-middle class','middle class','upper-middle class','upper class']

pre_app_filter['application_range'] = pd.cut(pre_app_filter['AMT_APPLICATION'],bins,labels = slot)

pre_app_filter['credit_range']=pd.cut(pre_app_filter['AMT_CREDIT'],bins,labels=slot)
pre_app_filter['goods_range'] = pd.cut(pre_app_filter['AMT_GOODS_PRICE'],bins,labels = slot)




col ={'SK_ID_PREV':'id_pre', 'SK_ID_CURR':'id_curr', 'NAME_CONTRACT_TYPE':'pre_credit_type',\
      'AMT_ANNUITY': 'pre_annuity', \
      'WEEKDAY_APPR_PROCESS_START':'pre_weekday', 'HOUR_APPR_PROCESS_START':'pre_hour',\
      'FLAG_LAST_APPL_PER_CONTRACT':'last_per_contract', 'NFLAG_LAST_APPL_IN_DAY':'last_per_day',\
      'RATE_INTEREST_PRIMARY':'interest', 'NAME_CASH_LOAN_PURPOSE':'cash_purpose',\
      'NAME_CONTRACT_STATUS':'status', 'DAYS_DECISION':'time_decision', 'NAME_PAYMENT_TYPE':'payment_name',\
      'CODE_REJECT_REASON':'reject_reason', 'NAME_CLIENT_TYPE':'client',\
      'NAME_GOODS_CATEGORY':'goods_cat','NAME_PORTFOLIO':'portfolio',\
      'NAME_PRODUCT_TYPE':'product_type', 'CHANNEL_TYPE':'channel_type',\
      'NAME_SELLER_INDUSTRY':'seller', 'CNT_PAYMENT':'cnt_payment',\
      'application_range':'pre_app_range','credit_range':'pre_credit_range',\
      'goods_range':'pre_goods_range'}



pre_app_filter = pre_app_filter.rename(columns = col)





pre_app_filter.to_csv('pre_app_clean.csv')
