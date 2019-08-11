import requests
import pickle
import json
from progress.bar import Bar
from time import sleep
import sys
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description="This is a program to handle Nobrand ")
parser.add_argument("-c","--saveCsv",action="store_true",help="It stores the csv")
parser.add_argument("-u","--update",action="store_true",help="It updates the numpy files")
parser.add_argument("-s","--sync",action="store_true",help="It syncs the files")

args=parser.parse_args()

senttoserver= False
UPDATE = False
STORE = False
add_product_endpoint = "http://no1brand.ru/add-product/"

AuthHeader= {"Authorization":"Bearer Zjk2ZTI0YWE1ZGNiNzBmMWNkZWIwNjliNTE2NzcyNDQ1N2EzMDllNzhhMGIyZDllNTViMmQxZGFhNWY5ODM3Yg"}
def update() :
    with open("Products","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/products", headers=AuthHeader)
        pickle.dump(r.content, f);
    with open("Information","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/productsinformation.json?isoCode=ru", headers=AuthHeader)
        pickle.dump(r.content, f);
    with open("Images","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/productsimages", headers=AuthHeader)
        pickle.dump(r.content, f);
    with open("Catagories","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/categories.json?isoCode=ru", headers=AuthHeader)
        pickle.dump(r.content, f);
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
if args.update:
    update()
    sys.exit()


with open("Products","rb") as f :
    products =pickle.load(f)
with open("Information","rb") as f :
    information =pickle.load(f)
with open("Images","rb") as f :
    images =pickle.load(f)
with open("Catagories","rb") as f :
    catagories =pickle.load(f)

productsjson = json.loads(products)
informationjson = json.loads(information)
imagesjson = json.loads(images)
catagoriesjson = json.loads(catagories)


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

if args.sync:
    
    sys.exit()

PRODUCTS = []
#bar = Bar('Processing', max=len(productsjson))

for i in range(len(productsjson)):
    #bar.next();
    thisproduct= productsjson[i]
    for j in range(len(informationjson)):
        if productsjson[i]['id'] == informationjson[j]['id']:
            thisinformation = informationjson[j]
            break
    for k in range(len(imagesjson)):
        if productsjson[i]['id']== imagesjson[k]['id']:
            thisimages = imagesjson[k]
            break
    product = Product()
    ids  = thisproduct['id']
    #description = thisinformation['description']
    #smalldescription = description[:100]
    smalldescription = description.split(".")[0]
    description = description.split(".")[1]
    title = thisinformation['name']
    sku  = thisinformation['sku']

# Please get this from https://api.bigbuy.eu/rest/catalog/categories.json?isoCode=ru :
    category= thisproduct['category']
# Please get this from https://api.bigbuy.eu/rest/catalog/categories.json?isoCode=ru :
    parent_category = thisproduct['category']

    style= "NAN"
    color= "NAN"
    gender = "NAN"
    data= [ids,smalldescription,description,title,sku,category,style,color,gender]
    numberofimages = len(thisimages['images'])
    for l in range(min(3,numberofimages)) :
        data.append(thisimages['images'][l]['url'])
    for h in range(3-numberofimages):
        data.append("Null")
    data.append(thisproduct['retailPrice'])
    data.append(thisproduct['inShopsPrice'])
    data.append(thisproduct['wholesalePrice'])
    product.setData(data)
    PRODUCTS.append(product)
    if senttoserver  :
        payload = {
                'bigbuy':                   data[0],
                'description':              data[1],
                'extended_description':     data[2],
                'title':                    data[3],
                'sku':                      data[4],
# TODO this variable
                'parent_category':          data[5],
                'category':                 data[5],
                'style':                    data[6],
                'colour':                   data[7],
                'gender':                   data[8],
                'image_1':                  data[9],
                'image_2':                  data[10],
                'image_3':                  data[11],
                'street_price':             data[12],
                'suggested_price':          data[13],
                'novat_price':              data[14],
        }
        r= requests.post(add_product_endpoint, data=payload)
        print(payload)
        print(r.content)
        break
#bar.finish()
#with open("ENDPRODUCTS","wb") as f :
#    pickle.dump(PRODUCTS,f)
