# BẮT BUỘC PHẢI CÓ ĐOẠN NÀY ĐỂ MAGE AI NHẬN DIỆN ĐƯỢC DECORATOR
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

import pandas as pd
from sqlalchemy import create_engine

@data_exporter
def export_data_to_neon(df: pd.DataFrame, **kwargs) -> None:
    """
    Đẩy trực tiếp dữ liệu AI đã phân tích lên máy chủ Neon Cloud.
    """
    print(f"🚀 Chuẩn bị đẩy {len(df)} bài báo sang Singapore (Neon Cloud)...")

    # 1. Cấu hình chìa khóa kết nối đến nhà Neon
    host = "ep-curly-dust-a1k3kq61-pooler.ap-southeast-1.aws.neon.tech"
    user = "neondb_owner"
    password = "npg_fby6LhI1giro"
    database = "neondb"
    
    # Tạo động cơ kết nối SSL bảo mật
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:5432/{database}?sslmode=require")

    # 2. Lọc đúng 5 cột mà Website Streamlit đang cần
    cols_to_export = ['published_at', 'title', 'sentiment_label', 'sentiment_score', 'url']
    
    # Kiểm tra xem df có đủ cột không trước khi đẩy
    missing_cols = [col for col in cols_to_export if col not in df.columns]
    if missing_cols:
        raise Exception(f"❌ DataFrame đang thiếu các cột: {missing_cols}")
        
    df_export = df[cols_to_export].copy()

    # 3. Bắn dữ liệu lên Cloud
    try:
        # Dùng if_exists='replace' để làm sạch 2 bài test cũ và thay bằng 100 bài mới nhất
        df_export.to_sql('news_articles', engine, if_exists='replace', index=False)
        print("✅ XUẤT SẮC! Đã đẩy thành công 100 bài báo lên Neon Cloud.")
    except Exception as e:
        print(f"❌ Lỗi khi đẩy lên Neon: {e}")
        raise e