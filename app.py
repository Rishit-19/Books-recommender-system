from flask import Flask, render_template, request
import pickle
import numpy as np

Top_50= pickle.load(open('Top_50.pkl','rb'))
books_df = pickle.load(open('book_df.pkl','rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
similar = pickle.load(open('similar.pkl','rb'))



app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template("index.html",
                           book_name= list(Top_50['Book-Title'].values),
                           author= list(Top_50['Book-Author'].values),
                           image=list(Top_50['Image-URL-M'].values),
                           votes=list(Top_50['num_rating'].values),
                           rating=list(Top_50['Book-Rating'].values))


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similar[index])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    # for i in similar_items:
    # print(pt.index[i[0]])

    for i in similar_items:
        item = []
        temp_df = books_df[books_df['Book-Title'] == pt.index[i[0]]]

        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)
    return render_template('recommend.html', data=data)


if __name__=='__main__':
    app.run(debug=True)