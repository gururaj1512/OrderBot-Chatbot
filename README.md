# OrderBot
This is a OrderBot Project, for automated service to collect orders for an online restaurant.

# How to run?
### STEPS:

Clone the repository

```bash
Project repo: https://github.com/
```
### STEP 01- Create a environment after opening the repository

```bash
python -m venv venv
```

```bash
.\venv\Scripts\activate
```


### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```


### Create a `.env` file in the root directory and add your Pinecone & openai credentials as follows:

```ini
GROQ_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GOOGLE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```


```bash
# Finally run the following command
chainlit run app.py
```

Now,
```bash
open up localhost:8000
```


### Techstack Used:

- Python
- LangChain
- Chainlit
- Groq