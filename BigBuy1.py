# usage: rm -rf ./log/* && python3 BigBuy1.py >./bigbuy_log.out 2>./bigbuy_error.out &
import requests
import pprint
import csv
import pickle
import json
from progress.bar import Bar
from time import sleep
import sys
import argparse
import pandas as pd
import lib.logger as lgr
import time,datetime
import numpy as np




parser = argparse.ArgumentParser(description="This is a program to handle Nobrand ")
parser.add_argument("-c","--saveCsv",action="store_true",help="It stores the csv")
parser.add_argument("-u","--update",action="store_true",help="It updates the numpy files")
parser.add_argument("-s","--sync",action="store_true",help="It syncs the files")
parser.add_argument("-d","--send",action="store_true",help="It sends the files")

args=parser.parse_args()

senttoserver= False
UPDATE = False
STORE = False
add_product_endpoint = "http://no1brand.ru/add-product/"

AuthHeader= {"Authorization":"Bearer Zjk2ZTI0YWE1ZGNiNzBmMWNkZWIwNjliNTE2NzcyNDQ1N2EzMDllNzhhMGIyZDllNTViMmQxZGFhNWY5ODM3Yg"}
def update(logger) :
    logger.wtil("Now updating...")
    logger.wtil("Getting stock_info...")
    with open("stock_info","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/productsstock.json", headers=AuthHeader)
        pickle.dump(r.content, f);
    logger.wtil("Getting products...")
    with open("Products","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/products", headers=AuthHeader)
        pickle.dump(r.content, f);
    logger.wtil("Getting english_information...")
    with open("english_information","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/productsinformation.json?isoCode=en", headers=AuthHeader)
        pickle.dump(r.content, f);
    logger.wtil("Getting information...")
    with open("Information","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/productsinformation.json?isoCode=ru", headers=AuthHeader)
        pickle.dump(r.content, f);
    logger.wtil("Getting images...")
    with open("Images","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/productsimages", headers=AuthHeader)
        pickle.dump(r.content, f);
    logger.wtil("Getting categories...")
    with open("categories","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/categories.json?isoCode=ru", headers=AuthHeader)
        pickle.dump(r.content, f);
    logger.wtil("Done...")
class Product:
    def __init__(self):
        self.bigbuy=0
        self.small_description=0
        self.description=0
        self.title=0
        self.sku=0
        self.category=0
        self.style=0
        self.colour=0
        self.gender=0
        self.image_1=0
        self.image_2=0
        self.image_3=0
        self.street_price=0
        self.suggested_price=0
        self.novat_price=0
    def setData(self,productdata):
        self.bigbuy  = productdata[0]
        self.small_description  = productdata[1]
        self.description  = productdata[2]
        self.title  = productdata[3]
        self.sku  = productdata[4]
        self.category  = productdata[5]
        self.style  = productdata[6]
        self.colour  = productdata[7]
        self.gender  = productdata[8]
        self.image_1  = productdata[9]
        self.image_2  = productdata[10]
        self.image_3  = productdata[11]
        self.street_price  = productdata[12]
        self.suggested_price  = productdata[13]
        self.novat_price  = productdata[14]

logger = lgr.Logger("bigbuy")
ts = time.time()
logger.wtil("Launching application..."+datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
if args.update:
    update(logger)
    sys.exit()
if args.send:
    senttoserver=True

logger.wtil("Reading data from files...")
with open("Products","rb") as f :
    products =pickle.load(f)
with open("stock_info","rb") as f :
    stock_info = pickle.load(f)
with open("english_information","rb") as f :
    english_information =pickle.load(f)
with open("Information","rb") as f :
    information =pickle.load(f)
with open("Images","rb") as f :
    images =pickle.load(f)
with open("categories","rb") as f :
    categories =pickle.load(f)

productsjson = json.loads(products)
stock_info_json = json.loads(stock_info)
informationjson = json.loads(information)
english_informationjson = json.loads(english_information)
imagesjson = json.loads(images)
categoriesjson = json.loads(categories)

logger.wtil("Data processed...")

if args.saveCsv:
    ids =[]
    skus= []
    for i in range(len(productsjson)):
        ids.append(productsjson[i]['id'])
        skus.append(productsjson[i]['sku'])
    main = pd.DataFrame({
        "ID" : ids, "SKU": skus
    })
    main.to_csv("product_skus.csv")
    sys.exit()
def Quantity(idofProduct):
    for k in range(len(stock_info_json)):
        if idofProduct== stock_info_json[k]['id']:
            return stock_info_json[k]['stocks'][0]['quantity']
            
    
if args.sync:
    data = pd.read_csv("product_skus.csv") 
    dataArray = np.array(data)
    for i in range(dataArray):
        if( Quantity(dataArray[i][1]) < 1 ): 
            r=requests.get("https://api.bigbuy.eu/disable-product"+str(dataArray[i][2]), headers=AuthHeader)
    sys.exit()

PRODUCTS = []
#bar = Bar('Processing', max=len(productsjson))

logger.wtil("Now uploading products...")
logger.wtil("Number of products: "+str(len(productsjson)))
for i in range(len(productsjson)):
    #bar.next();
    thisproduct= productsjson[i]
    for j in range(len(informationjson)):
        if productsjson[i]['id'] == informationjson[j]['id']:
            thisinformation = informationjson[j]
            break
    for j in range(len(english_informationjson)):
        if productsjson[i]['id'] == english_informationjson[j]['id']:
            this_english_information = english_informationjson[j]
            break
    for k in range(len(imagesjson)):
        if productsjson[i]['id']== imagesjson[k]['id']:
            thisimages = imagesjson[k]
            break

    for k in range(len(stock_info_json)):
        if productsjson[i]['id']== stock_info_json[k]['id']:
            this_stock_info = stock_info_json[k]
            break

    stock_info = this_stock_info['stocks'][0]['quantity']
    product = Product()
    ids  = thisproduct['id']
    description = thisinformation['description']
    #smalldescription = description[:100]
    #smalldescription = description.split("\n")[0]
    #description = description.split("\n")[1]
    smalldescription = description[:100]
    description = description
    title = thisinformation['name']
    sku  = thisinformation['sku']

    title_in_english = this_english_information['name']
    description_in_english  = this_english_information['description']


# Please get this from https://api.bigbuy.eu/rest/catalog/categories.json?isoCode=ru :
    #category= thisproduct['category']
# Please get this from https://api.bigbuy.eu/rest/catalog/categories.json?isoCode=ru :
    #parent_category = thisproduct['category']
    for k in range(len(categoriesjson)):
        if thisproduct['category']== categoriesjson[k]['id']:
            this_cat_info = categoriesjson[k]
            break
    category= this_cat_info['name']
    parent_category = this_cat_info['parentCategory']
    style= "NAN"
    color= "NAN"
    gender = "NAN"
    data= [ids,smalldescription,description,title,sku,category,style,color,gender]
    try:
        numberofimages = len(thisimages['images'])
    except:
        numberofimages=0
    for l in range(min(3,numberofimages)) :
        try :
            data.append(thisimages['images'][l]['url'])
        except:
            data.append("data:image/jpeg;base64,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")
    for h in range(3-numberofimages):
        data.append("Null")
    data.append(thisproduct['retailPrice'])
    data.append(thisproduct['inShopsPrice'])
    data.append(thisproduct['wholesalePrice'])
    product.setData(data)
    PRODUCTS.append(product)
    logger.wtil("Passing: "+str(title_in_english))
    if senttoserver  :
        payload = {
                'bigbuy':                            data[0],
                'description':                       data[1],
                'extended_description':              data[2],
                'title':                             data[3],
# TODO this variable
                'descriptionInEnglish':              description_in_english,
                'titleInEnglish':                    title_in_english,
                'stock_info':                        stock_info,
                'supplier':                          "bigb",



                'sku':                               data[4],
# TODO this variable
                'parent_category':                   data[5],
                'category':                          data[5],
                'style':                             data[6],
                'colour':                            data[7],
                'gender':                            data[8],
                'image_1':                           data[9],
                'image_2':                           data[10],
                'image_3':                           data[11],
                'street_price':                      data[12],
                'suggested_price':                   data[13],
                'novat_price':                       data[14],
        }
        
        r= requests.post(add_product_endpoint, data=payload)
        logger.wtil(str(r.content))
        with open('skus.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([ids,str(r.content).split(" ")[5]])
        logger.wtil(str(pprint.pformat(payload)))
        logger.wtil(str(r.content))
        break
#bar.finish()
#with open("ENDPRODUCTS","wb") as f :
#    pickle.dump(PRODUCTS,f)
