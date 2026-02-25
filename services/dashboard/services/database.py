import streamlit as st
import pandas as pd
import psycopg2
import os

def get_db_connection():
    # Ưu tiên lấy từ Streamlit Secrets
    if "postgres" in st.secrets:
        creds = st.secrets["postgres"]
        host, user, password, database = creds["host"], creds["user"], creds["password"], creds["database"]
    else:
        host = os.getenv('DB_HOST', "ep-curly-dust-a1k3kq61-pooler.ap-southeast-1.aws.neon.tech")
        user, password, database = "neondb_owner", "npg_fby6LhI1giro", "neondb"

    try:
        return psycopg2.connect(dbname=database, user=user, password=password, host=host, port="5432", sslmode="require")
    except Exception as e:
        st.error(f"❌ Lỗi kết nối: {e}")
        return None

@st.cache_data(ttl=600)
def load_data(ticker=None, days=7):
    conn = get_db_connection()
    if not conn: return pd.DataFrame()
    try:
        # 1. Bỏ source_name để fix KeyError
        query = f"SELECT published_at, title, sentiment_label, sentiment_score, url FROM public.news_articles WHERE published_at >= NOW() - INTERVAL '{days} days'"
        if ticker: query += f" AND (title ILIKE '%{ticker}%')"
        query += " ORDER BY published_at DESC"
        
        df = pd.read_sql(query, conn)
        conn.close()
        
        if not df.empty:
            # 2. Ép kiểu số để fix lỗi TypeError khi vẽ biểu đồ
            df['sentiment_score'] = pd.to_numeric(df['sentiment_score'], errors='coerce').fillna(0)
            df['published_at'] = pd.to_datetime(df['published_at'])
        return df
    except Exception as e:
        st.error(f"❌ Lỗi truy vấn News: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_correlation_data():
    conn = get_db_connection()
    if not conn: return pd.DataFrame()
    try:
        query = "SELECT * FROM public.market_correlation"
        df = pd.read_sql(query, conn)
        conn.close()
        
        if df.empty: return df
        
        # 1. Lưu lại danh sách tên cột gốc để báo cáo nếu thiếu
        raw_columns = df.columns.tolist()
        
        # 2. Chuyển hết về chữ thường và đổi tên
        df.columns = df.columns.str.lower()
        df.rename(columns={
            'ticker': 'Ticker', 
            'close': 'Close', 
            'sentiment_score': 'Sentiment_Score', 
            'date': 'Date'
        }, inplace=True)
        
        # 3. KIỂM TRA THÔNG MINH: Nếu không có cột Close thì báo lỗi rõ ràng ra màn hình
        if 'Close' not in df.columns:
            st.warning(f"⚠️ Dữ liệu Correlation bị thiếu cột giá đóng cửa. Các cột hiện có trên Neon DB là: {raw_columns}")
            # Trả về DF rỗng tạm thời để Web không bị sập (Crash)
            return pd.DataFrame()
            
        # 4. Nếu có đủ cột, tiến hành ép kiểu như bình thường
        df['Date'] = pd.to_datetime(df['Date'])
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        df['Sentiment_Score'] = pd.to_numeric(df['Sentiment_Score'], errors='coerce')
        
        return df.sort_values('Date', ascending=True)
        
    except Exception as e:
        st.error(f"❌ Lỗi truy vấn Correlation: {e}")
        return pd.DataFrame()