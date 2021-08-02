from stack import trat_code, get_questions_link,get_questions_text,get_answer
from fbgraph import FbConection, PageController
from datetime import datetime
from time import sleep
import os

access_token = "" #PAGE ACESS CODE
conection = FbConection(access_token)
stackao = PageController(conection)

today = datetime.today()
text_pub = f"""
POST ABERTO PARA CONSULTA! ({today.day}/{today.month}/{today.year})
 
⚠️⚠️⚠️⚠️⚠️⚠️
⚠️⚠️⚠️⚠️⚠️⚠️

VOCÊ PODE COMENTAR:

º SUA DUVIDA 🤔
º UM ERRO QUE ESTÁ DANDO NO SEU CÓDIGO🙄

E IREMOS LHE RETORNAR O RESULTADO DE UMA CONSULTA NO STACKOVERFLOW 😃😃
""".title()

pic = open("images/hiw.jpg","rb")

try:
    id_pub = stackao.insert_pub_pic(pic,text_pub)
except:
    id_pub = stackao.insert_pub_text(text_pub + " - Sessão 2")
comments = []

article_number = None
article_code = "$AR:"
error = True
while True:
    os.system('cls' if os.name == 'nt' else 'clear')    
    while True:
        try:
            comments_json, stts = stackao.get_comment(id_pub['id'])
            if error: print("Conexão concluida com sucesso");error = False
            break
        except:
            error = True
            print("Erro de conexão, tentando novamente em 5 segundos...")   
            sleep(5)
        
    if stts == 200:
        for data in comments_json['data']: 
            if data not in comments: 
                comments.append(data)
                print(f"Comentarios respondidos: {len(comments)}")
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
                    
                    text_answer = f"""
                    =============
                    Pergunta ❔
                    =============
                    
                    {output_question}
                    
                    =============
                    Resposta ✅
                    =============
                    
                    {output_answer}
                    """
                    _,ret = stackao.insert_comment(id_comment,text_answer)
                    if ret != 200:
                        text_answer = "O artigo selecionado ultrapassa do limite de caracteres, tente novamente com outro."
                        stackao.insert_comment(id_comment,text_answer)
    else:
        print("Publicação Não Encontrada.")
        break
    
    sleep(5)
    
