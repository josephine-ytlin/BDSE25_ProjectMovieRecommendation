import pandas as pd
#load df which recommend 10 movies for each user
df_user_recs= pd.read_csv('df_user_recs.csv', index_col=[0])

#covert str into list and turn to Series
def users_recommendation(userId):
    recs = df_user_recs[df_user_recs['userId']==userId]
    movieid = pd.Series(recs.iloc[0,1][1:-1].split(', '))
    rating = pd.Series(recs.iloc[0,2][1:-1].split(', '))
    rec_matrix = pd.DataFrame(movieid, columns = ["movieId"])
    rec_matrix["rating"] = rating
    return rec_matrix
