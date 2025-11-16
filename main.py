import requests
from flask import Flask, render_template, request
import urllib.parse

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def show_result():
    
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
    else:
        keyword = request.args.get('keyword', '')


    if not keyword:
        return render_template('result.html',
                               all_data = [],
                               keyword=keyword,
                               sort_order='',
                               error='キーワードを入力してください。')    

    url = (
        f"https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
        f"?applicationId=[YOUR_APP_ID]&keyword={urllib.parse.quote(keyword)}"
    )
    res = requests.get(url)
    data = res.json()

    if not data.get('Items'):
        return render_template('result.html',
                               all_data=[],
                               keyword=keyword,
                               sort_order='',
                               error="該当する商品は見つかりませんでした。")

    all_data = []
    for d in data['Items']:
        all_data.append({
            'name': d['Item'].get('itemName'),
            'price': d['Item'].get('itemPrice'),
            'url': d['Item'].get('itemUrl'),
            'img': d['Item'].get('mediumImageUrls'),
            'review_count': d['Item'].get('reviewCount'),
            'review_average': d['Item'].get('reviewAverage')
        })

    
    sort_order = request.args.get('sort_order', '')
    if sort_order == 'sort_asc':
        all_data.sort(key=lambda x: x['price'])
    elif sort_order == 'sort_desc':
        all_data.sort(key=lambda x: x['price'], reverse=True)
    elif sort_order == 'sort_review_count_asc':
        all_data.sort(key=lambda x: x['review_count'], reverse=True)
    elif sort_order == 'sort_review_count_desc':
        all_data.sort(key=lambda x: x['review_count'])
    elif sort_order == 'review_average_high':
        all_data.sort(key=lambda x: x['review_average'])       
    elif sort_order == 'review_average_low':
        all_data.sort(key=lambda x: x['review_average'], reverse=True)  

    return render_template('result.html', all_data=all_data, keyword=keyword, sort_order=sort_order)

if __name__ == '__main__':
    app.run(debug=True)
