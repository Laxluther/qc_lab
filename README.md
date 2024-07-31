**Project Title:** End-to-End Quality Control Dashboard for Edible Oil Production

The primary goal of this project is to develop an End-to-End Quality Control Dashboard for edible oil production, which integrates data collection, real-time processing, and comprehensive analytics to ensure consistent product quality and operational efficiency. The dashboard will serve as a centralized platform for monitoring and managing the quality control processes throughout the production lifecycle, from raw material procurement to final product dispatch. This initiative aims to enhance decision-making, streamline quality assurance workflows, and facilitate compliance with industry standards.

**Description**

In the edible oil industry, maintaining high-quality standards is critical due to strict regulatory requirements and competitive market conditions. This project aims to automate data collection, ensure accurate and real-time data processing, and provide an intuitive visual interface for monitoring quality metrics across the production lifecycle. This project is significant as it addresses the challenges of managing diverse quality control parameters, reduces the risk of product defects, and enhances compliance with industry standards.

The End-to-End Quality Control Dashboard for Edible Oil Production is an innovative project designed to enhance the quality assurance processes in the edible oil industry. This project aims to develop a comprehensive, centralized platform that integrates data collection, real-time processing, and detailed analytics to ensure consistent product quality and operational efficiency. By consolidating various quality metrics and production data, the dashboard will provide production managers with real-time insights and facilitate prompt decision-making, ultimately leading to improved product quality and customer satisfaction.

The Quality Control Dashboard for Edible Oil Production represents a significant advancement in the digital transformation of quality assurance processes within the edible oil industry. By leveraging modern technologies to create a comprehensive and user-friendly platform, the project aims to deliver substantial improvements in product quality and operational efficiency. The successful implementation of this dashboard will not only enhance the company's competitive edge but also set a new benchmark for quality control in the industry, fostering higher standards and greater customer trust.


# **Dependencies**

## **Software and Libraries**

- **Python 3.12 or Higher**

## **Python Libraries**

 **dash==2.17.1**

- **Usage**: Web-based dashboard framework.
- **Installation**: pip install dash==2.17.1

 **dash-bootstrap-components==1.4.2**

- **Usage**: Bootstrap components for Dash.
- **Installation**: pip install dash-bootstrap-components==1.4.2

 **dash-core-components==2.0.0**

- **Usage**: Core components for Dash.
- **Installation**: pip install dash-core-components==2.0.0

 **dash-extensions==1.0.16**

- **Usage**: Extensions for Dash to enhance functionality.
- **Installation**: pip install dash-extensions==1.0.16

 **dash-html-components==2.0.0**

- **Usage**: HTML components for Dash.
- **Installation**: pip install dash-html-components==2.0.0

 **dash-table==5.0.0**

- **Usage**: Table components for Dash.
- **Installation**: pip install dash-table==5.0.0

 **dash_renderer==0.13.0**

- **Usage**: Dash's React renderer.
- **Installation**: pip install dash_renderer==0.13.0

 **dashtable==1.4.5**

- **Usage**: Create ASCII tables for terminals and plain text.
- **Installation**: pip install dashtable==1.4.5

 **dataclass-wizard==0.22.3**

- **Usage**: Simplify data class creation and manipulation.
- **Installation**: pip install dataclass-wizard==0.22.3

 **Flask==2.2.5**

- **Usage**: Lightweight web application framework.
- **Installation**: pip install Flask==2.2.5

 **Jinja2==3.1.4**

- **Usage**: Templating engine for Python.
- **Installation**: pip install Jinja2==3.1.4

 **mysql-connector-python==8.4.0**

- **Usage**: MySQL driver for Python.
- **Installation**: pip install mysql-connector-python==8.4.0

 **numpy==1.26.4**

- **Usage**: Fundamental package for array computing.
- **Installation**: pip install numpy==1.26.4

 **pandas==2.2.2**

- **Usage**: Data analysis and manipulation library.
- **Installation**: pip install pandas==2.2.2

 **plotly==5.22.0**

- **Usage**: Interactive graphing library.
- **Installation**: pip install plotly==5.22.0
- **Installation**: pip install pyodbc==5.1.0

 **requests==2.32.2**

- **Usage**: HTTP library for Python.

**Installation on Windows using terminal:**

pip install -r requirement.txt

## **Database**

- **MySQL 5.7**

# **Database Schema**
![image](https://github.com/user-attachments/assets/4a82bb98-dab5-41a1-9432-df6eb28764a5)

## **Detailed Explanation of the Database Schema**

The provided database schema is for managing quality control data in edible oil production. Here’s a detailed explanation of each table, including their primary and foreign keys, and the relationships between them:

### Tables and Relationships

1. **l_lab**
    - **Primary Key**: LAB_ID
    - **Columns**:
        - ID (INT): Unique identifier for the lab.
        - LABORATORY (VARCHAR(50)): Name of the laboratory.
        - LAB_ID (VARCHAR(10)): Unique lab identifier.
        - LOCATION (VARCHAR(50)): Location of the laboratory.
    - **Relationships:** Linked to **l_**usr**,** analysisreg and samplereg tables via LabID.
2. **l_smplr**
    - **Primary Key**: SAMPLER_ID
    - **Columns**:
        - SAMPLER_ID (INT): Unique identifier for the sampler.
        - SAMPLER (VARCHAR(20)): Name of the sampler.
        - SAMPLER_CONTACT (BIGINT): Contact information for the sampler.
    - **Relationships**: Linked to samplereg table via SamplerID.
3. **l_usr**
    - **Primary Key**: USER_ID
    - **Columns**:
        - USER_ID (INT): Unique identifier for the user.
        - USER (VARCHAR(50)): Username.
        - LAB_ID (VARCHAR(10)): Foreign key referencing LAB_ID in l_lab table.
        - CONTACT (BIGINT): Contact information for the user.
        - PASSWORD (VARCHAR(50)): User password.
    - **Relationships**: Linked to **l_**lab**,** samplereg and analysisreg tables via UserID.
4. **l_smplptmatrix**
    - **Primary Key**: SmplPtID
    - **Columns**:
        - PRODUCT (VARCHAR(13))
        - SmplPtID (VARCHAR(10)): Primary Key
        - SmplPt (VARCHAR(26))
        - CHK (INT)
    - **Relationships**: Linked to samplereg via SmplPtID.
5. **l_tst**
    - **Primary Key**: PRODUCT
    - **Columns**:
        - PRODUCT (VARCHAR(20)): Primary Key
        - PARAMETER_1 to PARAMETER_6 (VARCHAR(30))
    - **Relationships**: Linked to samplereg via PRODUCT.
6. **l_test**
    - **Primary Key**: id
    - **Columns**:
        - id (INT): Unique identifier for the test.
        - PRODUCT (VARCHAR(13)): Foreign key referencing PRODUCT in l_tst table.
        - SampleType (VARCHAR(9))
        - PARAMETER_1 to PARAMETER_6 (VARCHAR(3))
    - **Relationships**: Connected to l_tst and l_smplptmatrix.
7. **samplereg**
    - **Primary Key**: SampleID
    - **Columns**:
        - SampleID (INT): Unique identifier for the sample.
        - SamplerID (INT): Foreign key referencing SAMPLER_ID in l_smplr table.
        - Date_Time (DATETIME)
        - LabID (VARCHAR(10)): Foreign key referencing LabID in l_lab table.
        - UserID (INT): Foreign key referencing USER_ID in l_usr table.
        - Material (VARCHAR(20))
        - SampleType (VARCHAR(10))
        - PartyName (VARCHAR(100))
        - BatchID_WhVo (VARCHAR(10))
        - SmplPt (VARCHAR(10)): Foreign key referencing SmplPtID in l_smplptmatrix table.
        - QtyMt (DECIMAL(10,2))
        - Test_RQMT (VARCHAR(50))
        - Parameter_1 to Parameter_6 (VARCHAR(10))
        - Date_Time_Stmp (DATETIME)
    - **Relationships**: Linked to analysisreg, l_smplr, l_lab, l_usr, l_tst and l_smplptmatrix.
8. **analysisreg**
    - **Primary Key**: AnlysID
    - **Columns**:
        - AnlysID (INT): Unique identifier for the analysis.
        - SampleID (INT): Foreign key referencing SampleID in samplereg table.
        - LabID (VARCHAR(10)): Foreign key referencing LabID in l_lab table.
        - TestType (VARCHAR(10))
        - UserID (INT): Foreign key referencing USER_ID in l_usr table.
        - Material (VARCHAR(50))
        - M_C to SV (FLOAT): Various quality parameters.
        - Date_Time_Stmp (DATETIME)
        - Remarks (VARCHAR(50))
    - **Relationships**: Linked to samplereg via SampleID, l_lab via LAB_ID, l_usr via USER_ID.

### Summary of Key Relationships

1. **User Management**:
    - l_usr (Users) table is linked to samplereg (Sample Registration) and analysisreg (Analysis Registration) through USER_ID.
2. **Sample Management**:
    - samplereg links samples to samplers (l_smplr), laboratories (l_lab), and users (l_usr).
3. **Laboratory Management**:
    - l_lab (Labs) table is referenced in samplereg and analysisreg.
4. **Analysis and Quality Control**:
    - analysisreg tracks analysis results, linked back to samplereg for the sample details.
5. **Sample Point and Test Parameters**:
    - l_smplptmatrix and l_tst define sample points and test parameters, connected to tests in l_test.

Folder structure

The structure of the Dash application is presented below:

\- app.py

\- templates

  |-- analyse_form.html

  |-- dashboard.html

  |-- error.html

  |-- login.html

  |-- sample_form.html

  |-- success.html

\- dash_app.py

\- database_operations.py

\- db_connection.py

\- plot_mc_app.py

\- plot_oc_app.py

\- static

  |-- favicon.ico

  |-- base.css

  |-- style.css

\-assets

  [|-- custom_script.js](mailto:-custom@script.js)

  |-- extensions_default.js

  |-- style.css

## **Database Connection**

Dump MySQL Workbench Database in Webuzo Server

Open MySQL Settings wizard from Webuzo Control Panel.

Navigate to **Webuzo Control Panel > Database services > MySQL settings**

Fill the required fields and click on Save settings

After that the MySQL remote connection will be set successfully.

Database Tables

# **Authors**

**Sanidhya Rana**

# **Acknowledgments**

**Mentors:**

Mr. Himanshu Dwivedi

Mrs. Ruchika Khandelwal

# **Screenshots/Demo**
## **Login Page**
![Picture1](https://github.com/user-attachments/assets/9548402c-c107-4dfb-b5c2-ed13cd5fa47f)

## **Home Page**
![image](https://github.com/user-attachments/assets/7664ddad-8a69-424b-8fa7-ae2272be3ba7)

## **Sample Form**
![image](https://github.com/user-attachments/assets/21599107-5164-46ce-94f0-73e1d9452838)

## **Analysis Form**
![image](https://github.com/user-attachments/assets/f30a6cdd-4c5a-41d8-add6-8f6a0f8c1d50)

## **Analysis Report**
![image](https://github.com/user-attachments/assets/df4c2d11-9002-43a8-9483-7ccf0edb677d)

### Daily Analysis Report
![image](https://github.com/user-attachments/assets/a38ed31c-0921-47e0-9f89-caebe34cbb17)

### Dispatch Report
![image](https://github.com/user-attachments/assets/3e5eb653-576a-4c1b-ab00-4954518368f7)

## **Register**
![image](https://github.com/user-attachments/assets/e3ecd486-9552-4e1f-b737-f3140671067d)

### Sample Register
![image](https://github.com/user-attachments/assets/7be9d372-b851-4c71-8118-5e3fadcffb3c)

### Analysis Register
![image](https://github.com/user-attachments/assets/824b23e0-a168-49a1-b7af-ae2ab170e237)

## **Analysis Chart**

### M/C Analysis Chart
![image](https://github.com/user-attachments/assets/e1f83fea-aa72-4e66-b430-d766942e50ce)

### O/C Analysis Chart
![image](https://github.com/user-attachments/assets/b6629837-5eb0-4902-8466-3bc129f057f2)
