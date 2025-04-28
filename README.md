# Startup Garage Competition - LOI Document Creation

## Getting Started  
  
- Install [Ollama](https://ollama.com/download/windows)  
- Download the model from Ollama by typing in CMD: `ollama pull mistral`  
- Clone this repository  
- In the root folder, create a virtual environment: 
`python -m venv env`  
- Activate the environment: 
`env\Scripts\activate`  
- Install the project dependencies: `pip install -r requirements.txt`  
- Create and populate the database: `python populate_database.py`  
- Run the API `uvicorn app:app --reload` 