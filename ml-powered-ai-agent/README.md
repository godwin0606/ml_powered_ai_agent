# ml-powered-ai-agent

## Setup and Usage Steps

1. **Create .env file with required values**
2. **Get `groq_api_key` from Groq Console**
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Train the diabetes model:**
   ```bash
   python ml_src/train_diabetes_model.py
   ```
5. **Run prediction script (optional/test):**
   ```bash
   python ml_src/predict_diabetes.py
   ```
6. **Run the main agent script (testing crew):**
   ```bash
   python agents_src/main.py
   ```
7. **Launch the Streamlit app:**
   ```bash
   streamlit run streamlit_src/app.py
   ```
