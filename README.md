# BDSE25_ProjectMovieRecommendation
```

├── Backend
├── Frontend
├── model
├── analyze
│   ├── EDA
│   └── feature_engineering   
└── README.md
```     
### This is a movie recommendation engine using Collaborative Filtering on Pyspark under Hadoop Ecosystem.
#### We use MovieLens 25M dataset and applied to Alternating Least Squares (ALS) matrix factorization.

#### ＊電影推薦系統：
#####    &nbsp;   預測用戶的觀賞傾向，依照用戶個人的喜好給出量身打造的電影推薦。
#### ＊使用工具與方法：
####   Container:
#####          以VMware建立Linux虛擬機
####   Data collection:
#####     1.以Selenium於IMDB與TMDBf網路爬蟲蒐集電影海報
#####     2.下載movielens公開授權的使用者評分、電影名稱、電影出版年份
####   Data analysis:
#####     1.以Python進行資料探索分析(EDA)
#####     2.以scikit-learn套件進行資料分群(K-means, DBSCAN）
####   Data processing:
#####     1.以Apache Hadoop建立分散式檔案處理系統處理，分析2500萬筆資料
#####     2.以Pyspark(Apache Spark in Python)編寫分析與建置統計模型
#####     3.以YARN啟動大數據叢集，進行機器學習模型訓練
####   Web delpoyment:
#####     1.以Flask框架呈現模型輸出之用戶電影推薦資料
#####     2.以HTML5與CSS5呈現後端傳送的資料部署至網站
