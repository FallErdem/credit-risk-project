import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(
    page_title="Kredi Risk Tahmin Sistemi",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    div.stButton > button {
        width: 100%;
        background-color: #2c3e50;
        color: white;
        height: 50px;
        font-size: 18px;
        border-radius: 5px;
    }
    .stAlert {
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_resources():
    try:
        model = joblib.load('models/final_model.pkl')
        features = joblib.load('models/features.pkl')
        return model, features
    except Exception as e:
        st.error(f"Dosya yükleme hatası: {e}")
        return None, None

def main():
    model, model_features = load_resources()

    if not model:
        st.stop()

    st.sidebar.header("Müşteri Bilgi Girişi")
    
    with st.sidebar.form("input_form"):
        st.subheader("Finansal Bilgiler")
        limit_bal = st.number_input("Kredi Limiti", min_value=1000.0, value=50000.0, step=1000.0)
        age = st.slider("Yaş", 18, 80, 30)

        st.subheader("Gecikme Durumu (Son 6 Ay)")
        c1, c2, c3 = st.columns(3)
        pay_0 = c1.number_input("Eylül", value=0)
        pay_2 = c2.number_input("Ağustos", value=0)
        pay_3 = c3.number_input("Temmuz", value=0)
        pay_4 = c1.number_input("Haziran", value=0)
        pay_5 = c2.number_input("Mayıs", value=0)
        pay_6 = c3.number_input("Nisan", value=0)

        st.subheader("Fatura Tutarları")
        bc1, bc2 = st.columns(2)
        bill_amt1 = bc1.number_input("Eylül Fatura", value=0.0)
        bill_amt2 = bc2.number_input("Ağustos Fatura", value=0.0)
        bill_amt3 = bc1.number_input("Temmuz Fatura", value=0.0)
        bill_amt4 = bc2.number_input("Haziran Fatura", value=0.0)
        bill_amt5 = bc1.number_input("Mayıs Fatura", value=0.0)
        bill_amt6 = bc2.number_input("Nisan Fatura", value=0.0)

        st.subheader("Ödeme Tutarları")
        pc1, pc2 = st.columns(2)
        pay_amt1 = pc1.number_input("Eylül Ödeme", value=0.0)
        pay_amt2 = pc2.number_input("Ağustos Ödeme", value=0.0)
        pay_amt3 = pc1.number_input("Temmuz Ödeme", value=0.0)
        pay_amt4 = pc2.number_input("Haziran Ödeme", value=0.0)
        pay_amt5 = pc1.number_input("Mayıs Ödeme", value=0.0)
        pay_amt6 = pc2.number_input("Nisan Ödeme", value=0.0)

        submit_btn = st.form_submit_button("HESAPLA")

    if submit_btn:
        st.header("Analiz Sonucu")
        
        input_data = pd.DataFrame({
            'limit_bal': [limit_bal],
            'age': [age],
            'pay_0': [pay_0], 'pay_2': [pay_2], 'pay_3': [pay_3], 
            'pay_4': [pay_4], 'pay_5': [pay_5], 'pay_6': [pay_6],
            'bill_amt1': [bill_amt1], 'bill_amt2': [bill_amt2], 'bill_amt3': [bill_amt3],
            'bill_amt4': [bill_amt4], 'bill_amt5': [bill_amt5], 'bill_amt6': [bill_amt6],
            'pay_amt1': [pay_amt1], 'pay_amt2': [pay_amt2], 'pay_amt3': [pay_amt3],
            'pay_amt4': [pay_amt4], 'pay_amt5': [pay_amt5], 'pay_amt6': [pay_amt6]
        })

        input_data['avg_limit_use'] = (
            (input_data['bill_amt1'] / input_data['limit_bal'].replace(0, 1)) +
            (input_data['bill_amt2'] / input_data['limit_bal'].replace(0, 1)) +
            (input_data['bill_amt3'] / input_data['limit_bal'].replace(0, 1)) +
            (input_data['bill_amt4'] / input_data['limit_bal'].replace(0, 1)) +
            (input_data['bill_amt5'] / input_data['limit_bal'].replace(0, 1)) +
            (input_data['bill_amt6'] / input_data['limit_bal'].replace(0, 1))
        ) / 6

        pay_cols = ['pay_0', 'pay_2', 'pay_3', 'pay_4', 'pay_5', 'pay_6']
        input_data['total_delay_score'] = input_data[pay_cols].apply(lambda x: x[x > 0].sum(), axis=1)
        input_data['max_delay_month'] = input_data[pay_cols].max(axis=1)
        input_data['zero_payment_count'] = (input_data[pay_cols] == -2).sum(axis=1)

        input_data['bill_trend'] = input_data['bill_amt1'] - input_data['bill_amt6']

        for i in range(1, 7):
            input_data[f'unpaid_balance_{i}'] = input_data[f'bill_amt{i}'] - input_data[f'pay_amt{i}']
        
        input_data['avg_unpaid_balance'] = input_data[[f'unpaid_balance_{i}' for i in range(1, 7)]].mean(axis=1)
        input_data.drop([f'unpaid_balance_{i}' for i in range(1, 7)], axis=1, inplace=True)

        for i in range(1, 7):
            bill_col = f'bill_amt{i}'
            pay_col = f'pay_amt{i}'
            input_data[f'pay_ratio_{i}'] = np.where(input_data[bill_col] <= 0, 1, input_data[pay_col] / input_data[bill_col])

        input_data['avg_pay_ratio'] = input_data[[f'pay_ratio_{i}' for i in range(1, 7)]].mean(axis=1)
        input_data.drop([f'pay_ratio_{i}' for i in range(1, 7)], axis=1, inplace=True)

        input_data.replace([np.inf, -np.inf], 0, inplace=True)
        input_data.fillna(0, inplace=True)

        for col in model_features:
            if col not in input_data.columns:
                input_data[col] = 0
                
        final_input = input_data[model_features]

        proba = model.predict_proba(final_input)[0][1]
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if proba > 0.5:
                st.error(f"RİSKLİ MÜŞTERİ (Skor: {proba:.4f})")
                st.write("Bu müşterinin temerrüde düşme ihtimali yüksektir.")
            else:
                st.success(f"GÜVENİLİR MÜŞTERİ (Skor: {proba:.4f})")
                st.write("Bu müşteri için kredi onayı verilebilir.")
            
            st.progress(float(proba))

        with col2:
            st.metric("Risk Oranı", f"%{proba*100:.2f}")

        st.subheader("Hesaplanan Metrikler")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Ortalama Limit Kullanımı", f"%{input_data['avg_limit_use'].values[0]*100:.1f}")
        m2.metric("Toplam Gecikme Skoru", f"{input_data['total_delay_score'].values[0]:.0f}")
        m3.metric("Maksimum Gecikme", f"{input_data['max_delay_month'].values[0]:.0f} Ay")
        m4.metric("Kalan Bakiye Ort.", f"{input_data['avg_unpaid_balance'].values[0]:,.0f} TL")

if __name__ == "__main__":
    main()