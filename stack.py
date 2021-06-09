from bs4 import BeautifulSoup as bs
import requests
from unidecode import unidecode

def get_questions_link(question,article_number=False):
    url = 'https://pt.stackoverflow.com/search?q=' + unidecode(question)
    content = requests.get(url)
    cs = bs(content.text,features='lxml')
    divs_questions = cs.findAll("div",{'class':'question-summary search-result'})
    a_questions = []
    for i in divs_questions:
        try:
            a_questions.append(i.find("a",{'class':'question-hyperlink'}))
            
        except: continue
    
    if str(article_number).isnumeric(): 
        try:
            return a_questions[1-article_number]
        
        except: 
            # print(f'Não conseguimos achar nada relacionado à "{question}" no artigo "{article_number}"')
            return False
    else: 
        try:
            return a_questions[0]
        except: 
            # print(f'Não conseguimos achar nada relacionado à "{question}"')
            return False

def get_questions_text(url):
    if url[0] == "/": url = "https://pt.stackoverflow.com" + url

    content = requests.get(url)
    cs = bs(content.text,features="lxml")
    
    _question = cs.findAll("div",{'itemprop':'text'})
    return _question[0].text

    
def get_answer(url):
    if url[0] == "/": url = "https://pt.stackoverflow.com" + url

    content = requests.get(url)
    soup = bs(content.text,features='lxml')
    
    try:
        answer = soup.find_all('div',attrs={'class':'accepted-answer'})
        accepted_content = answer[0].find("div",{'itemprop':'text'})
        return accepted_content.text
    
    except:
        try:
            answer = soup.find_all("div",{'class':'answer'})
            accepted_content = answer[0].find("div",{'itemprop':'text'})
            return accepted_content.text
        except:
            return "Não respondida"
    

def trat_code(article_code,question):
    if article_code in question:
        for i in question.split():
            if article_code in i:
                article_number = i.replace(article_code, "")
        question = question.replace(article_code+article_number, "")
        article_number = int(article_number)
        
        return article_number,question
    else:
        return False, question