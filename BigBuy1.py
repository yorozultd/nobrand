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
            data.append("")
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
        if i==14:
            break
#bar.finish()
#with open("ENDPRODUCTS","wb") as f :
#    pickle.dump(PRODUCTS,f)
