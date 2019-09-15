# usage: rm -rf ./log/* && python3 BigBuy1.py --download >./bigbuy_log.out 2>./bigbuy_error.out &
# usage: python3 BigBuy1.py --find >./find_log_1 2>./find_error &
import requests
import xml.etree.ElementTree as ET

import pprint
import csv
import pickle
import json
from time import sleep
import sys
import argparse
import pandas as pd
import lib.logger as lgr
import time,datetime
import numpy as np

import allowed_categories
import minimum_price



parser = argparse.ArgumentParser(description="This is a program to handle Nobrand ")
parser.add_argument("-u","--download",action="store_true",help="It download the numpy files")
parser.add_argument("-s","--sync",action="store_true",help="It syncs the files")
parser.add_argument("-d","--send",action="store_true",help="It sends the files")
parser.add_argument("-f","--find",action="store_true",help="Find a product with sku")

args=parser.parse_args()

UPDATE = False
STORE = False

add_product_endpoint = "http://no1brand.ru/add-product/"

AuthHeader= {"Authorization":"Bearer Zjk2ZTI0YWE1ZGNiNzBmMWNkZWIwNjliNTE2NzcyNDQ1N2EzMDllNzhhMGIyZDllNTViMmQxZGFhNWY5ODM3Yg"}

def download(logger) :
    logger.wtil("Now updating...")

    logger.wtil("Getting stock_info...")
    with open("./api_data/stock_info","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/productsstock.json", headers=AuthHeader)
        pickle.dump(r.content, f);

    logger.wtil("Getting variation stock_info...")
    with open("./api_data/variation_stock_info","wb") as f :
        r=requests.get("http://api.bigbuy.eu/rest/catalog/productsvariationsstock.json", headers=AuthHeader)
        pickle.dump(r.content, f);

    logger.wtil("Getting products...")
    with open("./api_data/Products","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/products", headers=AuthHeader)
        pickle.dump(r.content, f);
    logger.wtil("Getting english_information...")
    with open("./api_data/english_information","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/productsinformation.json?isoCode=en", headers=AuthHeader)
        pickle.dump(r.content, f);
    logger.wtil("Getting information...")
    with open("./api_data/Information","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/productsinformation.json?isoCode=ru", headers=AuthHeader)
        pickle.dump(r.content, f);
    logger.wtil("Getting images...")
    with open("./api_data/Images","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/productsimages", headers=AuthHeader)
        pickle.dump(r.content, f);
    logger.wtil("Getting categories...")
    with open("./api_data/categories","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/categories.json?isoCode=ru", headers=AuthHeader)
        pickle.dump(r.content, f);

    with open("./api_data/categoriesEn","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/categories.json?isoCode=en", headers=AuthHeader)
        pickle.dump(r.content, f);

    logger.wtil("Getting attributes...")
    with open("./api_data/attributes_english","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/attributes.json?isoCode=en", headers=AuthHeader)
        pickle.dump(r.content, f);

    with open("./api_data/attributes_russian","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/attributes.json?isoCode=ru", headers=AuthHeader)
        pickle.dump(r.content, f);

    with open("./api_data/attributes_groups_english","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/attributegroups.json?isoCode=en", headers=AuthHeader)
        pickle.dump(r.content, f);

    with open("./api_data/attributes_groups_russian","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/attributegroups.json?isoCode=ru", headers=AuthHeader)
        pickle.dump(r.content, f);



    logger.wtil("Getting manufacturers...")
    with open("./api_data/manufacturers","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/manufacturers.json", headers=AuthHeader)
        pickle.dump(r.content, f);

    logger.wtil("Getting Variations...")
    with open("./api_data/variations","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/variations", headers=AuthHeader)
        pickle.dump(r.content, f);

    logger.wtil("Getting Product Variations...")
    with open("./api_data/productsvariations","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/productsvariations", headers=AuthHeader)
        pickle.dump(r.content, f);

    logger.wtil("Getting productsvariationsstock...")
    with open("./api_data/productsvariationsstock","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/productsvariationsstock", headers=AuthHeader)
        pickle.dump(r.content, f);

    logger.wtil("Getting productsvariationsstockavailable...")
    with open("./api_data/productsvariationsstockavailable","wb") as f :
        r=requests.get("https://api.bigbuy.eu/rest/catalog/productsvariationsstockavailable", headers=AuthHeader)
        pickle.dump(r.content, f);

    logger.wtil("Done...")

class Product:
    def __init__(self):
        self.bigbuy             = 0
        self.small_description  = 0
        self.description        = 0
        self.title              = 0
        self.sku                = 0
        self.category           = 0
        self.style              = 0
        self.colour             = 0
        self.gender             = 0
        self.image_1            = 0
        self.image_2            = 0
        self.image_3            = 0
        self.street_price       = 0
        self.suggested_price    = 0
        self.novat_price        = 0

    def setData(self,productdata):
        self.bigbuy             = productdata[0]
        self.small_description  = productdata[1]
        self.description        = productdata[2]
        self.title              = productdata[3]
        self.sku                = productdata[4]
        self.category           = productdata[5]
        self.style              = productdata[6]
        self.colour             = productdata[7]
        self.gender             = productdata[8]
        self.image_1            = productdata[9]
        self.image_2            = productdata[10]
        self.image_3            = productdata[11]
        self.street_price       = productdata[12]
        self.suggested_price    = productdata[13]
        self.novat_price        = productdata[14]

logger = lgr.Logger("bigbuy")
ts = time.time()

logger.wtil("Launching application..."+datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

if args.download:
    download(logger)
    sys.exit()

logger.wtil("Reading data from files...")
with open("./api_data/Products","rb") as f :
    products =pickle.load(f)
with open("./api_data/stock_info","rb") as f :
    stock_info = pickle.load(f)
with open("./api_data/variation_stock_info","rb") as f :
    variation_stock_info = pickle.load(f)
with open("./api_data/english_information","rb") as f :
    english_information =pickle.load(f)
with open("./api_data/Information","rb") as f :
    information =pickle.load(f)
with open("./api_data/Images","rb") as f :
    images =pickle.load(f)
with open("./api_data/categories","rb") as f :
    categories =pickle.load(f)
with open("./api_data/manufacturers","rb") as f :
    manufacturers =pickle.load(f)

with open("./api_data/variations","rb") as f :
    variations = pickle.load(f)

with open("./api_data/productsvariations","rb") as f :
    productsvariations = pickle.load(f)
with open("./api_data/productsvariationsstock","rb") as f :
    productsvariationsstock = pickle.load(f)


with open("./api_data/categoriesEn","rb") as f :
    categoriesEn =pickle.load(f)

with open("./api_data/attributes_english","rb") as f :
    attributes_english =pickle.load(f)

with open("./api_data/attributes_russian","rb") as f :
    attributes_russian =pickle.load(f)

with open("./api_data/attributes_groups_english","rb") as f :
    attributes_groups_english =pickle.load(f)

with open("./api_data/attributes_groups_russian","rb") as f :
    attributes_groups_russian =pickle.load(f)




productsjson = json.loads(products)
stock_info_json = json.loads(stock_info)
variation_stock_info_json = json.loads(variation_stock_info)

informationjson = json.loads(information)
english_informationjson = json.loads(english_information)
imagesjson = json.loads(images)
categoriesjson = json.loads(categories)
categoriesjsonEn = json.loads(categoriesEn)
manufacturersjson = json.loads(manufacturers)
productsvariations_json = json.loads(productsvariations)

productsvariationsstock_json = json.loads(productsvariationsstock)

variations_json = json.loads(variations)

attributes_groups_english_json = json.loads(attributes_groups_english)
attributes_groups_russian_json = json.loads(attributes_groups_russian)

attributes_english_json = json.loads(attributes_english)
attributes_russian_json = json.loads(attributes_russian)

logger.wtil("Data processed...")

def Quantity(idofProduct,stock_info_json):
    this_stock_info = [x for x in stock_info_json if x['sku'] == idofProduct]
    if(len(this_stock_info) == 0):
     return 0
    stock_info  = this_stock_info[0]['stocks'][0]['quantity']

    return stock_info

if args.sync:

    all_listing_skus = []
    all_listing_inner_skus = []
    resp=requests.get(url="http://no1brand.ru/get-number-of-active-products/bigb")
    number_of_active_products = int(resp.content)
    number_of_requests = int(number_of_active_products / 1000)

    for i in range(0,number_of_requests+1):
     offset = i*1000
     resp=requests.get(url="http://no1brand.ru/product-xml-with-offset/"+str(offset)+"/bigb")
     root = ET.fromstring(resp.content)
     [all_listing_skus.append(x.text) for x in root.findall('./product/sku')]
     [all_listing_inner_skus.append(x.text) for x in root.findall('./product/inner_sku')]
    logger.wtil("Number of products: "+str(len(all_listing_skus)))


    for sku in all_listing_skus:
        if( Quantity(sku,stock_info_json) < 1 ):

            endpoint = "http://no1brand.ru/disable-product-with-sku/"+str(sku)
            logger.wtil("Now disabling: "+str(sku))
            resp=requests.get(url=endpoint)

            logger.wtil(str(resp.content))

    logger.wtil("Finished sync...")
    sys.exit()

products = []

logger.wtil("Now uploading products...")
number_of_products = len(productsjson)
number_of_updated_products = 0
logger.wtil("Number of products: "+str(number_of_products))

disabled_categories = []
for i in range(len(productsjson)):
    thisproduct = productsjson[i]
    product_id = productsjson[i]['id']

    thisinformation = [x for x in informationjson if x['id'] == product_id][0]
    this_english_information = [x for x in english_informationjson if x['id'] == product_id][0]
    thisimages = [x for x in imagesjson if x['id'] == product_id][0]
    this_stock_info = [x for x in stock_info_json if x['id'] == product_id][0]
    this_variation  = [x for x in productsvariations_json if x['product'] == product_id]

    stock_info  = this_stock_info['stocks'][0]['quantity']
    ids         = thisproduct['id']
    description = thisinformation['description']
    title       = thisinformation['name']
    sku         = thisinformation['sku']

    title_in_english = this_english_information['name']

    for k in range(len(categoriesjson)):
        if thisproduct['category']== categoriesjson[k]['id']:
            this_cat_info = categoriesjson[k]
            break
    for k in range(len(categoriesjsonEn)):
        if thisproduct['category']== categoriesjsonEn[k]['id']:
            this_cat_infoEn = categoriesjsonEn[k]
            break
    category= this_cat_info['name']
    categoryEn= this_cat_infoEn['name']

    for k in range(len(manufacturersjson)):
        if thisproduct['manufacturer']== manufacturersjson[k]['id']:
            manufacturer = manufacturersjson[k]['name']
            break

    upload_this = False
    if(categoryEn in allowed_categories.ac and int(thisproduct['wholesalePrice']) > minimum_price.mp):
#     logger.wtil("At product: "+str(title_in_english)+" ("+str(categoryEn)+") "+str(i))
     upload_this = True
     disabled_skus = ["S0322441"]
     if(sku in disabled_skus):
      upload_this = False
    else: 
     if(categoryEn not in disabled_categories ):
       disabled_categories.append(categoryEn)
    if(i % 10000 == 0): 
     logger.wtil("disabled_categories: "+str(disabled_categories)+" "+str(i))

    product = Product()
    smalldescription = description[:100]
    description = description
    description_in_english  = this_english_information['description']


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
    products.append(product)
    number_of_variations = len(this_variation)

    has_variations = 1 if number_of_variations > 0 else 0
     

#    if(args.find and str(ids) == "1041749"):
#     logger.wtil("At product: ("+str(sku)+") "+str(title_in_english)+" ("+str(categoryEn)+") "+str(i))
#     logger.wtil(str(thisproduct))
#     logger.wtil(str(thisinformation))
#    if(args.find and str(sku) == "S0329581"):
#     logger.wtil("At product: ("+str(sku)+") "+str(title_in_english)+" ("+str(categoryEn)+") "+str(i))
#     logger.wtil(str(thisproduct))
#     logger.wtil(str(thisinformation))
    

          
      

    full_payload = {}
    if(args.send and upload_this):
     if(has_variations):
      logger.wtil("Number of variations: "+str(len(this_variation)))
      logger.wtil("This has these variations: "+str(this_variation))

      variation_counter = 0

      for variation in this_variation: 
       wholesale_price = variation['wholesalePrice']
       retail_price    = variation['retailPrice']
       this_attribute  = [x for x in variations_json if x['id'] == variation['id']]
#       logger.wtil("Attributes : "+str(this_attribute))
       for attribute_1 in this_attribute:
        attribute_2 = attribute_1['attributes']
        for attribute_3 in attribute_2:
#         logger.wtil("Attr. Id : "+str(attribute_3['id']))
         attr_id = attribute_3['id']
         variation_stock_info = [x for x in variation_stock_info_json if x['id'] == attr_id][0]["stocks"][0]["quantity"] if len([x for x in variation_stock_info_json if x['id'] == attr_id]) > 0 else 0

         english_attributes  = [x for x in attributes_english_json if x['id'] == attr_id]
#         logger.wtil("Attr. : "+str(english_attributes))
         attribute_name = english_attributes[0]['name'] if len(english_attributes) > 0 else  "UNKNOWN"
         for english_attribute in english_attributes:
          a_group  = [x for x in attributes_groups_english_json if x['id'] == english_attribute['attributeGroup']]
#          logger.wtil("Group. : "+str(a_group))
          group_name = a_group[0]['name'] if len(a_group) > 0 else "UNKNOWN"
          english_value = attribute_name
          english_name  = group_name

          full_payload.update({'english_name_'+str(variation_counter) : english_name }) 
          full_payload.update({'english_value_'+str(variation_counter) : english_value }) 
          full_payload.update({'stock_info_'+str(variation_counter) : variation_stock_info }) 

         russian_attributes  = [x for x in attributes_russian_json if x['id'] == attr_id]
#         logger.wtil("Attr. : "+str(russian_attributes))
         attribute_name = russian_attributes[0]['name'] if len(russian_attributes) > 0 else  "UNKNOWN"
         for russian_attribute in russian_attributes:
          a_group  = [x for x in attributes_groups_russian_json if x['id'] == russian_attribute['attributeGroup']]
#          logger.wtil("Group. : "+str(a_group))
          group_name = a_group[0]['name'] if len(a_group) > 0 else "UNKNOWN"
          russian_value = attribute_name
          russian_name  = group_name

          full_payload.update({'russian_name_'+str(variation_counter) : russian_name }) 
          full_payload.update({'russian_value_'+str(variation_counter) : russian_value }) 

          full_payload.update({'stock_info_'+str(variation_counter) : variation_stock_info }) 
          full_payload.update({'variation_price_'+str(variation_counter) : wholesale_price }) 

       variation_counter = variation_counter + 1

      logger.wtil("Passing: "+str(title_in_english))
      payload = {
                     'bigbuy':                            data[0],
                     'description':                       data[1],
                     'extended_description':              data[2],
                     'title':                             data[3],
                     'descriptionInEnglish':              description_in_english,
                     'titleInEnglish':                    title_in_english,
                     'stock_info':                        stock_info,
                     'brand':                             manufacturer,
                     'supplier':                          "bigb",
                     'english_category' :                 categoryEn,
                     'has_variations':                    has_variations,
                     'number_of_variations':              number_of_variations,
                     'sku':                               data[4],
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
     
      full_payload.update(payload) 
      r = requests.post(add_product_endpoint, data=full_payload)
      logger.wtil(str(r.content))
     
#      logger.wtil(str(pprint.pformat(full_payload)))

      logger.wtil(str(r.content))
      number_of_updated_products = number_of_updated_products + 1

logger.wtil("Number of updated products: "+str(number_of_updated_products))
