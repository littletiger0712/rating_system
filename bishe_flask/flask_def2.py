import requests
import json
import pandas as pd
import jieba
import jieba.posseg as pseg
#import classifier_analysis2
from sklearn.externals import joblib
base_url = 'https://app.market.xiaomi.com/apm/comment/list/'
def get_comments(app_id):
    params = {'clientId': '3a0f6d2e1e8f3edd7f246f16c60961c0','os': '1513938363','sdk': 22,'page': 0}
    comments_list = []
    url = base_url+str(app_id)
    params['page'] = 0
    while(True):
        req = requests.get(url=url, params=params)
        res = json.loads(req.text)
        for item in res['comments']:
            if item['pointValue'] <= 3:
                comments_list.append(item['commentValue'])
        hasMore = res['hasMore']
        if hasMore == False:
            break
        else:
            params['page'] += 1
    app_comments = pd.DataFrame(comments_list, columns=['Value'])
    filter_type = {'x': '非语素字', 'm':'数词', 'eng': '英语','o': '拟声词',
               'e': '叹词', 'f':'方位词', 'nr': '人名','ns': '地名','nt':'机构团体'}
    def cut_line(line):
        line = str(line)
        return " ".join([word.word for word in pseg.cut(line) if word.flag not in filter_type])
    app_comments['cut_values'] = app_comments.Value.apply(cut_line)
    return app_comments
def get_score(app_id):
    predict = [0] * 5
    score = [''] * 5
    cut_v = get_comments(app_id).cut_values
    cut_v2 = []
    wordlist =['隐私','安全','权限','广告','短信','后台','盗取','流氓软件','泄露','打电话','个人信息','读取','禁止','授权','定位','扣费','下载','数据','流量','偷','录音','毒','扣','死机','号码','话费']
    for line in cut_v:
        for word in wordlist:
            if word in line:
                cut_v2.append(line)
                break
    #print(cut_v2)
    if cut_v2 == []:
        print('noone~')
        return ['A','A','A','A','A']
    for i in range(5):
        #print(cut_v)
        clf = joblib.load("train_model{}.m".format(i))
        predict[i] = clf.predict(cut_v2)
        sum_num = len(cut_v)
        one_num = 0
        for item in predict[i]:
            if item == 1:
                one_num +=1
        score_num = one_num / sum_num
        if score_num == 0:
            score[i] = 'A'
        elif score_num > 0 and score_num < 0.05:
            score[i] = 'B'
        elif score_num >= 0.05 and score_num < 0.1:
            score[i] = 'C'
        elif score_num >= 0.1:
            score[i] = 'D'
    return score


