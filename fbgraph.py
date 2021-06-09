from facebook import GraphAPI as GAPI
import requests

class FbConection:
    def __init__(self,token):
        self.token = self.__set_token(token)
    
    def __validate(self,token):
        url = "https://graph.facebook.com/me?access_token=" + token
        return True if requests.get(url).status_code == 200 else False
    
    def get_token(self):
        return self.token
    
    def __set_token(self,token):
        if not self.__validate(token):
            raise ValueError("Invalid Token")
        return token
    
    def increase_token_time(self,app_id,app_secret,short_lived_token):
        return requests.get(f'https://graph.facebook.com/v2.10/oauth/access_token?grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}&fb_exchange_token={short_lived_token}').json()
        
class PageController:
    def __init__(self,conection):
        self.graph = GAPI(conection.get_token())
        self.token = conection.get_token()
        
    def insert_pub_text(self,message):
        return self.graph.put_object("me","feed",message=message)        
        
    def insert_pub_pic(self,picture,message=""):
        return self.graph.put_photo(picture, message=message)        
    
    def __get_url_comment(self,pub_id):
        return f"https://graph.facebook.com/v10.0/{pub_id}/comments?access_token={self.token}"
        
    def get_comment(self,pub_id):
        req = requests.get(self.__get_url_comment(pub_id))
        return req.json(),req.status_code

    def insert_comment(self,pub_id,message):
        payload = {'message':message}
        return requests.post(self.__get_url_comment(pub_id),data=payload).json()
    
    def delete_comment(self,pub_id):
        return requests.delete(self.__get_url_comment(pub_id)).json()

    



