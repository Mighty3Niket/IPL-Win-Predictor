import main
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import pickle

x = main.final_df.iloc[:,:-1]
y = main.final_df.iloc[:,-1]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)
#print(x_train.describe())

trf = ColumnTransformer([('trf', OneHotEncoder(sparse_output=False, drop='first'), ['BattingTeam', 'BowlingTeam', 'City'])], remainder='passthrough')

pipe = Pipeline(steps=[('step1', trf), ('step2', LogisticRegression(solver='liblinear'))])
pipe.fit(x_train, y_train)

y_pred = pipe.predict(x_test)
accuracy_score(y_test, y_pred)

pickle.dump(pipe, open('pipe.pkl','wb'))
pickle.load(open('pipe.pkl','rb'))
