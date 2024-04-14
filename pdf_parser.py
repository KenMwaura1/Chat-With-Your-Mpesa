#Function for parsing the PDF File
#importing the necessary dependencies
import pandas as pd
import PyPDF2
import tabula
import datetime


#Function for decrypting the PDF
def pdf_decrypt(pdf_password,pdf_file):
    # Create a PDF object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Check if the PDF is encrypted
    if pdf_reader.is_encrypted:
        # Attempt to decrypt the PDF with the password
        if pdf_reader.decrypt(pdf_password):
            print("PDF successfully decrypted.")
        else:
            print("Failed to decrypt the PDF. Please check you've uploaded your statement and entered the correct password.")
            exit(1)

#Function for parsing the pdf
def pdf_parser(pdf_password,pdf_file):
    """
    inputs: [pdf_password and pdf_path provided from the Streamlit UI]
    outputs: The function returns the cleaned pandas dataframe containing the Mpesa Transactions
    
    """
    #Extracting the tables from the pdf file
    tables = tabula.read_pdf(pdf_file, password=pdf_password, pages="all")
    #Slicing the list to remove the extracted footer section: After every 2 from tables[2]: using Slicing Method
    new_table = tables[2::2]
    #concatenating all the tables in the list into one dataframe
    mpesa_df = pd.concat(new_table,axis=0,ignore_index = True)
    #Filtering for only the completed transactions
    mpesa_df = mpesa_df[mpesa_df['Transaction Status'] =='Completed']

    #Data Cleaning/Wrangling
    #Deleting the unmaed column
    mpesa_df.drop(['Unnamed: 0'],axis=1,inplace=True)
    #removing the - from the withdrawn column
    mpesa_df['Withdrawn'] = mpesa_df['Withdrawn'].str.replace("-","")
    #convrting the values to float by replacing the commas
    mpesa_df['Balance'] = mpesa_df['Balance'].str.replace(",","").astype(float)
    mpesa_df['Withdrawn'] = mpesa_df['Withdrawn'].str.replace(",","").astype(float)
    mpesa_df['Paid In'] = mpesa_df['Paid In'].str.replace(",","").astype(float)
    #converting the date column to datatime
    mpesa_df['Completion Time'] = pd.to_datetime(mpesa_df['Completion Time'])

    #Filling null values with 0
    mpesa_df['Balance'].fillna(0,inplace=True)
    mpesa_df['Withdrawn'].fillna(0,inplace=True)
    mpesa_df['Paid In'].fillna(0,inplace=True)
    #Filling the null details descripotion with:
    mpesa_df['Details'].fillna("Missing Transaction Details",inplace= True)

    #Some Feature Engineering
    #crtatinmg day of week
    mpesa_df['DayOfMonth'] = mpesa_df['Completion Time'].dt.day
    mpesa_df['DayOfWeek'] = mpesa_df['Completion Time'].dt.dayofweek

    # Define a dictionary or list to map numerical values to day names
    day_names = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }

    mpesa_df['DayOfWeekName'] = mpesa_df['DayOfWeek'].map(day_names)
    #Adding Date Column
    mpesa_df['Date'] = mpesa_df['Completion Time'].dt.date
    #Adding the Time column to know when the time the transaction was made?
    mpesa_df['Time'] = mpesa_df['Completion Time'].dt.time

    #Transaction Type Categorization
    #splitting Details column
    mpesa_df[['Transaction_Type','Account']] = mpesa_df['Details'].str.split('-', n=1, expand=True)

    #can categorise the rows based on the details column to identify transaction Types
    categories = ['Customer Transfer to','Pay Bill Online','Pay Bill to',
                'Customer Transfer of Funds\rCharge','Pay Bill Charge',
                'Merchant Payment Online','Customer Payment to Small',
                'M-Shwari Withdraw','Business Payment from',
                'Airtime Purchase','Funds received from',
                'Merchant Payment','Customer Withdrawal','Withdrawal Charge',
                'Pay Merchant Charge','M-Shwari Deposit','M-Shwari Loan',
                'Deposit of Funds at Agent','OD Loan Repayment to',
                'OverDraft of Credit Party',"Customer Transfer Fuliza MPesa"]

    mpesa_df['Category'] = 'Other'

    #Loop through the phrases and categorize the rows
    for category in categories:
        mpesa_df.loc[mpesa_df['Details'].str.contains(category, case=False), 'Category'] = category

    #Mapping the categories(raw categories) to cleaned version that is easier to understand
    mapped_categories = {
                'Customer Transfer to':'Send Money',
                'Customer Transfer Fuliza MPesa':'Send Money',
                'Pay Bill Online':'Pay Bill',
                'Pay Bill to':'Pay Bill',
                'Customer Transfer of Funds\rCharge':'Mpesa Charges',
                'Pay Bill Charge':'Mpesa Charges',
                'Merchant Payment Online':'Till No',
                'Customer Payment to Small':'Pochi',
                'M-Shwari Withdraw':'Mshwari Withdraw',
                'Business Payment from':'Bank Transfer',
                'Airtime Purchase':'Airtime Purchase',
                'Funds received from':'Receive Money',
                'Merchant Payment':'Till No',
                'Customer Withdrawal':'Cash Withdrawal',
                'Withdrawal Charge':'Mpesa Charges',
                'Pay Merchant Charge':'Mpesa Charges',
                'M-Shwari Deposit':'Mshwari Deposit',
                'M-Shwari Loan':'M-Shwari Loan',
                'Deposit of Funds at Agent':'Customer Deposit',
                'OD Loan Repayment to':'Fuliza Loan Repayment',
                'OverDraft of Credit Party':'Fuliza Loan',
                'Other':'Other'}

    mpesa_df['Transaction_Type'] = mpesa_df['Category'].map(mapped_categories)

    #cleaning the name column by removing digits & * symbol
    mpesa_df['Account'] = mpesa_df['Account'].str.replace(r'[\d*]', '')
    #Filling null names with the transaction type
    mpesa_df['Account'].fillna(mpesa_df['Transaction_Type'],inplace= True)

    #Removing the line separator '\r which messes the csv file
    mpesa_df['Details'] = mpesa_df['Details'].str.replace("\r"," ")
    mpesa_df['Account'] = mpesa_df['Account'].str.replace("\r"," ")

    #Getting the mpesa table with only the relevant details
    mpesa_df_final= mpesa_df[['Receipt No.','Account','Transaction_Type' ,
       'Paid In', 'Withdrawn', 'Balance',
       'DayOfWeekName', 'Completion Time']]
    #rename columns
    mpesa_df_final.rename(columns={'Paid In': 'Money_In', 'Withdrawn': 'Money_Out'}, inplace=True)
    
    #Returning the dataframe
    return mpesa_df_final




























