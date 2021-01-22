from flask import Flask, render_template, flash, redirect, url_for, send_from_directory, request, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug.utils import secure_filename
import wikiquote, random
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import json
import requests
import urllib.parse
import flickrapi
import urllib 
import pickle
import datetime
import uuid
import os
import io
import time

app = Flask(__name__)
Bootstrap(app)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"

db = SQLAlchemy(app)

#API keys
api_key = u'xxxxxxxxxxxxxxxxxxxx'
api_secret = u'xxxxxxxxxxxxxxxxxxx'
app.secret_key = 'xxxxxxxxxxxxxxxxxxxx'
flickr= flickrapi.FlickrAPI(api_key,api_secret,format='parsed-json')

#Create Data Datatable
class Data(db.Model):
    __tablename__ = 'Data'
    id = db.Column(db.String, primary_key=True)
    font_style = db.Column(db.String(100))
    font_url = db.Column(db.String(100))
    font_color = db.Column(db.String(100))
    font_size = db.Column(db.Integer)
    x_coordinate = db.Column(db.Integer)
    y_coordinate = db.Column(db.Integer)
    quote_text = db.Column(db.String(1500))
    url0 = db.Column(db.String(100))
    url1 = db.Column(db.String(100))
    url2 = db.Column(db.String(100))
    url3 = db.Column(db.String(100))
    url4 = db.Column(db.String(100))
    url5 = db.Column(db.String(100))
    url6 = db.Column(db.String(100))
    url7 = db.Column(db.String(100))
    url8 = db.Column(db.String(100))
    url9 = db.Column(db.String(100))
    url10 = db.Column(db.String(100))
    url11 = db.Column(db.String(100))
    url12 = db.Column(db.String(100))
    url13 = db.Column(db.String(100))
    url14 = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, id, font_style, font_url, font_color, font_size, x_coordinate, y_coordinate, quote_text, base_image, styled_image,
                 url0, url1, url2, url3, url4, url5, url6, url7, url8, url9, url10, url11, url12, url13, url14):
        
        self.id = id
        self.font_style = font_style
        self.font_url = font_url
        self.font_color = font_color
        self.font_size = font_size
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.quote_text = quote_text
        self.base_image = base_image
        self.styled_image = styled_image
        self.url0 = url0
        self.url1 = url1
        self.url2 = url2
        self.url3 = url3
        self.url4 = url4
        self.url5 = url5
        self.url6 = url6
        self.url7 = url7
        self.url8 = url8
        self.url9 = url9
        self.url10 = url10
        self.url11 = url11
        self.url12 = url12
        self.url13 = url13
        self.url14 = url14

db.create_all() 

@app.route('/')
def index():
    #Assign Unique Session ID
    if 'id' in session.keys() == True:
        pass
    else:
        session['id'] = uuid.uuid4().hex[:16]
        id = session['id']

    path1 = "static/Unedited_Image"
    path2 =  "static/Styled_Image"
    now = time.time()

    #delete photos older than 12 hours
    for filename in os.listdir(path1):
        # if os.stat(os.path.join(path, filename)).st_mtime < now - 5 * 86400:
        if os.path.getmtime(os.path.join(path1, filename)) < now - 0.5 * 86400:
            if os.path.isfile(os.path.join(path1, filename)):
                os.remove(os.path.join(path1, filename))

    #delete photos older than 12 hours     
    for filename in os.listdir(path2):
        # if os.stat(os.path.join(path, filename)).st_mtime < now - 5 * 86400:
        if os.path.getmtime(os.path.join(path2, filename)) < now -  0.5 * 86400:
            if os.path.isfile(os.path.join(path2, filename)):
                os.remove(os.path.join(path2, filename))

    #delete records in database older than 1 day
    limit = datetime.datetime.now() - datetime.timedelta(days=1)
    db.session.query(Data).filter(Data.date_created <= limit).delete()
    db.session.commit()

    #Insert Session Row to Data Table
    mydata = Data(id, None, None, None, None, 250, 250, None, None, None,
                 'https://live.staticflickr.com/65535/40830745703_6430007c6a_b.jpg',
                 'https://live.staticflickr.com/5816/23486046021_96b0529547_b.jpg', 
                 'https://live.staticflickr.com/705/23272768780_200797f5cf_b.jpg',
                 'https://live.staticflickr.com/622/31379579370_8409d5b337_b.jpg',
                 'https://live.staticflickr.com/509/31784388130_81aec36062_b.jpg',
                 'https://live.staticflickr.com/4586/38049127124_de39d7f24b_b.jpg', 
                 'https://live.staticflickr.com/1959/44587024794_19c01982fa_b.jpg', 
                 'https://live.staticflickr.com/276/30909743094_f15db2426e_b.jpg',
                 'https://live.staticflickr.com/1978/30429922717_26c8cec30d_b.jpg',
                 'https://live.staticflickr.com/1978/43694954610_a90cf35f87_b.jpg',
                 'https://live.staticflickr.com/90/277840874_9983fe8bbe_o.jpg',
                 'https://live.staticflickr.com/544/20256001381_260f1f296f_b.jpg',
                 'https://live.staticflickr.com/1933/45199962262_da696b1a97_b.jpg',
                 'https://live.staticflickr.com/2922/32436807393_1ef839813c_b.jpg',
                 'https://live.staticflickr.com/4687/39376518292_b68567da60_b.jpg')

    db.session.add(mydata)
    db.session.commit()
    return render_template('index.html')     

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/image_search', methods=["GET", "POST"])
def image_search():
    text = str(request.form['Item_2'])
    licenses = 7, 9, 10 #No known copyrights, Public Domain Dedication, #"Public Domain Mark"
    sort = 'relevance'
    privacy_filter = 1 #public photos
    safe_search = 1 #safe
    per_page = '15' #first 10 images
    page = '1' #first page

    #Flickr photo searh
    photos = flickr.photos.search(text = text, license = licenses, sort = sort, privacy_filter= privacy_filter,
                                  safe_search = safe_search, per_page = per_page, page = page)

    #Json for Flickr Search
    photo_list = photos['photos']['photo']

    #Flikr Search Photo id names
    p_ids = [photo_list[i]['id'] for i in range(len(photo_list))]

    #More json with photo sizes
    siz = [flickr.photos.getSizes(photo_id = i) for i in p_ids]

    #Url links for photo download, this is the original photo size
    myurls = [siz[i]['sizes']['size'][-1]['source'] for i in range(len(siz))]

    var_id = session['id']
    update = db.session.query(Data).filter(Data.id == var_id).one()
    update.url0 = myurls[0]
    update.url1 = myurls[1]
    update.url2 = myurls[2]
    update.url3 = myurls[3]
    update.url4 = myurls[4]
    update.url5 = myurls[5]
    update.url6 = myurls[6]
    update.url7 = myurls[7]
    update.url8 = myurls[8]
    update.url9 = myurls[9]
    update.url10 = myurls[10]
    update.url11 = myurls[11]
    update.url12 = myurls[12]
    update.url13 = myurls[13]
    update.url14 = myurls[14]
    db.session.commit()

    var_id = session['id']
    urls = db.session.query(Data).filter(Data.id == var_id).first()

    url0 = urls.url0
    url1 = urls.url1
    url2 = urls.url2
    url3 = urls.url3
    url4 = urls.url4
    url5 = urls.url5
    url6 = urls.url6
    url7 = urls.url7
    url8 = urls.url8
    url9 = urls.url9
    url10 = urls.url10
    url11 = urls.url11
    url12 = urls.url12
    url13 = urls.url13
    url14 = urls.url14
    return render_template('gallery.html', url0=url0, url1=url1, url2=url2, url3=url3,
                      url4=url4, url5=url5, url6=url6, url7=url7, url8=url8, url9=url9,
                      url10=url10, url11=url11, url12=url12, url13=url13, url14=url14)

@app.route("/popular_tags", methods=["GET", "POST"])
def popular_tags():
    if "open" in request.form:
        popular_tags = ['any color', 'sunset', 'beach', 'water', 'sky', 'flower', 'nature', 'night', 'tree',
                        'flowers', 'portrait', 'art', 'light', 'snow', 'dog', 'sun', 'clouds',
                        'park', 'winter', 'landscape', 'street', 'summer', 'sea', 'city', 'trees',
                        'lake', 'christmas', 'people', 'bridge', 'family', 'bird', 'river', 'house',
                        'car', 'food', 'old', 'music', 'new', 'moon', 'blackandwhite']
    elif "close" in request.form:
        popular_tags = []
    
    popular_tags = sorted(popular_tags)
    tags_printed = ', '.join(popular_tags)
    return render_template('index.html',  tags_printed=tags_printed)

@app.route('/gallery.html')
def gallery():
    var_id = session['id']
    urls = db.session.query(Data).filter(Data.id == var_id).first()
    
    url0 = urls.url0
    url1 = urls.url1
    url2 = urls.url2
    url3 = urls.url3
    url4 = urls.url4
    url5 = urls.url5
    url6 = urls.url6
    url7 = urls.url7
    url8 = urls.url8
    url9 = urls.url9
    url10 = urls.url10
    url11 = urls.url11
    url12 = urls.url12
    url13 = urls.url13
    url14 = urls.url14
    return render_template('gallery.html', url0=url0, url1=url1, url2=url2, url3=url3,
                      url4=url4, url5=url5, url6=url6, url7=url7, url8=url8, url9=url9,
                      url10=url10, url11=url11, url12=url12, url13=url13, url14=url14)

@app.route('/fonts.html')
def fonts():
    return render_template('fonts.html')

@app.route('/colors.html')
def colors():
    #Show Current Variable Data
    var_id = session['id']
    path1 = "static/Unedited_Image/"+ str(var_id) + '.jpg'
    if os.path.exists(path1) == True:
        image_file = 'Submitted'
    else:
        image_file = None

    #Show Current Variable Data
    data = db.session.query(Data).filter(Data.id == var_id).first()
    font_style = data.font_style
    font_color = data.font_color  
    return render_template('colors.html', image_file=image_file, font_style=font_style, font_color=font_color)

@app.route('/image_download', methods=["GET", "POST"])
def image_download():
    photo_number = int(request.form['Font1'])
    var_id = session['id']

    #This selects Image to download
    urls = db.session.query(Data).filter(Data.id == var_id).first()
    url_list = [urls.url0, urls.url1, urls.url2, urls.url3, urls.url4, urls.url5 , urls.url6, urls.url7, urls.url8,
    urls.url9, urls.url10, urls.url11, urls.url12, urls.url13, urls.url14]
    unaltered_image = urllib.request.urlopen( url_list[photo_number] ).read()

    #This resizes image while keeping proportions before download
    image = Image.open(io.BytesIO(unaltered_image))
    width, height = image.size
    maxwidth = 1024
    maxheight = 732

    if width > maxwidth or height > maxheight:
        new_width = int(width * min(maxwidth/width, maxheight/height))
        new_height = int(height * min(maxwidth/width, maxheight/height))
        image = image.resize((new_width, new_height), Image.ANTIALIAS)
    else:
        pass

    #This downloads image
    image.save('static/Unedited_Image/' + var_id + '.jpg')

    #Show current Variables
    var_id = session['id']
    path1 = "static/Unedited_Image/"+ str(var_id) + '.jpg'
    if os.path.exists(path1) == True:
        image_file = 'Submitted'
    else:
        image_file = None

    #Show Current Variable Data
    data = db.session.query(Data).filter(Data.id == var_id).first()
    font_style = data.font_style
    font_color = data.font_color  
    return render_template('colors.html', image_file=image_file, font_style=font_style, font_color=font_color)

@app.route('/font_style', methods=["GET", "POST"])
def font_style():
    var_id = session['id']
    
    #updata database
    data = db.session.query(Data).filter(Data.id == var_id).first()
    data.font_style = str(request.form['Font_Style'])
    data.font_url = "fonts/" + str(request.form['Font_Style'])

    db.session.commit()

    #Show Current Variables
    var_id = session['id']
    path1 = "static/Unedited_Image/"+ str(var_id) + '.jpg'
    if os.path.exists(path1) == True:
        image_file = 'Submitted'
    else:
        image_file = None

    #Show Current Variable Data
    data = db.session.query(Data).filter(Data.id == var_id).first()
    font_style = data.font_style
    font_color = data.font_color  
    return render_template('colors.html', image_file=image_file, font_style=font_style, font_color=font_color)

@app.route('/font_color', methods=["GET", "POST"])
def font_color():
    var_id = session['id']
    
    #update database
    data = db.session.query(Data).filter(Data.id == var_id).first()
    data.font_color = str(request.form['Color_Text'])
    db.session.commit()

    #Show Current Variables
    var_id = session['id']
    path1 = "static/Unedited_Image/"+ str(var_id) + '.jpg'
    if os.path.exists(path1) == True:
        image_file = 'Submitted'
    else:
        image_file = None

    #Show Current Variable Data
    data = db.session.query(Data).filter(Data.id == var_id).first()
    font_style = data.font_style
    font_color = data.font_color  
    return render_template('colors.html', image_file=image_file, font_style=font_style, font_color=font_color)

@app.route('/image.html')
def image():
    var_id = session['id']
    image_file = url_for('static', filename='/Unedited_Image/' + str(var_id) + '.jpg')
    
    #Show Current Variable Data
    data = db.session.query(Data).filter(Data.id == var_id).first()
    font_style = data.font_style
    font_color = data.font_color
    font_size = data.font_size
    coordinates = (data.x_coordinate, data.y_coordinate)
    quote_text = data.quote_text    
    if quote_text is None:
        pass
    else:
        quote_text = 'Submitted'

    return render_template('image.html', image_file=image_file, font_style=font_style, font_color=font_color,
                            font_size=font_size, coordinates = coordinates, quote_text= quote_text)

@app.route('/quote', methods=["GET", "POST"])
def quote_text():
    var_id = session['id']
    data = db.session.query(Data).filter(Data.id == var_id).first()

    data.quote_text = str(request.form['Quote_Text'])
    db.session.commit()

    image_file = url_for('static', filename='/Unedited_Image/' + str(var_id) + '.jpg')

    #Show Current Variable Data
    data = db.session.query(Data).filter(Data.id == var_id).first()
    font_style = data.font_style
    font_color = data.font_color
    font_size = data.font_size
    coordinates = (data.x_coordinate, data.y_coordinate)
    quote_text = data.quote_text    
    if quote_text is None:
        pass
    else:
        quote_text = 'Submitted'

    return render_template('image.html', image_file=image_file, font_style=font_style, font_color=font_color,
                            font_size=font_size, coordinates = coordinates, quote_text= quote_text)

@app.route('/coordinates', methods=["GET", "POST"])
def coordinates():
    var_id = session['id']
    
    #Updata Database
    data = db.session.query(Data).filter(Data.id == var_id).first()
    data.x_coordinate = int(request.form['X_Coordinate'])
    data.y_coordinate = int(request.form['Y_Coordinate'])
    db.session.commit()

    image_file = url_for('static', filename='/Unedited_Image/' + str(var_id) + '.jpg')

    #Show Current Variable Data
    data = db.session.query(Data).filter(Data.id == var_id).first()
    font_style = data.font_style
    font_color = data.font_color
    font_size = data.font_size
    coordinates = (data.x_coordinate, data.y_coordinate)
    quote_text = data.quote_text    
    if quote_text is None:
        pass
    else:
        quote_text = 'Submitted'

    return render_template('image.html', image_file=image_file, font_style=font_style, font_color=font_color,
                            font_size=font_size, coordinates = coordinates, quote_text= quote_text)

@app.route('/font_size', methods=["GET", "POST"])
def font_size():
    var_id = session['id']

    #Update Database
    data = db.session.query(Data).filter(Data.id == var_id).first()
    data.font_size = int(request.form['Font_size'])
    db.session.commit()

    image_file = url_for('static', filename='/Unedited_Image/' + str(var_id) + '.jpg')

    #Show Current Variable Data
    data = db.session.query(Data).filter(Data.id == var_id).first()
    font_style = data.font_style
    font_color = data.font_color
    font_size = data.font_size
    coordinates = (data.x_coordinate, data.y_coordinate)
    quote_text = data.quote_text    
    if quote_text is None:
        pass
    else:
        quote_text = 'Submitted'

    return render_template('image.html', image_file=image_file, font_style=font_style, font_color=font_color,
                            font_size=font_size, coordinates = coordinates, quote_text= quote_text)

@app.route('/styled_image', methods=["GET", "POST"])
def styled_image():
    #Create Edited Image
    var_id = session['id']
    data = db.session.query(Data).filter(Data.id == var_id).first()

    img_styled = Image.open('static/Unedited_Image/' + var_id + '.jpg')

    draw = ImageDraw.Draw(img_styled)
    font = ImageFont.truetype(data.font_url,  data.font_size)

    coordinates = (data.x_coordinate, data.y_coordinate)

    draw.text(coordinates, data.quote_text, data.font_color, font = font,
    align = "center" )

    save_string='static/Styled_Image/' + var_id + '.jpg'
    img_styled.save(save_string)

    #path is filename string
    image_file = url_for('static', filename='/Styled_Image/' + var_id + '.jpg')

    data = db.session.query(Data).filter(Data.id == var_id).first()
    font_style = data.font_style
    font_color = data.font_color
    font_size = data.font_size
    coordinates = (data.x_coordinate, data.y_coordinate)
    quote_text = data.quote_text    
    if quote_text is None:
        pass
    else:
        quote_text = 'Submitted'

    return render_template('image.html', image_file=image_file, font_style=font_style, font_color=font_color,
                            font_size=font_size, coordinates = coordinates, quote_text= quote_text)

@app.route('/daily_quote.html')
def daily_quote():
    todays_date = datetime.datetime.now()
    month = todays_date.strftime("%B")
    year = datetime.datetime.now().year

    web_address = "https://en.wikiquote.org/wiki/Wikiquote:Quote_of_the_day/" + month + "_" + str(year)
    return render_template('daily_quote.html', web_address = web_address)

@app.route('/wikiquote_quote.html', methods=["GET", "POST"])
def wiki_quote():
    month = request.form['Month']
    year = request.form['Year']

    web_address = "https://en.wikiquote.org/wiki/Wikiquote:Quote_of_the_day/" + month + "_" + str(year)
    return render_template('daily_quote.html', web_address = web_address)

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store', 'no-cache', 'must-revalidate',
    'post-check=0', 'pre-check=0', 'max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
