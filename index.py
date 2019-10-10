import argparse 
import xml.etree.ElementTree as ET
import requests
def main():
    parser = argparse.ArgumentParser(description='Python Script to post and sync data ')
    parser.add_argument('-s','--senddata',action='store_true',help='To send the post requests to the server')
    parser.add_argument('-u','--sync',action='store_true',help='To sync the xml data ')
    args = parser.parse_args()
    print(args.senddata)
    print(args.sync)
    if args.senddata : 
        tree= ET.parse('./file.xml')
        root= tree.getroot();
        products = root.findall('Product')
        print(products)
        for product in products  : 
            print(product)
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
            send(small_description,get_extended_description,product_title,sku,image_1,category,'style' ,color,gender,image_2,image_3,street_price,suggested_price,novat_price)
            break
    if args.sync : 
        sync()

def send(small_description,get_extended_description,product_title,sku,image_1,category,style,colour,gender,image_2,image_3,street_price,suggested_price,novat_price):
    add_product_endpoint = "http://no1brand.ru/add-product/"
    # ! PRINTING THE PAYLOAD 
    print([small_description,get_extended_description,product_title,sku,image_1,category,style,colour,gender,image_2,image_3,street_price,suggested_price,novat_price])
    payload = {
              'bigbuy':                   1,
              'description':              small_description,
              'extended_description':     get_extended_description,
              'title':                    product_title,
              'sku':                      'GR-'+sku,
              'image_1':                  image_1,
              'category':                 category,
              'style':                    style,
              'colour':                   colour,
              'gender':                   gender,
              'image_2':                  image_2,
              'image_3':                  image_3,
              'street_price':             street_price,
              'suggested_price':          suggested_price,
              'novat_price':              novat_price
             }
    res=requests.post(add_product_endpoint, data=payload)
    print(res.content)

    


def sync():
    print("Syncing .......  ")
    r=requests.get("http://cdn-dropship.griffati.com/xmlExport.py?gui=0&datatype=prod&go=1&token=567504&apikey=hhhy-o90i-lltr-5cca&lg=en&fbclid=IwAR2ItKHajHL4P8xyU8lhlks97Trj7phjCqv_saaZ63ZnG14FTgZGs_diHjQ")
    with open("file.xml",'wb') as f:  
        f.write(r.content) 

if __name__ == "__main__":
    main()