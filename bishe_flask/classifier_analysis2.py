import pandas as pd
from sklearn.externals import joblib
comments_lables= pd.read_csv("/home/zs/bishe/codes/comments_lables.csv")
#提取停用词
stop_words = set()
stop_files = ['HIT','SCU','CHN']
for file_name in stop_files:
    filepath = '/home/zs/bishe/codes/stopwords/{}.txt'.format(file_name)
    for words in open(filepath):
        stop_words.add(words)
stop_file = open('stop_file.txt', 'w')
for word in stop_words:
    stop_file.write(word)
stop_file.close()
def get_words(filepath = 'stop_file.txt'):
    stop_file = open(filepath)
    lists = [line [:-1] for line in stop_file]
    return lists
#利用词性分词
import jieba
import jieba.posseg as pseg
filter_type = {'x': '非语素字', 'm':'数词', 'eng': '英语','o': '拟声词',
               'e': '叹词', 'f':'方位词', 'nr': '人名','ns': '地名','nt':'机构团体'}
def cut_line(line):
    line = str(line)
    return " ".join([word.word for word in pseg.cut(line) if word.flag not in filter_type])
comments_lables['cut_values'] = comments_lables.Value.apply(cut_line)
#评分函数
def judge_score(y_pridict,y_test):
    num_array = confusion_matrix(y_test, y_pridict)
    sum_num = (num_array[0][0]+num_array[0][1])*2
    bili = (num_array[1][0]+num_array[1][1])/(num_array[0][0]+num_array[0][1])
    true_num = num_array[1][1]/bili + num_array[0][0] 
    true_bili = true_num/sum_num
    return true_bili
#分为训练集与测试集
from sklearn.model_selection import train_test_split
train_set,test_set = train_test_split(comments_lables,test_size=0.2, random_state=42)
y_train = [train_set['System'],train_set['Privacy'],train_set['Spam'],train_set['Finance'],train_set['Others']]
y_test = [test_set['System'],test_set['Privacy'],test_set['Spam'],test_set['Finance'],test_set['Others']]
#应用了MultinomialNB
from imblearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import imp
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
#from imblearn.over_sampling import SMOTE
#from imblearn.over_sampling import ADASYN
from imblearn.over_sampling import RandomOverSampler 
from imblearn.ensemble import EasyEnsemble
from sklearn.naive_bayes import MultinomialNB
#from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
#from sklearn.ensemble import AdaBoostClassifier
#from sklearn.ensemble import GradientBoostingClassifier
from sklearn import svm
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import mutual_info_classif
from sklearn.metrics import confusion_matrix
import copy
vec = CountVectorizer(
    #max_df=0.8,
    min_df=20,
    binary=False,
    token_pattern='(?u)\\b\\w+\\b',
    stop_words=frozenset(get_words()))
model = SelectKBest(mutual_info_classif, k=100)
test_pipeline = [0] * 5
for i in range(5): 
    test_pipeline[i] = Pipeline([('CountVectorizer',copy.deepcopy(vec)),('TfidfTransformer',TfidfTransformer()),('SelectFromModel',copy.deepcopy(model)),('smote',RandomOverSampler(random_state=42)),('MultinomialNB',svm.SVC(kernel='rbf'))])
    test_pipeline[i].fit(train_set.cut_values,y_train[i])
    joblib.dump(test_pipeline[i], "train_model{}.m".format(i))
