import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from kaggle.api.kaggle_api_extended import KaggleApi
import os
from datetime import datetime

# 加载测试数据
test = pd.read_csv('data/kaggle/test.csv')
processed_df = test  # 在这里复刻你的特征工程
# 加载模型
model = XGBClassifier()
model.load_model('xgb_model.json')

# 预测
predictions = model.predict_proba(processed_df)[:,1]

# 创建提交文件
submission = pd.DataFrame({
    'id': test.id,
    'rainfall': predictions
})

# 生成带时间戳的文件名
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
submission_file = f'submission_{timestamp}.csv'

# 保存提交文件
submission.to_csv(submission_file, index=False)
print(f"预测完成，提交文件已保存为 {submission_file}")

# 使用Kaggle API上传结果
try:
    # 初始化Kaggle API
    api = KaggleApi()
    api.authenticate()
    
    # 上传提交文件
    competition = 'playground-series-s5e3'
    api.competition_submit(
        submission_file,
        f"XGBoost submission {timestamp}",
        competition
    )
    print(f"成功上传到Kaggle竞赛: {competition}")
    
except Exception as e:
    print(f"上传到Kaggle时出错: {str(e)}")
    print("请确保您已经：")
    print("1. 安装了kaggle包: pip install kaggle")
    print("2. 在~/.kaggle/kaggle.json中设置了API凭证")
    print("3. 设置了正确的文件权限: chmod 600 ~/.kaggle/kaggle.json") 