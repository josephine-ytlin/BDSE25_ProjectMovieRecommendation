
import timeit

setup = """
import locale
"""
# test_yarn_mode = """
# from pyspark.sql import SparkSession
# from pyspark.ml.evaluation import RegressionEvaluator 
# from pyspark.ml.recommendation import ALS
# from pyspark.ml.tuning import TrainValidationSplit, ParamGridBuilder, CrossValidator


# #yarn mode
# spark = SparkSession\
#         .builder\
#         .master("yarn")\
#         .config('spark.executor.instances','3')\
#         .config('spark.executor.memory','4G')\
#         .config('spark.driver.memory','4G')\
#         .appName("ubuntu12")\
#         .getOrCreate()

# # Read raw dataset


# #確定dataset已存進HDFS,且確認namenode是哪一台
# df_ratings = spark.read.csv("hdfs://bdse50.example.com/tmp/ratings.csv", inferSchema=True, header=True)
# df_movies = spark.read.csv("hdfs://bdse50.example.com/tmp/movies.csv", inferSchema=True, header=True)


# (train, test) = df_ratings.randomSplit([0.7,0.3],seed=42)

# als =ALS(maxIter=5,\
#          regParam=0.01,\
#          userCol="userId",\
#          itemCol="movieId",\
#          ratingCol="rating",\
#          nonnegative = True,\
#          coldStartStrategy="drop",\
#          implicitPrefs = False)

# model = als.fit(train)

# pred = model.transform(test)

# pred_test = pred.filter(pred.prediction != float('nan'))

# evals_r2 = RegressionEvaluator(metricName="r2", labelCol="rating", predictionCol="prediction")
# evals_rmse = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")

# r2 = evals.evaluate(pred_test)
# print(f"R square:{r2}")
# rmse = evals.evaluate(pred_test)
# print(f"RMSE:{rmse}")

# #get recommendation for user 1

# user_1 = test.filter(test['userId'] == 1 ).select(['movieId','userId'])
# # user_1.show()
# rec = model.transform(user_1) 

# #see the movie recommendation results for user 1
# rec.join(df_movies, rec.movieId == df_movies.movieId, 'inner')\
# .select(rec["movieId"], rec["userId"], rec["prediction"], df_movies["title"],df_movies["genres"])\
# .distinct()\
# .orderBy(rec["prediction"],ascending=False)\
# .show(30,truncate=False)


# rec.orderBy("Prediction",ascending=False).describe().show(truncate=False)  
# """

# yarn_timeit = timeit.timeit(stmt=test_yarn_mode, setup=setup, number=5)

# print("yarn mode running time = ", yarn_timeit)


test_local_mode = """
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator 
from pyspark.ml.recommendation import ALS
from pyspark.ml.tuning import TrainValidationSplit, ParamGridBuilder, CrossValidator

#local mode
spark = SparkSession.builder.appName("modelDemoLocal").getOrCreate()

#.config('spark.driver.memory','16G')

df_ratings = spark.read.csv("file:///home/yutinglin/ml-25m/ratings.csv", inferSchema=True, header=True)
df_movies = spark.read.csv("file:///home/yutinglin/ml-25m/movies.csv", inferSchema=True, header=True)

(train, test) = df_ratings.randomSplit([0.7,0.3],seed=42)

als =ALS(maxIter=5,\
         regParam=0.01,\
         userCol="userId",\
         itemCol="movieId",\
         ratingCol="rating",\
         nonnegative = True,\
         coldStartStrategy="drop",\
         implicitPrefs = False)

model = als.fit(train)

pred = model.transform(test)

pred_test = pred.filter(pred.prediction != float('nan'))

evals_r2 = RegressionEvaluator(metricName="r2", labelCol="rating", predictionCol="prediction")
evals_rmse = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")

r2 = evals_r2.evaluate(pred_test)
print(f"R square:{r2}")
rmse = evals_rmse.evaluate(pred_test)
print(f"RMSE:{rmse}")

#get recommendation for user 1

user_1 = test.filter(test['userId'] == 1 ).select(['movieId','userId'])
# user_1.show()
rec = model.transform(user_1) 

#see the movie recommendation results for user 1
rec.join(df_movies, rec.movieId == df_movies.movieId, 'inner')\
.select(rec["movieId"], rec["userId"], rec["prediction"], df_movies["title"],df_movies["genres"])\
.distinct()\
.orderBy(rec["prediction"],ascending=False)\
.show(30,truncate=False)


rec.orderBy("Prediction",ascending=False).describe().show(truncate=False)  
"""

local_timeit = timeit.timeit(stmt=test_local_mode, setup=setup, number=5)

print("local mode running time = ", local_timeit/5)