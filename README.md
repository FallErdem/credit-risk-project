# End-to-End Credit Risk Prediction System

Bu proje, **Machine Learning Bootcamp** kapsamında geliştirilmiş uçtan uca bir Kredi Risk Tahminleme sistemidir. Finansal verileri kullanarak müşterilerin temerrüde düşme (borcunu ödememe) ihtimalini hesaplar.

## Proje Amacı ve Kapsamı
Bankacılık sektöründe batık kredilerin (churn/default) önceden tespiti hayati önem taşır. Bu projede:
* Geçmiş ödeme verileri ve finansal limitler analiz edilmiştir.
* Dengesiz veri seti (Imbalanced Dataset) üzerinde çalışılmıştır.
* **XGBoost** algoritması ile %78 doğruluk oranına sahip bir model geliştirilmiştir.
* Model, **Streamlit** ile canlı bir web uygulamasına dönüştürülmüştür.

## Kullanılan Teknolojiler
* **Python 3.10+**
* **Veri Analizi:** Pandas, NumPy
* **Görselleştirme:** Matplotlib, Seaborn
* **Makine Öğrenmesi:** Scikit-learn, XGBoost (RandomizedSearchCV ile optimize edildi)
* **Arayüz (Deployment):** Streamlit
* **Model Kayıt:** Joblib

## Model Performansı ve Sonuçlar
Modelin başarısı "Recall" (Riskli müşteriyi yakalama) metriği üzerine optimize edilmiştir.

| Metrik | Skor | Açıklama |
| :--- | :--- | :--- |
| **ROC AUC** | **0.7821** | Modelin sınıf ayırma başarısı yüksektir. |
| **Recall (Riskli)** | **0.60** | Batacak müşterilerin %60'ı tespit edilmektedir. |
| **Accuracy** | **0.78** | Genel doğruluk oranı. |

### Confusion Matrix & Feature Importance
Model karar verirken en çok **"Maksimum Gecikme Süresi" (max_delay_month)** ve **"Toplam Gecikme Skoru"** özelliklerine odaklanmaktadır.


## Kurulum ve Çalıştırma

Projeyi lokalinizde çalıştırmak için adımları izleyin:

1. **Repoyu klonlayın:**
   ```bash
   git clone [https://github.com/KULLANICI_ADINIZ/credit-risk-project.git](https://github.com/KULLANICI_ADINIZ/credit-risk-project.git)
   cd credit-risk-project