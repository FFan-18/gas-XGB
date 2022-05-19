import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error
import pandas as pd
import numpy as np
df = pd.read_pickle("10mix_absorp_ori_false.pickle")
xori = df.loc[0:1999,'absorp']
X = xori.values.tolist()
yori = df.loc[0:1999,'conc']
y = 1e6 * np.array(yori.values.tolist())


def my_func(x):
    return np.log(x+1.e-30) # 避免0值log出现nan
vfunc = np.vectorize(my_func) # 对coef每个元素取对数
X = vfunc(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=23)

# 模型初始化
model = xgb.XGBRegressor(max_depth = 6,learning_rate = 0.1,n_estimators=100,
                         objective = 'reg:squarederror',tree_method='gpu_hist')#参数定义可以参阅https://xgboost.readthedocs.io/en/stable/parameter.html
multi_ouput_model = MultiOutputRegressor(model) # XGBoost模型只支持单变量输出，这里应用sklearn打包一下
# 模型训练
multi_ouput_model.fit(X_train,y_train)

# 模型在test数据集上预测和评估
pred = multi_ouput_model.predict(X_test) # 获取模型预测值
loss = mean_absolute_error(y_test,pred, multioutput='raw_values') # 以平均绝对误差评估模型准确度

print(f'loss:{loss}')
for i,j in zip(pred,y_test):
    print(f'pred,real:{i,j},diff:{i-j}')













# multi_ouput_model.save_model('model.json') # 保存模型（多输出保存不了）