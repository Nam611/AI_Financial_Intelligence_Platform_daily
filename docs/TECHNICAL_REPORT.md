# 📄 PROJECT TECHNICAL REPORT
## FinNexus 2.0: AI-Powered Financial Intelligence Platform

* **Prepared by:** Nguyen Nhut Nam – Data Engineer / AI Developer  
* **Domain:** Financial Technology (FinTech), Data Engineering, Artificial Intelligence  
* **System Type:** End-to-End ETL Data Pipeline & BI Dashboard  

---

### 1. EXECUTIVE SUMMARY
> In highly volatile financial markets, stock prices are heavily influenced by the constant influx of global and local news. **FinNexus 2.0** is an enterprise-grade Data Engineering platform designed to automate the ingestion of financial news, quantify market sentiment using advanced Natural Language Processing (NLP), and correlate these sentiment scores with stock market trends in real-time. By bridging the gap between unstructured text data and quantitative financial metrics, FinNexus empowers users to make data-driven, emotionless investment decisions.

---

### 2. PROBLEM STATEMENT (THE CHALLENGE)
* **Information Overload:** Human traders and analysts cannot manually monitor, read, and evaluate thousands of financial articles published daily.
* **Qualitative to Quantitative Gap:** News data is unstructured text. Without a standardized system to convert the "tone" of news into a mathematical score, correlation with numerical stock prices is impossible.
* **System Bottlenecks:** Traditional scraping scripts often crash, lack fault tolerance, and fail to scale when processing large volumes of data concurrently.

---

### 3. THE PROPOSED SOLUTION
FinNexus solves these challenges by implementing a highly resilient, cloud-integrated **ETL (Extract, Transform, Load)** architecture:

1. **Automated Ingestion:** Isolated Docker containers reliably scrape data without environmental conflicts.
2. **AI-Driven Transformation:** Leveraging the HuggingFace `DistilBERT` model to read Vietnamese financial news and assign precise mathematical sentiment scores.
3. **Orchestration & Cloud Storage:** Using **Mage AI** to orchestrate the pipeline and **SQLAlchemy** to push processed data into a Serverless Cloud Data Warehouse (**Neon PostgreSQL**).
4. **Fault-Tolerant Visualization:** A robust Streamlit frontend that dynamically visualizes the correlation without failing due to schema mismatches or missing data.

---

### 4. DATA PIPELINE SPECIFICATIONS (INPUTS & OUTPUTS)
To understand the core engine of FinNexus, the data flow is strictly categorized into explicit Inputs and Outputs across the pipeline layers. 

#### A. DATA EXTRACTION (The Ingestion Layer)
* **Inputs:** * Unstructured web data from major financial news outlets.
  * *Target elements:* `HTML tags`, `Timestamps`, `Article URLs`.
* **Outputs:** * Raw, tabular dataset stored in Local Staging PostgreSQL.
  * *Schema:* `[id, title, url, published_at, raw_content]`.

#### B. AI TRANSFORMATION (The NLP Layer via Mage AI)
* **Inputs:** * Unprocessed text strings from the Staging database.
  * Pre-trained `DistilBERT` weights for language comprehension.
* **Outputs:** * Machine-readable labels and numerical values.
  * **Output 1 (`sentiment_label`):** Categorical classification (`POSITIVE`, `NEGATIVE`, `NEUTRAL`).
  * **Output 2 (`sentiment_score`):** Continuous numerical value from `-1.0` (Extreme Fear/Negative) to `1.0` (Extreme Greed/Positive).

#### C. AGGREGATION & CORRELATION (The Merging Layer)
* **Inputs:**
  * Processed News Dataset (with AI scores).
  * Historical and Real-time Stock Market Data APIs (Tickers: `VN-Index`, `FPT`, `HPG`, `SSI`, `VCB`, etc. / Attributes: `Close Price`, `Trading Date`).
* **Outputs:**
  * A unified, multi-ticker analytical dataset mapping exact dates to both market close prices and the daily average sentiment score.

#### D. PRESENTATION (The BI Dashboard Layer)
* **Inputs:**
  * SQL queries fetching real-time data from the Neon Cloud Data Warehouse.
* **Outputs (End-User Value):**
  * **Real-time News Feed:** A dynamic, color-coded stream of the latest articles.
  * **Sentiment Distribution:** Donut charts displaying the macro-view of market psychology (bullish vs. bearish ratio).
  * **Dual-Axis Correlation Chart:** An interactive Altair chart overlaying the Stock Price (Line) against the AI Sentiment Score (Bar), revealing hidden market patterns.

---

### 5. SYSTEM ARCHITECTURE & ENGINEERING ACHIEVEMENTS
The architecture was intentionally designed to overcome common data engineering pitfalls. Key achievements include:

1. **Clean Architecture & Environment Isolation:** By decoupling the web crawler into a standalone Docker container, the system avoids dependency conflicts with the heavy AI models running in Mage AI.
2. **Robust Data Orchestration:** Migrated from basic cron jobs to **Mage AI** Directed Acyclic Graphs (DAGs). This provides complete observability, automated retry mechanisms, and block-level debugging.
3. **Cloud-Native Deployment (Serverless):** Transitioned the final analytical database from local storage to **Neon Serverless Postgres**. This enables global accessibility for the Streamlit Dashboard while maintaining zero infrastructure overhead.
4. **Frontend Fault-Tolerance ("Bulletproof UI"):** Developed robust data-handling functions in Streamlit. Implemented strict `try-except` blocks, `pd.to_numeric` type casting with `coerce`, and `dropna()` mechanisms. This guarantees the dashboard remains highly available and functional even if the Cloud database returns `NaN` values or altered schema fields (e.g., dynamically mapping `stock_price` to `Close`).

---

### 6. BUSINESS VALUE & CONCLUSION
**FinNexus 2.0** successfully demonstrates how modern Data Engineering, combined with AI, can transform chaotic internet noise into highly actionable financial intelligence.

By automating the entire lifecycle of data—from extraction to insight—the platform reduces manual analytical workloads by nearly 100%. The modular design ensures that scaling the system to include more news sources, new AI models, or additional stock tickers requires minimal engineering effort. It stands as a testament to high-performance pipeline design, cloud integration, and applied Machine Learning.