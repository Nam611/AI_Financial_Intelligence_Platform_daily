# 📈 FinNexus 2.0: AI Financial Intelligence Platform

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
![Mage AI](https://img.shields.io/badge/Mage_AI-Data_Pipeline-8A2BE2)
![PostgreSQL](https://img.shields.io/badge/Neon_Cloud-PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)

🎯 **Trải nghiệm Hệ thống Trực tiếp (Live Demo):** [FinNexus AI Intelligence Dashboard](https://finnexus-ai-intelligence.streamlit.app/)

**FinNexus 2.0** là một hệ thống Data Engineering toàn diện (End-to-End), được thiết kế với kiến trúc Clean Architecture. Hệ thống tự động hóa việc thu thập tin tức tài chính, phân tích tâm lý thị trường (Sentiment Analysis) bằng AI, và tìm ra mối tương quan với biến động giá cổ phiếu (Multi-Ticker) theo thời gian thực.

---

## 📑 Mục lục
- [Giới thiệu Dự án](#-giới-thiệu-dự-án)
- [Hệ thống Thực tế (System Showcase)](#-hệ-thống-thực-tế-system-showcase)
- [Kiến trúc Hệ thống (System Architecture)](#-kiến-trúc-hệ-thống-system-architecture)
- [Các Tính năng Cốt lõi](#-các-tính-năng-cốt-lõi)
- [Công nghệ Sử dụng (Tech Stack)](#-công-nghệ-sử-dụng-tech-stack)
- [Cấu trúc Dữ liệu (Database Schema)](#-cấu-trúc-dữ-liệu-database-schema)
- [Tác giả](#-tác-giả)

---

## 🚀 Giới thiệu Dự án
Trong kỷ nguyên thông tin, biến động của thị trường chứng khoán chịu ảnh hưởng mạnh mẽ bởi tin tức. **FinNexus** ra đời nhằm giải quyết bài toán: *Làm thế nào để lượng hóa tâm lý thị trường từ hàng ngàn bài báo tài chính mỗi ngày và đối chiếu nó với giá cổ phiếu một cách hoàn toàn tự động?*

Dự án là sự kết hợp hoàn hảo giữa **Data Extraction** (Docker Crawler), **Data Orchestration & Transformation** (Mage AI + NLP DistilBERT), **Cloud Data Warehousing** (Neon Postgres), và **Data Visualization** (Streamlit).

---

## 📸 Hệ thống Thực tế (System Showcase)

Dưới đây là minh chứng cho các luồng hoạt động thực tế của hệ thống từ Backend đến Frontend:

Link demo project : https://finnexus-ai-intelligence.streamlit.app/

### 1. Giao diện Phân tích Trực quan (Streamlit Dashboard)
*Bảng điều khiển cung cấp cái nhìn toàn cảnh về tâm lý thị trường và sự tương quan với giá cổ phiếu.*
<img width="1920" height="927" alt="image" src="https://github.com/user-attachments/assets/2ab08086-bf68-47e9-9847-a03443c79797" />
<img width="1920" height="929" alt="image" src="https://github.com/user-attachments/assets/7822f7fc-e419-49a2-9d89-0d6ca873d76d" />



### 2. Luồng Điều phối Dữ liệu (Mage AI Pipeline)
*Pipeline ETL tự động hóa việc cào dữ liệu thô, gọi model AI chấm điểm cảm xúc và hợp nhất dữ liệu.*
<img width="1610" height="854" alt="image" src="https://github.com/user-attachments/assets/73e968d2-0b29-4830-9bb9-fe05263a75f2" />


### 3. Lưu trữ Đám mây (Neon Serverless Postgres)
*Dữ liệu sau khi Transform được tự động đẩy lên Data Warehouse trên Cloud, sẵn sàng phục vụ truy vấn thời gian thực.*
<img width="1605" height="853" alt="image" src="https://github.com/user-attachments/assets/72df5c58-f94d-4f06-b20a-cdb8008d8998" />



---

## 🗺️ Kiến trúc Hệ thống (System Architecture)

Hệ thống được thiết kế theo mô hình **ETL (Extract - Transform - Load)** chuẩn doanh nghiệp, chia tách rõ ràng môi trường Staging (Local) và Production (Cloud) để tối ưu hóa hiệu suất và tính toàn vẹn của dữ liệu.

```mermaid
graph TD
    subgraph EXTRACTION [1. Data Extraction]
        A[Nguồn tin Tài chính] -->|Scraping| B(Docker Container: fn_crawler)
    end

    subgraph STAGING [2. Local Staging]
        B -->|Raw Data| C[(Local PostgreSQL)]
    end

    subgraph TRANSFORMATION [3. Orchestration & AI Transformation - Mage AI]
        C -->|Extract| D{Mage AI Pipeline}
        D -->|Transform| E[NLP Model: DistilBERT]
        E -->|Sentiment Score: -1 to 1| D
        D -->|Merge Data| F[Stock Price Aggregator]
    end

    subgraph PRODUCTION [4. Cloud Data Warehouse]
        F -->|Load via SQLAlchemy| G[(Neon Cloud Postgres: neondb)]
        D -->|Load via SQLAlchemy| G
    end

    subgraph PRESENTATION [5. Frontend Dashboard]
        G -->|Real-time Query| H[Streamlit Cloud App]
        H --> I((End User))
    end

    classDef container fill:#f9f,stroke:#333,stroke-width:2px;
    classDef db fill:#bbf,stroke:#333,stroke-width:2px;
    classDef ai fill:#ffd,stroke:#333,stroke-width:2px;
    class C,G db;
    class E ai;
### ⚙️ Luồng hoạt động chi tiết:

1. **Extract**: Job Docker chạy ngầm cào tin tức mới nhất và đổ vào CSDL PostgreSQL Local (Staging Area).
2. **Transform**: Mage AI được trigger, kéo dữ liệu thô lên. Bài báo được đưa qua mô hình AI (DistilBERT) để đọc hiểu và gán nhãn (POSITIVE, NEGATIVE, NEUTRAL) kèm điểm số.
3. **Merge**: Dữ liệu tâm lý (Sentiment) được gộp với dữ liệu giá cổ phiếu lịch sử (VN-Index, FPT, HPG, SSI...).
4. **Load**: Dữ liệu thành phẩm được đẩy lên Data Warehouse (Neon Cloud Postgres) thông qua SQLAlchemy.
5. **Visualize**: Streamlit Dashboard tự động render biểu đồ dựa trên dữ liệu Cloud mới nhất với cơ chế xử lý lỗi (Fault-Tolerant) mạnh mẽ.

---

## ✨ Các Tính năng Cốt lõi

* **Automated Data Ingestion:** Hệ thống Crawler chạy độc lập trong Docker Container, đảm bảo khả năng mở rộng.
* **AI-Powered Sentiment Analysis:** Tích hợp mô hình NLP tiên tiến để biến dữ liệu văn bản phi cấu trúc thành chỉ số định lượng.
* **Multi-Ticker Correlation:** Phân tích tương quan song song giữa điểm tâm lý và biến động giá của nhiều mã cổ phiếu.
* **Fault-Tolerant Dashboard:** Frontend "chống đạn" với cơ chế bọc lỗi `try-except`, tự làm sạch `NaN` và mapping Schema thông minh (vd: `stock_price` -> `Close`).

---

## 🛠️ Công nghệ Sử dụng (Tech Stack)

| Layer | Công nghệ | Mục đích |
| --- | --- | --- |
| **Data Extraction** | Python, Docker | Xây dựng và cô lập môi trường Crawler |
| **Orchestration** | Mage AI | Xây dựng và quản lý luồng ETL Pipeline (DAGs) |
| **AI / NLP** | HuggingFace, Transformers | Chấm điểm cảm xúc bài báo |
| **Data Storage** | PostgreSQL, Neon Cloud | Lưu trữ Staging (Local) và Data Warehouse (Cloud) |
| **Data Processing** | Pandas, SQLAlchemy | Làm sạch, ép kiểu và thao tác dữ liệu cấu trúc |
| **Frontend / BI** | Streamlit, Altair, Plotly | Xây dựng Dashboard tương tác trực quan |

---

## 🗄️ Cấu trúc Dữ liệu (Database Schema)

Hệ thống hoạt động dựa trên 2 bảng chính trên Neon Cloud:

1. **`news_articles`**: `[published_at, title, url, sentiment_label, sentiment_score]` - Lưu trữ tin tức đã qua xử lý AI.
2. **`market_correlation`**: `[date, ticker, close, sentiment_score]` - Dữ liệu đã gộp giữa giá cổ phiếu đóng cửa và điểm tâm lý trung bình.

---

## 👨‍💻 Tác giả

* **Nguyễn Nhựt Nam**
* *Data Engineer | Python Developer*

***

