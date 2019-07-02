from vk_api.longpoll import  VkLongPoll,VkEventType
import vk_api

import text as tex



vk = vk_api.VkApi(token=tex.token)
ses_api= vk.get_api()
longpoll= VkLongPoll(vk)
def message_send(user_id,otv):
	ses_api.messages.send(user_id=user_id,message=otv,random_id=0)	





while True:
	for event in longpoll.listen():
		if event.type == VkEventType.MESSAGE_NEW:
				response = event.text.lower()
				user_id=int(event.user_id)
				if event.from_user and not (event.from_me):
					
					if response =='hello' or response=='привет':
						us=str(ses_api.users.get(user_id=user_id)[0]['first_name'])
						otv='Привет , '+us + '. Мы тебя ждали'
						message_send(user_id,otv)

					if response =='информация об авторе':
						otv=' автор Kiritodyat \n ССЫЛКИ \n Vk: https://vk.com/mr_hacher \n inst : ros.mal_'
						
						message_send(user_id,otv)
					if response =="начать":
						otv='возможности: \n -hello или привет \n -информация об авторе \n -ярик( ярослав или админ) красавчик  '
						
						message_send(user_id,otv)
					if response =='ярик красавчик' or response=='ярослав красавчик' or response=='админ красавчик':
						otv='точно красавчик '
						
						message_send(user_id,otv)
					if response =='а кто илья?':
						otv='нуб'
						
						message_send(user_id,otv)
					
