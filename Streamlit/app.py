import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

startup=pd.read_csv('startup_cleaned.csv')
startup['date']=pd.to_datetime(startup['date'])
startup['month']=startup['date'].dt.month
startup['year']=startup['date'].dt.year


def load_investor(investor):
    df=startup[startup['investors'].str.contains(investor)]
    st.title(investor)
    #recent 5 investment 
    last5_df=startup[startup['investors'].str.contains(investor)][['date','startup','vertical','city','round','amount']]
    st.dataframe(last5_df)

    col1,col2 = st.columns(2)
    with col1:
        biginvestment=df.groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('biginvestment')
        fig, ax = plt.subplots()
        ax.bar(biginvestment.index, biginvestment.values)
        st.pyplot(fig)
   

    with col2:
        biginvestment=df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('biginvestment')
        fig, ax = plt.subplots()
        ax.pie(biginvestment,labels=biginvestment.index,autopct='%1.1f%%')
        st.pyplot(fig)
   
    
    biginvestment=df.groupby('city')['amount'].sum().sort_values(ascending=False).head()
    st.subheader('biginvestment')
    fig, ax = plt.subplots()
    ax.pie(biginvestment,labels=biginvestment.index,autopct='%1.1f%%')
    st.pyplot(fig)



    biginvestment=df.groupby('round')['amount'].sum().sort_values(ascending=False).head()
    st.subheader('biginvestment')
    fig, ax = plt.subplots()
    ax.pie(biginvestment,labels=biginvestment.index,autopct='%1.1f%%')
    st.pyplot(fig)

    startup['year']=startup['date'].dt.year
    biginvestment=startup[startup['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('biginvestment')
    fig, ax = plt.subplots()
    ax.plot(biginvestment)
    st.pyplot(fig)

def loadoverall():
    st.title('overall analysis')
    total=round(startup['amount'].sum())
    maxamount=startup.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    avgamount=startup.groupby('startup')['amount'].sum().mean()
    tostart=startup.groupby('startup').count().shape[0]
    col1,col2,col3,col4=st.columns(4)
    with col1:
       st.metric(label='total',value=f'{total}cr')
    with col2:
       st.metric(label='Max',value=f'{maxamount}')
    with col3:
       st.metric(label='Max',value=f'{(avgamount)}')
    with col4:
       st.metric(label='Max',value=f'{tostart}')
    

    st.header('mom graph')
    selecto=st.selectbox('select',['count','total'])
    if selecto == 'count':
        s=startup.groupby(['year','month'])['amount'].count().reset_index()
        
        st.subheader('count')

    if selecto=='total':
        s=startup.groupby(['year','month'])['amount'].sum().reset_index()
        st.subheader('total')

    s['x-axis']=s['month'].astype('str')+'-'+s['year'].astype('str')
    fig2, ax2 = plt.subplots()
    ax2.plot(s['x-axis'],s['amount'])
    st.pyplot(fig2)
    
    



    





# st.dataframe(startup)
st.sidebar.title("Startup Funding Analysis")
option=st.sidebar.selectbox('select one',['overall','startup','investor'])
if option =='overall':
    btn0=st.sidebar.button('overall')
    loadoverall()
elif option =='startup':
    x=st.sidebar.selectbox('select startup',sorted(startup['startup'].unique()))
    btn1=st.sidebar.button('startup detailes')
    df=startup[startup['startup']==x]
   
else:
    x=st.sidebar.selectbox('select one',sorted(startup['investors'].unique()))
    btn2=st.sidebar.button('startup detailes')
    load_investor(x)