import streamlit as st
from data_coun_grape_dynDB import country_variety_DB
from data_region_type_dynDB import region_type_DB
from preprocessing import preprocess
from decompose_autocorr import df_decompose, autocorr, adf_test
from time_xgboost import xgb
import os
import boto3
from modelarima import model_arima
from lists_streamlit import lists_for_streamlit




# local launch
access_key = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
region = os.environ.get('AWS_REGION')
file_path = 'C:/Users/user/projects/wine/parcer/all_wines_in_db_log.txt'

# streamlit launch
#access_key = st.secrets["aws"]["access_key"]
#secret_key = st.secrets["aws"]["secret_key"]
#region = st.secrets["aws"]["AWS_REGION"]
#file_path = 'https://raw.githubusercontent.com/AndreiGalavnev/gp_med_git/master/data/df_contacts_new_with_coordinates.csv'  



if __name__ == "__main__": 
    countries_list, regions_list, types_list, grapes_list = lists_for_streamlit(file_path)
    
    st.header('Wine demand forecast', divider='red')
    st.subheader('                  ...using winelover\'s reviews from Vivino.com :wine_glass:')
    st.text('')
    st.text('')
    st.text('')
    st.markdown('What types of wines do you want to get a forecast for?')
    # Выбор режима работы

    option = st.radio('Choose a wine\'s type', ('Red/White/Rose', 'Fortified/Dessert/Sparkling'))
    if option == 'Red/White/Rose':
        coun_opt = st.selectbox('Choose a country', countries_list, key='coun')
        reg_opt = st.selectbox('Choose a grape', grapes_list, key='reg')
        period = st.selectbox('Choose a period in months', [6,12,24], key='period')
        cs = st.button('Confirm selection', key='button_clicked2')
        if cs:
            data, sum_rev = country_variety_DB(coun_opt, reg_opt, access_key, secret_key)
            # for lack of data
            if (data is None) or (int(sum_rev) < 7000):
                st.write("No data found")
                exit()
            data = preprocess(data)
            if coun_opt:
                opt1 = f"{reg_opt} in {coun_opt}"
            # Создание раскрывающегося блока
            tab1, tab2, tab3 = st.tabs([f"**XGBOOST Forecast for {opt1}**", f"**ARIMA Forecast for {opt1}**", f"*Some advanced data*"])
            with tab1:
                xgb1 = xgb(data, period)
                st.pyplot(xgb1)
            with tab2:
                ar = model_arima(data, period)
                st.pyplot(ar)
            with tab3:
                st.write('Sum of parced reviews: ', sum_rev)
                # показываем adf-test, decomposition, acf, pacf
                adf, pval, usedlag, nobs, crit_vals, icbest =  adf_test(data)
                st.write('ADF test statistic:', adf)
                st.write('ADF p-value:', pval)
                st.write('ADF number of lags used:', usedlag)
                st.write('ADF number of observations:', nobs)
                st.write('ADF critical values:', crit_vals)
                st.write('ADF best information criterion:', icbest)
                dec = df_decompose(data)
                st.pyplot(dec)
                acorr = autocorr(data)
                st.pyplot(acorr)


    if option == 'Fortified/Dessert/Sparkling':
        reg_opt = st.selectbox('Choose a region\'s style', regions_list)
        type_opt = st.selectbox('Choose a type of wine', types_list)
        period = st.selectbox('Choose a period in months', [6,12,24])
        cs = st.button('Confirm selection')
        if cs:
            data, sum_rev = region_type_DB(reg_opt, type_opt, access_key, secret_key)
            if (data is None) or (int(sum_rev) < 2000):
                st.write("No data found")
                exit()
            data = preprocess(data)
            if reg_opt:
                opt1 = f"{type_opt} in {reg_opt} region"
            # Создание раскрывающегося блока
            tab1, tab2, tab3 = st.tabs([f"**XGBOOST Forecast for {opt1}**", f"**ARIMA Forecast for {opt1}**", f"*Some advanced data*"])
            with tab1:
                
                xgb1 = xgb(data, period)
                st.pyplot(xgb1)
            with tab2:
                ar = model_arima(data, period)
                st.pyplot(ar)
            with tab3:
                st.write('Sum of parced reviews: ', sum_rev)
                # показываем adf-test, decomposition, acf, pacf
                adf, pval, usedlag, nobs, crit_vals, icbest =  adf_test(data)
                st.write('ADF test statistic:', adf)
                st.write('ADF p-value:', pval)
                st.write('ADF number of lags used:', usedlag)
                st.write('ADF number of observations:', nobs)
                st.write('ADF critical values:', crit_vals)
                st.write('ADF best information criterion:', icbest)
                dec = df_decompose(data)
                st.pyplot(dec)
                acorr = autocorr(data)
                st.pyplot(acorr)