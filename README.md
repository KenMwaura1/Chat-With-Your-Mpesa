# Chat With Your Mpesa Statements

![Home_Page](https://github.com/DennisChangach/Chat-With-Your-Mpesa-Statements/assets/41690660/269fcde4-9090-450d-9ee8-d3d0d4f385e0)

Ever wanted to analyze your Mpesa spending using the power of Large Language Models (LLMs) without sharing your sensitive data?

This project encompasses the extraction and cleaning of transactions from Mpesa PDF statements to the development of APIs for integration with the Streamlit Front End.

The project is structured around three main components:

- Data Extraction & Cleaning: This phase involves the extraction of transactions from Mpesa PDF statements and the subsequent cleaning and wrangling of the data to prepare it for utilization by the Large Language Model (LLM) application.
- Python Code Generation with LLMs: As sensitive data is not shared with the LLMs, the development of the API is crucial. This component focuses on constructing an API capable of accepting user queries and converting them into syntactically correct Python statements.
- Streamlit UI: This front end will seamlessly interact with the LLM application APIs, providing users with an engaging platform to analyze their Mpesa transactions.

## Data Extraction & Cleaning

The data extraction and cleaning process is crucial for preparing the Mpesa transactions for analysis by the Large Language Models (LLMs). The following steps are involved in this process:

- Extraction of transactions from Mpesa PDF statements
- Cleaning and wrangling of the data
- Preparation of the data for utilization by the LLM application
- The data extraction and cleaning process is essential for ensuring that the Mpesa transactions are accurately represented and can be effectively analyzed by the LLM application.
- Python Code Generation with LLMs
- The Python code generation component focuses on constructing an API capable of accepting user queries and converting them into syntactically correct Python statements. This process involves the following steps:
- Development of the API for interacting with the LLMs
- Conversion of user queries into Python code
- Execution of the Python code to analyze the Mpesa transactions
- The Python code generation component is essential for enabling users to interact with the LLM application and analyze their Mpesa transactions without sharing sensitive data.
- Streamlit UI
- The Streamlit UI provides users with an engaging platform to interact with the LLM application and analyze their Mpesa transactions. The following features are included in the Streamlit UI:
- User-friendly interface for inputting queries
- Visualization of the Mpesa transactions
- Integration with the LLM application APIs
- The Streamlit UI is essential for providing users with an intuitive platform to analyze their Mpesa transactions and gain insights into their spending habits.
- Conclusion
- The Chat With Your Mpesa Statements project encompasses the extraction and cleaning of transactions from Mpesa PDF statements to the development of APIs for integration with the Streamlit Front End. This project aims to provide users with an engaging platform to analyze their Mpesa transactions using the power of Large Language Models (LLMs) without sharing sensitive data.

## Getting Your Mpesa Statements

### Using USSD

To get your Mpesa statements, follow the steps below:

1. Dial *234# on your Safaricom line.
2. Select "My M-PESA Information".
3. Select "M-PESA Statement".
4. Select "Full Statement".
5. Select "PDF".
6. Enter the start date for the statement.
7. Enter the end date for the statement.
8. Enter the email address where you would like to receive the statement.
9. You will receive an email with the Mpesa statement in PDF format.
10. Download the PDF statement and save it to your local machine.
11. You'll also receive a code to open the PDF statement. Save this code as you'll need it to extract the transactions.
12. You can now upload the PDF statement to the Chat With Your Mpesa Statements platform to analyze your transactions.

### Use the MySafaricom App

1. Open the MySafaricom App on your phone.
2. Click on M-PESA.
3. Click on "Statements".
4. Click on "Full Statement".
5. Select the period for the statement.
6. Enter the email address where you would like to receive the statement.
7. You will receive an email with the Mpesa statement in PDF format.
8. Download the PDF statement and save it to your local machine.
9. You'll also receive a code to open the PDF statement. Save this code as you'll need it to extract the transactions.
10. You can now upload the PDF statement to the Chat With Your Mpesa Statements platform to analyze your transactions.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required dependencies.

```bash
pip install -r requirements.txt
```

## Usage

To run the Streamlit UI, execute the following command:

```bash
streamlit run streamlit_app.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

