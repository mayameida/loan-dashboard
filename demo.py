import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Demo Dashboard", #nama page pada tab browser
    page_icon="🎶",
    layout="wide"

)

st.title("Financial Insight Dashboard: Loan Performance & Trends")
st.markdown("---") #menambahkan garis

st.sidebar.header("Dashboard Filters and Features")

st.sidebar.markdown(
'''
- **Overview**: Provides a summary of key loan metrics.
- **Time-Based Analysis**: Shows trends over time and loan amounts.
- **Loan Performance**: Analyzes loan conditions and distributions.
- **Financial Analysis**: Examines loan amounts and distributions based on conditions.
'''
)

loan = pd.read_pickle('data_input/loan_clean')
loan['purpose'] =loan['purpose'].str.replace("_","")

with st.container(border=True):
    col1,col2 = st.columns(2) #mendefinisikan nama kolom

    with col1 : #isi dari kolom pertama
        st.metric('Total Loans',f"{loan['id'].count():,.0f}",help="Total number of loans")
        st.metric('Total Loan Amount',f"${loan['loan_amount'].sum():,.0f}")

    with col2: #isi dari kolom kedua
        st.metric('Average Interest Rate',f"{loan['interest_rate'].mean():,.2f}%")
        st.metric('Average Loan Amount',f"${loan['loan_amount'].mean():,.0f}")

with st.container(border=True):
    tab1, tab2, tab3 = st.tabs(['Loans Issued Over Time','Loan Amount Over Time','Issue Date Analysis'],)

    with tab1:
        loan_date_count = loan.groupby('issue_date')['loan_amount'].count()

        line_count = px.line(loan_date_count,
            markers=True,
            title='Number of Loans Over Time',
            labels={
            'value':'Number of Loans',
            'issue_date':'Issue Date'
        },
        template='seaborn'
        ).update_layout(showlegend=False)

        st.plotly_chart(line_count)

    with tab2:
        loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum()

        line_sum= px.line(loan_date_sum,
            markers=True,
            title='Total Loans Over Time',
            labels={
                'value':'Number of Loans',
                'issue_date':'Issue Date'
            },
        template='seaborn'
        ).update_layout(showlegend=False)
        
        st.plotly_chart(line_sum)

    with tab3:
        loan_day_count = loan.groupby('issue_weekday')['loan_amount'].count()

        issue_date = px.bar(
            loan_day_count,
            category_orders= {
                'issue_weekday':['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
                },
            title='Distribution of Loans by Day of the Week',
            labels={
                'value':'Number of Loans',
                'issue_weekday':'Day of the Week'
            },
            template='seaborn'
            ).update_layout(showlegend=False)
        st.plotly_chart(issue_date)

with st.expander("Click Here to Expand Visualization"):
    col3,col4 = st.columns(2)

    with col3:
        pie = px.pie(
            loan,
            names='loan_condition',
            hole=0.4,
            title = 'Distribution of Loans by Condition',
            template = 'seaborn'
            ).update_traces(textinfo='percent + value')
        st.plotly_chart(pie)

    with col4:
        grade = loan['grade'].value_counts().sort_index()
        bar_grade=px.bar(
            grade,
            category_orders= {
                'grade':['A','B','C','D','E','F','G']
                },
            title='Distribution of Grade of Loans',
            labels={
                'value':'Number of Loans',
                'grade':'Grade'
            },
            template='seaborn'
            
            )
        st.plotly_chart(bar_grade)


condition = st.selectbox("Select Loan Condition",["Good Loan","Bad Loan"])
loan_condition = loan[loan['loan_condition'] == condition]

with st.container(border=True):
    tab4, tab5 = st.tabs(['Loan Amount Distribution','Loan Amount Distribution by Purpose'],)
    with tab4:
        loan_dist = px.histogram(
        loan_condition,
        x='loan_amount',
        nbins=20,
        color='term',
        color_discrete_sequence=['darkslateblue', 'tomato'],
        template='seaborn',
        labels={
            'loan_amount':'Loan Amount',
            'term':'Loan Term'
        }
        ).update_layout(showlegend=False)
        st.plotly_chart(loan_dist)

    with tab5:
        loan_purpose = px.box(
        loan_condition,
        x = 'purpose',
        y = 'loan_amount',
        color = 'term',
        labels={
            'loan_amount' : 'Loan Amount',
            'loan_condition' : 'Loan Condition',
            'purpose' : 'Loan Purpose'
        }
        ).update_layout(showlegend=False)
        st.plotly_chart(loan_purpose)


#st.header("Ini adalah Header")
#st.header("Header Kedua")

#st.subheader("Hari Biasa")