# Credit Risk Scoring for an Online Lending Company

[![Image 1](/01_Documents/00_Images/webapp2.png)](https://03-notebooks03-systemapp-risk-scoring-deploymentapp-ri-cv1jfo.streamlitapp.com/)

- [Introduction](#introduction)
- [Objectives](#objectives)
- [Project results](#project-results)
    - [Predictive expected financial loss model + web application](#expected-loss-model)
    - [Business Insights](#business-insights)
- [Project structure](#project-structure)
- [Instructions](#instructions)
- [License](#licensing)

## Introduction <a name="introduction"></a>
The client is an online platform which specialises in lending various types of loans to urban customers. Borrowers can easily access lower interest rate loans through a fast online interface.

When the company receives a loan application, the company has to make a decision for loan approval based on the applicant’s profile. Like most other lending companies, lending loans to ‘risky’ applicants is the largest source of financial loss. The company aims to identify such ‘risky’ applicants and their associated loan’s expected loss in order to utilise this knowledge for managing its economic capital, portfolio and risk assessment.

## Objectives <a name="objectives"></a>
Creating an advanced analytical asset based on machine learning predictive models to estimate the expected financial loss of each new customer-loan binomial.

## Project results  <a name="project-results"></a>
### Expected financial loss model and web application <a name="expected-loss-model"></a>
In order to estimate the expected financial loss (EL) associated to a certain loan application, three risk models have been developed:
1. **Probability of default model (PD):** The purpose of this model is to predict the probability that a given borrower will default.
2. **Exposure at default model (EAD):** The objective of this model is to predict the percentage of the loan that a given borrower has not yet repaid when a default occurs.
3. **Loss given default model (LGD):** The objective of this model is to predict the percentage of the principal that will not be possible to recover from a loan that has been defaulted on.

Once the probability of default, exposure at default and loss given default models have been developed, the expected loss (EL) for each new loan application is obtained by simply combining the predictions of these models and the principal amount of the loan as follows:

> EL($) = PD(%) · Principal($) · EAD(%) · LGD(%)

<img src="/01_Documents/00_Images/3models.png" width="480" height="300" alt="centered image">

Finally, in order to get the most value out of the developed machine learning model, a prototype web application has been designed so employees can start using them to make practical decisions. This web app collects, on the one hand, the internal data that the company has for each client and on the other hand, the information provided by the borrower itself through a loan application.

[**Launch Credit Risk Analyzer Web App!**](https://03-notebooks03-systemapp-risk-scoring-deploymentapp-ri-cv1jfo.streamlitapp.com/)

[![Image 2](/01_Documents/00_Images/webapp1.png)](https://03-notebooks03-systemapp-risk-scoring-deploymentapp-ri-cv1jfo.streamlitapp.com/)

### Business Insights derived from exploratory data analysis <a name="business-insights"></a>
#### Borrowers:
- Borrowers with poorer credit scores tend to borrow larger amounts and have lower annual incomes than clients with higher credit scores, thus paying higher monthly installments and higher interest rates.
- One third of all customers have been employed for more than 10 years. The job title of most clients is unknown. Of the clients who do provide this information, the top three most frequent jobs are ‘Teacher’, ‘Manager’ and ‘Owner’.
- The score feature appears to be predictive of loan status: the percentage of loans charged off increases as the borrower’s credit score worsens while the percentage of fully paid loans increases as the borrower’s credit score increases.
- Three main groups can be clearly distinguished: those borrowers who used less than 20% of the credit available on their credit card, another group of borrowers have used between 20 and 80 percent of the available credit on their credit card, and a last group of borrower who have used more than 80% of their available credit on their credit card.
#### Loans
- In general, 60-month loans tend to have a higher percentage of late payments and charge-offs.
- The percentage of loans charged off for ‘moving’ and ‘small business’ purposes is slightly higher (16%-17%) than the average for the rest of loan purposes (around 11%).

## Project structure <a name="project-structure"></a>
- :file_folder: 01_Documents
  - Contains basic project files:
    - `Feature_dictionary.xlsx`: feature-level metadata.
    - `pf_riskscoring.yml`: project environment file.
    - `Development stage_Data Transformation Design.xlsx`: support file for designing feature transformation processes.
    - `Production stage_Processes Design`: support file for designing final production script.
  - :file_folder: 00_Images: Contains project images.
- :file_folder: 02_Data
  - :file_folder: 01_Originals
    - `Loans.csv`: Original dataset.
  - :file_folder: 02_Validation
    - `validation.csv`: Sample extracted from the original dataset at the beginning of the project in order to be used to check the correct performance of the model once it is put into production.
  - :file_folder: 03_Work
    - This folder contains the datasets resulting from each of the stages of the project (data quality, exploratory data analysis, feature transformation...).
- :file_folder: 03_Notebooks
  - :file_folder: 02_Development
    - `00_Project Design.ipynb`: Notebook compiling the initial design of the project.
    - `01_Set Up.ipynb`: Notebook used for the initial set up of the project.
    - `02_Data Quality.ipynb`: Notebook detailing and executing all data quality processes.
    - `03_EDA.ipynb`: Notebook used for the execution of the exploratory data analysis and which collects the business insights found.
    - `04_Feature Transformation.ipynb`: Notebook that details and executes the data transformation processes necessary to prepare the features for input into the models.
    - `05_Supervised Classification Modelling PD.ipynb`: Notebook for modelling the predictive probability of default model. Model selection, hyperparameterisation and evaluation of results.
    - `06_Supervised Regression Modelling EAD.ipynb`: Notebook for modelling the predictive exposure at default model. Model selection, hyperparameterisation and evaluation of results.
    - `07_Supervised Regression Modelling LGD.ipynb`: Notebook for modelling the predictive loss given default model. Model selection, hyperparameterisation and evaluation of results.
    - `08_Production Code Preparation.ipynb`: Notebook used to compile all the quality, transformation as well as the final models, execution and retraining processes, with the aim of creating the final retraining and execution pipes that condense all the aforementioned processes.
    - `09_Retraining script.ipynb`: Notebook to retrain the models with new data when necessary.
    - `10_Execution script.ipynb`: Notebook to execute the final models and obtain the results.
  - :file_folder: 03_System/app_risk_scoring_deployment
    - This folder contains the files (app script, production script, models, ...) used in the deployment of the web application [Credit Risk Analyzer](https://03-notebooks03-systemapp-risk-scoring-deploymentapp-ri-cv1jfo.streamlitapp.com/).
- :file_folder: 04_Models
  - `pipe_execution_pd.pickle`: pipe that condenses the final probability of default (PD) trained model as well as all necessary prior data transformations.
  - `pipe_execution_ead.pickle`: pipe that condenses the final exposure at default (EAD) trained model as well as all necessary prior data transformations.
  - `pipe_execution_lgd.pickle`: pipe that condenses the final loss given default (LGD) trained model as well as all necessary prior data transformations.
  - `pipe_training_pd.pickle`:  pipe that condenses the entire probability of default (PD) model training process. It can be used to retrain the model with new data when necessary.
  - `pipe_training_ead.pickle`:  pipe that condenses the entire exposure at default (EAD) model training process. It can be used to retrain the model with new data when necessary.
  - `pipe_training_lgd.pickle`:  pipe that condenses the entire loss given default (LGD) model training process. It can be used to retrain the model with new data when necessary.
- :file_folder: 05_Results
  - `execution script.py`: Python script to execute the models and obtain the results.
  - `retraining script.py`: Python script to retrain the models with new data when necessary.
  - `Credit_risk_analyzer_web_app_link.md`: Credit risk analyzer web app link.

## Instructions  <a name="instructions"></a>
The project should be run using exactly the same environment in which it was created.

- Project environment can be replicated using 'pf_riskscoring.yml' file which was created during the set up phase of the project. It can be found in the folder '01_Documents'.
- Copy 'pf_riskscoring.yml' file to the directory and using the terminal or anaconda prompt execute:
    > conda env create --file pf_riskscoring.yml --name project_name

By other hand, remember to update the `project_path` variable of the notebooks to the path where you have replicated the project.

## Licensing <a name="licensing"></a>
The data set, licensing, and other descriptive information is available at [LendingClub website](https://www.lendingclub.com/).
