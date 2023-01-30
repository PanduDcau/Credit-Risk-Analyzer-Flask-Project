from execution_script import *
import streamlit as st
from streamlit_echarts import st_echarts
from PIL import Image

# LOADING IMAGES
im_sidebar = Image.open('03_Notebooks/03_System/app_risk_scoring_deployment/img_sidebar.png')
im_title = Image.open('03_Notebooks/03_System/app_risk_scoring_deployment/img_title.png')

# PAGE SET UP
st.set_page_config(
     page_title = 'Credit Risk Analyzer',
     page_icon = '03_Notebooks/03_System/app_risk_scoring_deployment/icon.png',
     layout = 'wide',
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': None,
         'Report a bug': None,
         'About': "### Credit Risk Analyzer. \n\n The purpose of this data-driven application is to automate the calculation of fees that make each new loan-customer binomial profitable by estimating the expected financial loss based on probability of default, loss given default, and exposure at default risk model predictions.\n&nbsp; \n  \n - Source code can be found [here](https://github.com/pedrocorma/credit-risk-scoring). \n - Further project details are available [here](https://pedrocorma.github.io/project/1riskscoring/)."
     })

# Page margins
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 1rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
                .css-hxt7ib{
                    padding-top: 2.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

# Sidebar width
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 430px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 300px;
        margin-left: -300px;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

# SIDEBAR
with st.sidebar:
    st.image(im_sidebar)
    st.markdown('')

    col1, col2, col3, col4, col5 = st.columns([0.5,1,0.25,1,0.5])
    with col2:
        form_button = st.button('NEW LOAN APPLICATION')
    with col4:
        calculate_button = st.button('CALCULATE RISK')

    st.markdown('---')
    st.markdown("<h1 style='text-align: center; color: #f76497;'>SERVER-SIDE PARAMETERS</h1>", unsafe_allow_html=True)


    # Server-side features - Input
    col1,col2 = st.columns(2)
    with col1:
        scoring = st.select_slider('Profile scoring:',options=['A','B','C','D','E','F','G'],value='B')
        revolving_utilization = st.slider('% Revolving utilisation:', 0, 100, value=50)
        income_verification = st.radio('Income verification status:', ['Source verified','Verified','Not verified'], 0)
    with col2:
        dti = st.slider('Debt-to-income ratio:', 0, 100, value=18)
        p_credit_cards_exceeding_75p = st.slider('% Credit cards exceeding 75%:', 0, 100, value=37)
        n_derogations = st.radio('Previous derogations:', ['Yes','No'], 1)


# MAIN
# Title image
col1,col2,col3 = st.columns([0.8,1,0.5])
with col2:
    st.image(im_title)

placeholder = st.empty()

with placeholder.container():
    # Subtitle
    st.markdown("<h3 style='text-align: left; color: #f76497;'>LOAN APPLICATION FORM</h3>", unsafe_allow_html=True)
    st.markdown(' ')

    # Lead web form features - Input
    # Loan details
    st.markdown("<h5 style='text-align: left; color: #f76497;'>Loan details</h5>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns([2,0.25,1,0.25,2])
    with col1:
        loan_amount = st.number_input('Loan amount ($):',500,50000,12500,1,
                                      help="If the client wishes to apply for a loan amount above $50000 please refer him/her to the dedicated lending team.")
    with col3:
        term = st.radio('Term (months):',['36','60'],0)
    with col5:
        purpose = st.selectbox('Purpose:',
                               ['Debt consolidation','Credit card ','Home improvement','Major purchase','Medical',
                                'Small business','Car','Vacation','Moving','House','Wedding','Renewable energy','Educational','Other'],0)
    st.markdown('---')

    # Personal details
    st.markdown("<h5 style='text-align: left; color: #f76497;'>Personal  details</h5>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        employment_title = st.text_input('Employment title:', value='Teacher', max_chars=60, type="default")
    with col2:
        employment_length = st.select_slider('Employment length:',
                                             options=['< 1 year','1 year','2 years','3 years','4 years','5 years',
                                                      '6 years','7 years','8 years','9 years','10+ years'],value='3 years')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        annual_income = st.number_input('Annual income ($):',0,350000,65000,1,
                              help="If the client's annual income exceeds $350000 please refer him/her to the dedicated lending team.")
    with col2:
        home_ownership = st.selectbox('Home ownership status:',['Mortgage', 'Rent', 'Own', 'Any', 'Other', 'None'],0)
    with col3:
        n_credit_lines = st.number_input('Nº credit lines:',0,100,5,1)
    with col4:
        n_mortages = st.number_input('Nº mortages:',0,50,1,1)

    st.markdown('')

# Fixed data for simplicity:
## interest_rate
if scoring=='A':
    interest_rate = 7.08
elif scoring=='B':
    interest_rate = 10.68
elif scoring=='C':
    interest_rate = 14.15
elif scoring=='D':
    interest_rate = 18.13
elif scoring=='E':
    interest_rate = 21.78
elif scoring=='F':
    interest_rate = 25.44
elif scoring=='G':
    interest_rate = 28.13

## installment:
installment = round(loan_amount*(1+(interest_rate/100))/int(term),2)


df_loan = pd.DataFrame({'term':term + ' months',
                        'home_ownership':home_ownership.upper(),
                        'purpose':purpose.lower().replace(' ','_'),
                        'n_derogations':np.where(n_derogations=='Yes',1,0),
                        'employment_length':employment_length,
                        'scoring':scoring,
                        'annual_income':annual_income,
                        'dti':dti,
                        'installment':installment,
                        'interest_rate':interest_rate,
                        'loan_amount':loan_amount,
                        'n_credit_lines':n_credit_lines,
                        'n_mortages':n_mortages,
                        'revolving_utilization':revolving_utilization,
                        'employment_title':employment_title[0].upper() + employment_title[1:].lower(),
                        'income_verification':income_verification,
                        'p_credit_cards_exceeding_75p':p_credit_cards_exceeding_75p,
                        'client_id':1},
                        index=[0])


# CALCULATE RISK:
if calculate_button:
    df_el = run_models(df_loan)
    placeholder.empty()
    placeholder_results = st.empty()

    PD = float(df_el.probability_of_default)
    EAD = float(df_el.exposure_at_default)
    LGD = float(df_el.loss_given_default)
    EL = float(df_el.expected_loss)

    def formatter_custom(model,opt):
        if model=='PD':
            if opt==0:
                return('PD'+'\n'+str(round(PD*100))+'%')
            elif opt==1:
                return(str(round(PD*100))+'%')
        elif model=='EAD':
            if opt==0:
                return('EAD'+'\n'+str(round(EAD*100))+'%')
            elif opt==1:
                return(str(round(EAD*100))+'%')
        elif model=='LGD':
            if opt==0:
                return('LGD'+'\n'+str(round(LGD*100))+'%')
            elif opt==1:
                return(str(round(LGD*100))+'%')
        elif model=='EL':
            if opt==0:
                return('EL'+'\n'+str(round(EL,2))+' $')
            elif opt==1:
                return('Expected loss')

    st.markdown(' ')
    st.markdown(' ')
    st.markdown(' ')
    col1,col2,col3,col4,col5 = st.columns([2.75,1,1,1,0.25])
    with col1:
        liquidfill_option = {
        "series": [{"type": "liquidFill",
                    "data": [{"name": 'PD',
                              "value": EL,
                              "itemStyle": {"color": "#262730"}}],

                    "label": {"formatter": formatter_custom('EL',0),
                              "fontSize": 40,
                              "color": '#f76497',
                              "insideColor": '#f76497',
                              "show":"true"},


                    "backgroundStyle": {"borderWidth": 5,
                                        # "borderColor": 'red',
                                        "color": '#262730'},

                    "outline": {"borderDistance": 8,
                                "itemStyle": {"color": "#262730",
                                              "borderColor": '#fff',
                                              "borderWidth": 2,
                                              "shadowBlur": 40,
                                              "shadowColor": '#f76497'}},

                    "amplitude": 5,
                    "shape": 'roundRect'}],

        "tooltip": {"show": "true",
                    "formatter": formatter_custom('EL',1)}
                    }

        st_echarts(liquidfill_option, width='100%', height='450%', key=0)
    with col2:
        liquidfill_option = {
        "series": [{"type": "liquidFill",
                    "data": [{"name": 'PD',
                              "value": PD,
                              "itemStyle": {"color": "#f76497"}}],

                    "label": {"formatter": formatter_custom('PD',0),
                              "fontSize": 40,
                              "color": '#f76497',
                              "insideColor": '#fff',
                              "show":"true"},


                    "backgroundStyle": {"borderWidth": 5,
                                        # "borderColor": 'red',
                                        "color": '#262730'},

                    "outline": {"borderDistance": 8,
                                "itemStyle": {"color": 'none',
                                              "borderColor": '#fff',
                                              "borderWidth": 2,
                                              "shadowBlur": 40,
                                              "shadowColor": '#f76497'}},

                    "amplitude": 5,
                    "shape": 'container'}],

        "tooltip": {"show": "true",
                    "formatter": formatter_custom('PD',1)}
                    }

        st_echarts(liquidfill_option, width='100%', height='450%', key=1)
    with col3:
        liquidfill_option = {
        "series": [{"type": "liquidFill",
                    "data": [{"name": 'EAD',
                              "value": EAD,
                              "itemStyle": {"color": "#f76497"}}],

                    "label": {"formatter": formatter_custom('EAD',0),
                              "fontSize": 40,
                              "color": '#f76497',
                              "insideColor": '#fff',
                              "show":"true"},


                    "backgroundStyle": {"borderWidth": 5,
                                        # "borderColor": 'red',
                                        "color": '#262730'},

                    "outline": {"borderDistance": 8,
                                "itemStyle": {"color": 'none',
                                              "borderColor": '#fff',
                                              "borderWidth": 2,
                                              "shadowBlur": 40,
                                              "shadowColor": '#f76497'}},

                    "amplitude": 5,
                    "shape": 'container'}],

        "tooltip": {"show": "true",
                    "formatter": formatter_custom('EAD',1)}
                    }

        st_echarts(liquidfill_option, width='100%', height='450%', key=2)
    with col4:
        liquidfill_option = {
        "series": [{"type": "liquidFill",
                    "data": [{"name": 'LGD',
                              "value": LGD,
                              "itemStyle": {"color": "#f76497"}}],

                    "label": {"formatter": formatter_custom('LGD',0),
                              "fontSize": 40,
                              "color": '#f76497',
                              "insideColor": '#fff',
                              "show":"true"},


                    "backgroundStyle": {"borderWidth": 5,
                                        # "borderColor": 'red',
                                        "color": '#262730'},

                    "outline": {"borderDistance": 8,
                                "itemStyle": {"color": 'none',
                                              "borderColor": '#fff',
                                              "borderWidth": 2,
                                              "shadowBlur": 40,
                                              "shadowColor": '#f76497'}},

                    "amplitude": 5,
                    "shape": 'container'}],

        "tooltip": {"show": "true",
                    "formatter": formatter_custom('LGD',1)}
                    }

        st_echarts(liquidfill_option, width='100%', height='450%', key=3)


    col1,col2,col3,col4,col5,col6 = st.columns([0.22,2,0.18,0.9,0.9,1])
    with col2:
        st.markdown('Opening commission recommended to cover expected loss')
    with col4:
        st.markdown('Probability of default')
    with col5:
        st.markdown('Exposure at default')
    with col6:
        st.markdown('Loss given default')
