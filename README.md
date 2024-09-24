# SQLite Query Generator
SQLite Query Generator is an intuitive AI-powered application that allows users to interact with SQLite 
databases seamlessly. Users can upload CSV files to create tables in their database, generate SQL queries 
based on their questions, and retrieve results directly from the database. Built using **LangChain** and **Streamlit**, 
this app is designed for ease of use, making database management accessible to everyone.

![result](https://github.com/user-attachments/assets/9b1cfc06-0c35-4a5d-b1a1-a2c5375ea613)

## Key Features
- **AI Models**: Powered by Mistral's `mistral-small-latest` for the chatbot model,
with Togethers's `togethercomputer/m2-bert-80M-8k-retrieval` used for embeddings.
- **Upload Files**:  Seamlessly upload CSV files in the `Upload Files` section to create database tables.
- **Interactive Queries**: Ask questions about the data, and the model will generate the corresponding SQL queries.
- **Query Results**: View the results of the executed queries directly within the application.
- **Custom API Keys**: Save and update API keys easily in the `API Keys` section.



## Getting Started

### Local Setup

To run the SQLite Query Generator locally, follow these steps:
1. **Clone the repository**
   ```bash
   git clone https://github.com/andrewiva99/sql-gen
   cd sql-gen
   ```

3. **Create Conda Environment**:
    ```bash
    conda create --name <env_name> python=3.10
    conda activate <env_name>
    ```

4. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the Application**:
    ```bash
    streamlit run app.py
    ```

### Docker Setup

Alternatively, you can use Docker to run the application:

```bash
docker pull andreybg/sql-gen
```

```bash
docker run -p 8501:8501 andreybg/sql-gen
```
