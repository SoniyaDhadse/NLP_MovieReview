from flask import render_template,request,Flask
import nltk
import re
from nltk.corpus import stopwords
from gensim.models import Word2Vec
import numpy as np

app=Flask(__name__)
@app.route('/')
def home():
    return 'Welcome to Movie Review'
@app.route('/reviews',methods=['GET','POST'])
def reviews():
    if request.method=='GET':
        return render_template('reviews.html')
    else:
        f = str(request.form['review'])
        # data preprocessing
        text = re.sub(r'\[[0-9\*]', ' ', f)
        text = re.sub(r'\s+', ' ', text)
        text = text.lower()
        text = re.sub(r'\d', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        sentenses = nltk.sent_tokenize(text)
        sentenses = [nltk.word_tokenize(sentense) for sentense in sentenses]
        # print(sentenses)
        for i in range(len(sentenses)):
            sentenses[i] = [word for word in sentenses[i] if word not in stopwords.words('english')]
        # print(sentenses)
        # training Word2Vec
        model = Word2Vec(sentenses, min_count=1)
        words = model.wv.index_to_key
        # print(words)
        # print((model.wv.vectors))
        f = open("C:\\Users\\91885\\Downloads\\AFINN.txt", "r")
        rln1 = f.readlines()
        core = []
        for i in words:
            for x in rln1:
                rw = x.split()
                rw1 = rw[0:1]
                rw2 = rw[-1]
                # print(rw1,rw2)
                if i == rw[0]:
                    core.append(int(rw2))
        # print(sum(core))
        # result=(sum(core))
        result = np.round(np.mean(core))
        cases={-1:'Bad',-2:'Very Bad',-3:'Disgusting',0:'Not Good Not Bad',
            1:'OK',2:'Good',3:'Very Good',4:'Perfect',5:'Excellent Movie'}
        def review():
            result1=result
            func=cases.get(result1)
            return func
        review()
        # return render_template('reviews.html', res=result)
        return render_template('reviews.html', res=review())

if __name__=='__main__':
    app.run(debug=True)
