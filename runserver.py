from flask import Flask, request, jsonify 
from pymongo import MongoClient
import bs4, requests
app = Flask(__name__)
app.debug = True
connection = MongoClient()
db = connection.onecloud #database name = onecloud.
coll = db.data # collection name = data.

@app.route('/')
def crawler():
    rows = {}
    try:
        rows['data']=[]
        group = 'fds' #group name : javforever, jav, fds, hdd, fap2vn, javfshare and more
        y = 1
        while y <= 3: #total pagination
            url =  ('http://onecloud.media/group/%s?page=%s' % (group, y))
            req = requests.get(url)
            result = bs4.BeautifulSoup(req.text)
            hasil = result.select('tr')
            print('page : %s' % y)
            for val in hasil[2:]:
                if val.find(attrs={"data-placement": "top"}).get('class')[1] == 'glyphicon-ok-circle':
                    status = 'unlock'
                else:
                    status = 'lock'
                data = {
			        "id" : val.find_all('a')[1]['href'].replace('//onecloud.media/file/', ''),
			        "name" : val.find('a').string,
			        "owner" : val.find_all(attrs={"class": "col-md-1 middle text-center"})[0].getText(),
			        "size" : val.find_all(attrs={"class": "col-md-1 middle text-center"})[1].getText(),
			        "date" : val.find_all(attrs={"class": "col-md-1 middle text-center"})[2].getText(),
			        "file" : val.find_all('a')[1]['href'].replace('//', ''),
			        "embed" : val.find_all('a')[2]['href'].replace('//', ''),
			        "status" : status,
			        "group" : 'onecloud.media/group/%s' % group
		        }
                rows['data'].append(data)
                getColl = coll.find_one({'id': val.find_all('a')[1]['href'].replace('//onecloud.media/file/', '')})
                if not getColl:
                    print('insert : %s' % val.find('a').string)
                    coll.insert(data)
            y = y + 1         
        rows['meta'] = {
            'code'      : '200',
            'message'   : 'OK'
        }        
    except Exception as e:
        rows['meta'] = {
            'code'      : '404',
            'message'   : str(e)
        }
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4545)
