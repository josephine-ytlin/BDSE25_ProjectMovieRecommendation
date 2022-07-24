from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS, ALSModel
spark = SparkSession.builder.appName("ALSmodel").config('spark.driver.memory','16G').getOrCreate()
spark

df_ratings = spark.read.csv("file:///home/yutinglin/ml-25m/ratings.csv", inferSchema=True, header=True)
df_movies = spark.read.csv("file:///home/yutinglin/ml-25m/movies.csv", inferSchema=True, header=True)


model = ALSModel.load("file:///home/yutinglin/ml-25m/ALS_0719")

(train, test) = df_ratings.randomSplit([0.7,0.3],seed=42)
pred = model.transform(test)
pred.show()
pred_test = pred.filter(pred.prediction != float('nan'))

user_1 = test.filter(test['userId'] == 1 ).select(['movieId','userId'])
user_1.show()
rec = model.transform(user_1) 
rec.orderBy("Prediction",ascending=False).show() 
rec.join(df_movies, rec.movieId == df_movies.movieId, 'inner')\
.select(rec["movieId"], rec["userId"], rec["prediction"], df_movies["title"],df_movies["genres"])\
.distinct()\
.orderBy(rec["prediction"],ascending=False)\
.show()