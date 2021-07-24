import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
plt.style.use('ggplot')
pd.get_option("display.max_columns",None)
pd.get_option("display.max_rows", None)
import seaborn as sns
from scipy import stats



app = pd.read_csv('credit_application_data.csv')

app = app.drop(['WALLSMATERIAL_MODE','EMERGENCYSTATE_MODE','NAME_TYPE_SUITE', 'REGION_RATING_CLIENT','REGION_RATING_CLIENT','EXT_SOURCE_1','EXT_SOURCE_2', 'EXT_SOURCE_3','APARTMENTS_AVG','BASEMENTAREA_AVG','YEARS_BEGINEXPLUATATION_AVG', 'YEARS_BUILD_AVG','COMMONAREA_AVG','ELEVATORS_AVG','ENTRANCES_AVG','FLOORSMAX_AVG', 'FLOORSMIN_AVG','LANDAREA_AVG','LIVINGAPARTMENTS_AVG','LIVINGAREA_AVG', 'NONLIVINGAPARTMENTS_AVG','NONLIVINGAREA_AVG','APARTMENTS_MODE','BASEMENTAREA_MODE', 'YEARS_BEGINEXPLUATATION_MODE','YEARS_BUILD_MODE','COMMONAREA_MODE','ELEVATORS_MODE', 'ENTRANCES_MODE','FLOORSMAX_MODE','FLOORSMIN_MODE','LANDAREA_MODE','LIVINGAPARTMENTS_MODE','LIVINGAREA_MODE','NONLIVINGAPARTMENTS_MODE','NONLIVINGAREA_MODE','APARTMENTS_MEDI','BASEMENTAREA_MEDI','YEARS_BEGINEXPLUATATION_MEDI','YEARS_BUILD_MEDI','COMMONAREA_MEDI','ELEVATORS_MEDI','ENTRANCES_MEDI','FLOORSMAX_MEDI','FLOORSMIN_MEDI','LANDAREA_MEDI','LIVINGAPARTMENTS_MEDI','LIVINGAREA_MEDI','NONLIVINGAPARTMENTS_MEDI','NONLIVINGAREA_MEDI','FONDKAPREMONT_MODE','HOUSETYPE_MODE','TOTALAREA_MODE'],axis = 1)
    
# function to get null value
def column_wise_null_percentage(df):
    output = round(df.isnull().sum()/len(df.index)*100,2)
    return output

NA_col = column_wise_null_percentage(app)
NA_col.shape

app = app.drop(['OWN_CAR_AGE','OCCUPATION_TYPE','OBS_30_CNT_SOCIAL_CIRCLE', 'DEF_30_CNT_SOCIAL_CIRCLE', 'OBS_60_CNT_SOCIAL_CIRCLE', 'DEF_60_CNT_SOCIAL_CIRCLE'],axis = 1)

app = app[app['CODE_GENDER'] != 'XNA']


age = round(app['DAYS_BIRTH'].abs()/365,2)

app.rename(columns = {'DAYS_BIRTH':'age','DAYS_EMPLOYED':'employed','DAYS_REGISTRATION':'registration','DAYS_ID_PUBLISHED':'id_pub'}, inplace = True )
app['age']= round(app['age'].abs()/365,2)
app['employed'] = round(app['employed'].abs()/365,2)
app['registration'] = round(app['registration'].abs()/365,2)
app['id_pub'] = round(app['registration'].abs()/365,2)

columns = ['CNT_CHILDREN','AMT_INCOME_TOTAL', 'AMT_CREDIT','AMT_GOODS_PRICE', 'REGION_POPULATION_RELATIVE', 'age','employed','registration', 'id_pub', 'HOUR_APPR_PROCESS_START']



filter_df = app[['AMT_INCOME_TOTAL']]
z = np.abs(stats.zscore(filter_df))
outliers_income = np.where(z > 2)


filter_df = app[['AMT_CREDIT']]
z = np.abs(stats.zscore(filter_df))
outliers_credit = np.where(z > 2)


filter_df = app[['AMT_GOODS_PRICE']]
z = np.abs(stats.zscore(filter_df))
outliers_goods = np.where(z > 2)


filter_df = app[['REGION_POPULATION_RELATIVE']]
z = np.abs(stats.zscore(filter_df))
outliers_region = np.where(z > 2)


filter_df = app[['employed']]
z = np.abs(stats.zscore(filter_df))
outliers_empl = np.where(z > 2)


comb_outliers = np.unique(np.concatenate((outliers_income[0], outliers_credit[0],outliers_goods[0], outliers_region[0], outliers_empl[0]), axis =0),0)
app_filter = app.drop(app.index[comb_outliers],axis = 0)


#bins = [0,30000,50000,70000,90000,110000,150000,200000,300000,10000000]
#slot = ['<30000', '30000-50000','50000-70000','70000-90000', '90000-110000', '110000-150000', '150000-200000', '200000-300000', '>300000']

#app_filter['AMT_CREDIT_RANGE'] = pd.cut(app_filter['AMT_CREDIT'],bins,labels = slot)
#app_filter['AMT_INCOME_RANGE']=pd.cut(app_filter['AMT_INCOME_TOTAL'],bins,labels=slot)
#app_filter['AMT_GOODS_RANGE'] = pd.cut(app_filter['AMT_GOODS_PRICE'],bins,labels = slot)
bins = [0,35000,55000,100000,350000,1000000000]
slot = ['Low income','lower-middle class','middle class','upper-middle class','upper class']
app_filter['AMT_INCOME_RANGE']=pd.cut(app_filter['AMT_INCOME_TOTAL'],bins,labels=slot)



bins = [0,50000,100000,150000,200000,300000,500000,1000000,100000000000]
slot = ['<50000', '50000-100000','100000-150000','150000-200000',\
        '200000-300000', '300000-500000', '500000-1000000',\
        '>1000000']
app_filter['AMT_CREDIT_RANGE'] = pd.cut(app_filter['AMT_CREDIT'],bins,labels = slot)
app_filter['AMT_GOODS_RANGE'] = pd.cut(app_filter['AMT_GOODS_PRICE'],bins,labels = slot)



#bins = [20,25,30,35,40,45,50,55,60,65,70]
#slot = ['<25', '25-30','30-35','35-40', '40-45', '45-50', '50-55', '55-60', '60-65','>65']

#app_filter['age_range'] = pd.cut(app_filter['age'],bins,labels = slot)
#app_filter['employment_range'] = pd.cut(app_filter['employed'],bins,labels = slot)
#app_filter['id_pub_range'] = pd.cut(app_filter['id_pub'],bins,labels = slot)
bins = [0,30,45,60,100]
slot = ['<30','30-45','45-60','>60']
app_filter['age_range'] = pd.cut(app_filter['age'],bins,labels = slot)
app_filter['employment_range'] = pd.cut(app_filter['employed'],bins,labels = slot)
app_filter['id_pub_range'] = pd.cut(app_filter['id_pub'],bins,labels = slot)


col = {'SK_ID_CURR':'id_curr', 'TARGET': 'target', 'NAME_CONTRACT_TYPE': 'credit_type', 'CODE_GENDER': 'gender', 'FLAG_OWN_CAR': 'fcar', 'FLAG_OWN_REALTY': 'frealty', 'CNT_CHILDREN':'kids', 'AMT_INCOME_TOTAL':'income', 'AMT_CREDIT':'credit', 'AMT_ANNUITY':'annuity', 'AMT_GOODS_PRICE':'goods', 'NAME_INCOME_TYPE' : 'income_type', 'NAME_EDUCATION_TYPE':'education', 'NAME_FAMILY_STATUS': 'family_status', 'NAME_HOUSING_TYPE': 'housing', 'REGION_POPULATION_RELATIVE': 'pop_relative', 'DAYS_ID_PUBLISH': 'id_pub', 'FLAG_MOBIL':'fmobile', 'FLAG_EMP_PHONE':'femp_phone', 'FLAG_WORK_PHONE':'fwork_phone', 'FLAG_CONT_MOBILE':'freach_phone', 'FLAG_PHONE':'fphone', 'FLAG_EMAIL':'femail', 'CNT_FAM_MEMBERS':'fam_members', 'REGION_RATING_CLIENT_W_CITY':'region_rating', 'WEEKDAY_APPR_PROCESS_START':'weekday', 'HOUR_APPR_PROCESS_START':'hour', 'REG_REGION_NOT_LIVE_REGION':'reg_not_live', 'REG_REGION_NOT_WORK_REGION':'reg_not_work', 'LIVE_REGION_NOT_WORK_REGION':'live_not_work', 'REG_CITY_NOT_LIVE_CITY':'regvity_not_livecity', 'REG_CITY_NOT_WORK_CITY':'regcity_not_workcity', 'LIVE_CITY_NOT_WORK_CITY':'livecity_not_workcity', 'ORGANIZATION_TYPE':'worktype', 'DAYS_LAST_PHONE_CHANGE':'phone_change', 'FLAG_DOCUMENT_2':'d2', 'FLAG_DOCUMENT_3':'d3', 'FLAG_DOCUMENT_4':'d4', 'FLAG_DOCUMENT_5':'d5', 'FLAG_DOCUMENT_6':'d6', 'FLAG_DOCUMENT_7':'d7', 'FLAG_DOCUMENT_8':'d8', 'FLAG_DOCUMENT_9':'d9','FLAG_DOCUMENT_10':'d10', 'FLAG_DOCUMENT_11':'d11', 'FLAG_DOCUMENT_12':'d12', 'FLAG_DOCUMENT_13': 'd13', 'FLAG_DOCUMENT_14':'d14', 'FLAG_DOCUMENT_15':'d15', 'FLAG_DOCUMENT_16':'d16', 'FLAG_DOCUMENT_17':'d17', 'FLAG_DOCUMENT_18':'d18', 'FLAG_DOCUMENT_19':'d19', 'FLAG_DOCUMENT_20':'d20', 'FLAG_DOCUMENT_21':'d21', 'AMT_CREDIT_RANGE':'credit_range', 'AMT_INCOME_RANGE':'income_range', 'AMT_GOODS_RANGE':'goods_range'}

app_filter = app_filter.rename(columns = col)


men = app_filter[app_filter['gender'] == 'M']
women = app_filter[app_filter['gender'] == 'F']
target1 = app_filter[app_filter['target'] == 1]
target0 = app_filter[app_filter['target'] == 0]


app_filter.to_csv('app_clean.csv')
#men.to_csv('men_app.csv')
#women.to_csv('women_app.csv')
#target1.to_csv('target1_app.csv')
#target0.to_csv('target0_app.csv')