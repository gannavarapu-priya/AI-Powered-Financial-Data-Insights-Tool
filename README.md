# AI Powered Financial Data Insights Tool

Developed and deployed an AI-driven financial insights platform that allows users to explore and query companies 10-K reports with natural language questions.

# Project Overview

This project is a simple yet powerful tool that helps explore and understand the financial reports of big companies like Microsoft, Amazon, Apple, and Meta. It uses AI technology to let users ask questions in plain English about revenue, risks, and trends found in these companies’ official SEC 10-K filings. The app pulls relevant information from the reports and gives clear, easy-to-understand answers. Built with Streamlit, it combines natural language processing, document search, and user-friendly design to make digging into complex financial data much easier and faster.
## Files

### 1. `src/app.py`  
Main Streamlit app that serves the user interface, including company selection and question input.

### 2. `src/rag_chain.py`  
Core backend logic to retrieve relevant document chunks using FAISS vector store and generate answers with OpenAI models.

### 3. `src/ingest.py`  
Scripts to preprocess and ingest 10-K financial reports into vector stores.

### 4. `src/prompts.py`  
Prompt engineering templates for the AI question answering.

### 5. `requirements.txt`  
Specifies all Python dependencies needed to run this application.

## Installation

### Clone the repo
```bash
git clone https://github.com/gannavarapu-priya/AI-Powered-Financial-Data-Insights-Tool.git
cd AI-Powered-Financial-Data-Insights-Tool
```

### Set up virtual environment and install dependencies
```bash
python3 -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows
pip install -r requirements.txt
```
### Configure environment variables
Create a `.env` file in the root directory, add your keys:
```bash
OPENAI_API_KEY=your_openai_api_key
```

### Run the app locally
```bash
streamlit run src/app.py
```
---

## Usage

- Select a company from the dropdown.
- Ask questions about financial data, like revenue growth or risk factors.
- View AI-generated contextual answers pulled from 10-Ks.

---

## Data

- Financial reports (10-Ks) and vector indices are loaded dynamically.
- Large data files (vectorstore indexes, raw 10-Ks) are **not included** in the repo; prepare or download them separately.

---

## Contributing

Contributions, feedback, and improvements are welcome!  
Please fork the repository and open a pull request.

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or collaboration, contact: [gannavarapup.11@gmail.com](mailto:gannavarapup.11@gmail.com)

---

*Happy coding and learning!*


