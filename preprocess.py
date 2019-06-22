# -*- coding: utf-8 -*-


'''
预处理数据为csv格式，包含了其得分和内容
'''
import random
import pandas as pd

excel = './data/conclusion/conclusion_s.xlsx'
text = './data/conclusion/conclusion.txt'

def parse_txt(line):
    isEmpty = 0
    line = line.strip().split(":", 2)
    ind_num = int(line[0].strip())
    student_num = str(int(line[1].strip()))
    content = line[2]
    content = content.strip().replace("第4节实验结论", "").replace(" ", "").strip()
    # print(ind_num, student_num, content)
    # print(len(content))
    if len(content)<=5: #实验结论为空
        isEmpty = 1
    return (ind_num, student_num, content, isEmpty)  


if __name__ == '__main__':

    val_ratio = 0.15
    conclusion = pd.read_excel(excel)
    conclusion = conclusion.iloc[:, 0:9]
    conclusion['学号'] = conclusion['学号'].astype('str')
    text_df = pd.DataFrame(columns = ('学号', 'content', 'isTrain')) 

    with open(text, encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for line in lines:
            is_train = 1 if random.randint(0, 100) > val_ratio*100 else 0
            ind_num, student_num, content, isEmpty = parse_txt(line)
            text_df = text_df.append([{'学号':student_num, 'content':content, 'isTrain':is_train}],
                 ignore_index=True)


    # print(text_df.head(10))    
    # print(conclusion.head(10)) 
    conclusion = pd.merge(conclusion, text_df, on = "学号")
    conclusion.to_csv('res.csv', index=False)
    # print(conclusion.head(10))


    test = pd.read_csv('res.csv')
    test['学号'] = test['学号'].astype('str')
    test.set_index('学号')


    print(test.head(50))
    print(test.dtypes)
    # # print(test.index)
    # print(test[test['实验结论为空']==1])


