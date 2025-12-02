# ⚖️ **LawMate — AI Contract Analyzer (NLP + Risk Detection + Summarization)**

LawMate is an AI-powered contract analysis tool that helps users **understand, summarize, and evaluate legal documents**.
It automatically:

* Extracts text from **PDF / DOCX / TXT**
* Splits content into **clauses**
* Highlights **risky legal phrases**
* Generates a **summary**
* Provides **semantic search + Q&A**
* Detects penalties, termination, confidentiality issues, liability risks, and more

Built using **Python, Streamlit, Sentence Transformers, and rule-based NLP**.

---

# ⭐ **Features**

### 🔍 **1. Smart Contract Text Extraction**

Supports:

* PDF
* DOCX
* TXT

### 🧩 **2. Clause Splitting**

Breaks long documents into meaningful legal clauses.

### 🚨 **3. Risk Detection Engine**

Uses **risk_keywords.json** to detect risky terms such as:

* Penalty
* Termination
* Confidentiality
* Refund / Non-refundable
* Liability
* Fees, charges

Shows severity → `low`, `medium`, `high`.

### 🧠 **4. Semantic Search + Q&A**

Embed clauses → match the best clause for any query using cosine similarity.

### 📝 **5. Contract Summarization**

LLM generated short & clear summary of the contract.

### 🎨 **6. Highlighted Risk View**

Risky clauses shown in **red**, others in normal text.

---

# 📁 **Project Structure**

```
LawMate/
│
├── app/
│   ├── main.py                  # Streamlit main application
│   └── components/
│       └── highlights.py        # UI for highlighting risky clauses
│
├── backend/
│   ├── analysis/
│   │   ├── risk_detector.py     # Rule-based risk analysis
│   │   ├── summarizer.py        # LLM summarizer
│   │   └── qa_engine.py         # Question answering engine
│   │
│   ├── nlp/
│   │   ├── clause_splitter.py   # Clause splitting logic
│   │   ├── embeddings.py        # Embedding model loading + encoding
│   │   ├── llm_client.py        # LLM connection
│   │   └── risk_rules.py        # Risk rule loader + checker
│   │
│   ├── parser/
│   │   ├── pdf_extractor.py     # PDF text reader
│   │   ├── docx_extractor.py    # DOCX reader
│   │   └── clean_text.py        # Cleaning utilities
│   │
│   └── utils/
│       ├── config.py            # Paths + config
│       └── file_reader.py       # Unified file reader
│
├── models/
│   ├── loader.py                # Model loader (embedding model)
│   └── rules/
│       └── risk_keywords.json   # Rule-based risk words
│
├── data/
│   └── uploads/                 # Uploaded files saved here
│
├── requirements.txt
└── README.md
```

---

# 🚀 **How the System Works**

### **1. User Uploads a Contract**

Streamlit saves the file into `data/uploads/`.

### **2. Backend Reads the File**

* PDF → extracted via PyPDF2
* DOCX → python-docx
* TXT → direct read

### **3. Clause Extraction**

`clause_splitter.py` splits text into 15–40 legal clauses.

### **4. Risk Analysis**

`risk_detector.py` loads rules from:

```
models/rules/risk_keywords.json
```

Example rules:

```json
{
    "high": ["terminate", "penalty", "non-refundable"],
    "medium": ["delay", "fee", "charge"],
    "low": ["confidential", "governing law"]
}
```

Matching is done by checking if any keyword appears in each clause.

### **5. Embedding + Semantic Search**

* All clauses → converted into vector embeddings.
* User question → also embedded.
* Compare using cosine similarity.
* Return best matching clauses.

### **6. Summarization**

`summary = summarize_document(text)`
Uses your chosen LLM (OpenAI / HuggingFace).

---

# 🧪 **Example Output Screenshot Section**

Add your images inside a folder:

```
RESULT PHOTOS/
   ├── input.PNG
   ├── highlighted_output.PNG
   └── summary_output.PNG
```

Then in README:

### 📸 **Screenshots**

#### **1️⃣ Input Screen**

<img src="RESULT PHOTOS/input.PNG" width="700">

#### **2️⃣ Highlighted Risky Clauses**

<img src="RESULT PHOTOS/highlighted_output.PNG" width="700">

#### **3️⃣ Summary & Q/A Panel**

<img src="RESULT PHOTOS/summary_output.PNG" width="700">

---

# 🔧 **Setup Instructions**

### **1. Clone the repo**

```bash
git clone https://github.com/JaweriaAsif745/LawMate
cd LawMate
```

### **2. Create Virtual Environment**

```bash
conda create -n lawmate python=3.10
conda activate lawmate
```

### **3. Install Requirements**

```bash
pip install -r requirements.txt
```

### **4. Run the App**

```bash
streamlit run app/main.py
```

---

# 💡 **Future Improvements**

* OCR support for scanned PDFs
* Multi-language contracts
* More advanced risk scoring
* User accounts + dashboard
* Model fine-tuning on legal datasets

---

# 🤝 **Contributing**

Pull requests are welcome!

---

# 🛡️ License

MIT License.

---
