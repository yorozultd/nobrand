import argparse 
import xml.etree.ElementTree as ET
import requests
import numpy 
try : 
    dictdata = numpy.load("stockDictionary.npy",allow_pickle=True)
except :
    if args.downloadStock or args.syncDictionary :
        pass
    else:
        print("Try using python3 graffati.py -ds to download the stock file with dictionary ")
        exit();
with open('./outputdata.txt','w') as f : 
    f.write("Products     \n")
def main():
    parser = argparse.ArgumentParser(description='Python Script to post and download data ')
    parser.add_argument('-s','--senddata',action='store_true',help='To send the post requests to the server')
    parser.add_argument('-d','--download',action='store_true',help='To download the xml data ')
    parser.add_argument('-sd','--syncdictionary',action='store_true',help='To create a dictionary file for the stock info ')
    parser.add_argument('-ds','--downloadStock',action='store_true',help='To create a dictionary file for the stock info ')

    args = parser.parse_args()
    working = 0
    try: 
        dictdata = numpy.load("stockDictionary.npy",allow_pickle=True)
    except :
        if not args.syncdictionary : 
            print("Try using python graffati.py -sd to create the dictionary file for stock info")
            exit();
    if args.syncdictionary : 
        syncDictionary()
    if args.senddata : 
        tree= ET.parse('./graffati.xml')
        root= tree.getroot();
        products = root.findall('Product')
        for product in products  : 
            sku = product.find("Product_id").text
            category = product.find("Product_SubCategory").text
            image_1 = product.find("Product_Image_1").text
            image_2 = product.find("Product_Image_2").text
            image_3 = product.find("Product_Image_3").text
            color = product.find("Product_Colour").text
            product_title = product.find("Product_Name").text
            small_description = product.find("Product_Description").text.split("<br>")[0]+"]]"
            get_extended_description = product.find("Product_Description").text
            novat_price = product.find("Product_Price_Special").text
            suggested_price = product.find("Product_Price_Special").text
            street_price = product.find("Product_Price").text
            gender = product.find("Product_MainCategory").text
            brand = product.find("Product_Manufacturer").text
            if int(novat_price) >40 and int(novat_price) < 350 : 
                send(small_description,get_extended_description,product_title,sku,image_1,category,'style' ,color,gender,image_2,image_3,street_price,suggested_price,novat_price,brand)
                working+=1
                print('#')
            if(working == 3 ): 
                break
    if args.download : 
        sync()
    if args.downloadStock : 
        syncstock();
def send(small_description,get_extended_description,product_title,sku,image_1,category,style,colour,gender,image_2,image_3,street_price,suggested_price,novat_price,brand):
    add_product_endpoint = "http://no1brand.ru/add-product/"
    # ! PRINTING THE PAYLOAD 
    try : 
        si= dictdata.item().get(sku)
    except :
        si="N/A"
        print(sku)
    print(si)
    
    payload = {
              'stock_info' :              1,
              'bigbuy':                   0,
              'description':              get_extended_description.replace("[","").replace("]",""),#small_description.replace("[","").replace("]",""),
              'extended_description':     '',
              'title':                    product_title.replace("[","").replace("]",""),
              'sku':                      'GR-'+sku,
              'image_1':                  image_1,
              'category':                 category,
              'style':                    "NONE",#style,
              'colour':                   colour,
              'gender':                   gender,
              'image_2':                  image_2,
              'image_3':                  image_3,
              'street_price':             street_price,
              'suggested_price':          suggested_price,
              'novat_price':              novat_price,
              'supplier'  :               'griffati',
              'brand'  :                    brand,
              'stock_info' :                si,
             }
    #print(payload)
    res=requests.post(add_product_endpoint, data=payload)
    #print(res.content)
    with open("outputdata.txt",'a') as f :
        f.write(str(res.content)+"\n")

    


def sync():
    print("Downloading .......  ")
    r=requests.get("http://cdn-dropship.griffati.com/xmlExport.py?gui=0&datatype=prod&go=1&token=567504&apikey=hhhy-o90i-lltr-5cca&lg=ru")
    #r=requests.get("http://cdn-dropship.griffati.com/xmlExport.py?gui=0&datatype=prod&go=1&token=567504&apikey=hhhy-o90i-lltr-5cca&lg=ru&fbclid=IwAR2ItKHajHL4P8xyU8lhlks97Trj7phjCqv_saaZ63ZnG14FTgZGs_diHjQ")
    with open("graffati.xml",'wb') as f:  
        f.write(r.content) 
def syncstock():
    r=requests.get("http://cdn-dropship.griffati.com/xmlExport.py?gui=0&datatype=attr&go=1&token=567504&apikey=hhhy-o90i-lltr-5cca&lg=ru")
    with open("stock.xml",'wb') as f:  
        f.write(r.content) 
    syncDictionary();
def syncDictionary():
    tree= ET.parse('./stock.xml')
    try: 
        pass
    except :
        print("Try using python graffati.py -ds to download the stock.xml file ")
        exit();
    root=tree.getroot()
    models= root.findall('Model')
    dictionary =  {}
    for model in models :
        dictionary[model.find('parent_id').text]=model.find('availability').text
    numpy.save('stockDictionary',dictionary)
if __name__ == "__main__":
    main()



#https://www.no1brand.ru/pr/N1B-11ED9FB
