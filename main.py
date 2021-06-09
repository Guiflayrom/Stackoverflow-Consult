from stack import trat_code, get_questions_link,get_questions_text,get_answer
from fbgraph import FbConection, PageController
from datetime import datetime
from time import sleep

access_token = "" #Your Acess Token
conection = FbConection(access_token)
stackao = PageController(conection)

today = datetime.today()
text_pub = f"""
post aberto para perguntas! ({today.day}/{today.month}/{today.year})

comente qual é a sua pergunta e o nosso robô irá te responder com base no stackoverflow :D
""".title()

try:
    id_pub = stackao.insert_pub_text(text_pub)
except:
    id_pub = stackao.insert_pub_text(text_pub + "1")
comments = []

article_number = None
article_code = "#$%AR"
while True:
    comments_json, stts = stackao.get_comment(id_pub['id'])
    if stts == 200:
        for data in comments_json['data']: 
            if data not in comments: 
                comments.append(data)
                
                message_comment = data['message']
                id_comment = data['id']
                
                article_number, question = trat_code(article_code,message_comment)
                question = question.replace(" ", "+").lower()
                
                topic = get_questions_link(question,article_number)
                
                if not topic:
                    text_answer = "Não conseguimos achar nada relacionado."
                    stackao.insert_comment(id_comment,text_answer)
                else:
                    output_question = get_questions_text(topic['href'])
                    output_answer = get_answer(topic['href'])
                    
                    text_answer = f'====================\n{output_question}\n====================\n{output_answer}\n===================='
                    _,ret = stackao.insert_comment(id_comment,text_answer)
                    if ret != 200:
                        text_answer = "O artigo selecionado ultrapassa do limite de caracteres, tente novamente com outro."
                        stackao.insert_comment(id_comment,text_answer)
    else:
        print("Publicação Não Encontrada.")
        break
    
    sleep(5)
    