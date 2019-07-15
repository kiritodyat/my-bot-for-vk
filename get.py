from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
from PIL import Image,ImageOps, ImageDraw,ImageFont
import requests
from io import BytesIO
import requests

token='27b7ab9bb881978742286fd17cd604145d22f365a8d2f8d8e6bcb149fe87cb86d4aac1e7671f1b43ad0a6'

vk = vk_api.VkApi(token=token)
ses_api= vk.get_api()
longpoll= VkBotLongPoll(vk,182171896)
# создание круглой маски
group_id =  182171896


upload = vk_api.VkUpload(ses_api)
# обрезка фотографии по координатам 

       
def minifoto(user_id) :
    global name_surname 

    users_id=user_id
    a=ses_api.users.get(user_id=user_id,fields='crop_photo') # парс всех данных
   
    b=a[0]['crop_photo']['crop']# выбор  данных координат обрезки фотографии
    name=a[0]['first_name']# имя
    surname=a[0]['last_name']# фамилия 
    name_surname=str(name +'\n'+ surname)#имя и фамилия 

    x_1=b['x']# координаты
    x_2=b['x2']
    y_1=b['y']
    y_2=b['y2']
    url=a[0]['crop_photo']['photo']['sizes'][4]['url']# ссылка на фотографию профля 



    response = requests.get(url)
    im = Image.open(BytesIO(response.content))#отрытие фотографии
    
       
    def crop(im, s):
 
        w, h = im.size
        x1=w*x_1/100
        x2=w*x_2/100
        y1=h*y_1/100
        y2=h*y_2/100
  

        im=im.crop((x1,y1,x2,y2))
    #k = w / s[0] - h / s[1]
   #if k > 0: im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
    #elif k < 0: im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
        return im.resize(s, Image.ANTIALIAS)

    size = (150, 150)
    im = crop(im, size)
    


# маска
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + size, fill=255)

    im = im.resize(size)

    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    output.thumbnail(size, Image.ANTIALIAS)
    output.save('pic/output.png')
    
while True:
    for event in longpoll.listen():
        if event.type == VkBotEventType.GROUP_JOIN:
              
            try:
                user_id=event.obj.user_id  
                
               
                minifoto(user_id)    
               
                print(name_surname)
                output = Image.open('pic/output.png')
                bg = Image.open('pic/bg1.png')
                bg.paste(output, (455,160), output)
                draw = ImageDraw.Draw(bg)
                font = ImageFont.truetype('pic/16863.otf', 36)
                
                draw.text((450,317),name_surname, (255,255,255), font=font)
                
                bg.save('pic/result.png')

                photo = upload.photo_cover(photo='pic/result.png',group_id=group_id,crop_x=0,crop_y=0,crop_x2=1590,crop_y2=400)
               
                
            except:
                print('не робит')
                continue   
   
                 