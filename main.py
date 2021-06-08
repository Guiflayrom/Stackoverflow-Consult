from stack import trat_code, get_questions_link,get_questions_text,get_answer

while True:
            
    question = input("Pesquisar: ")
    if question in ["break","stop","quit","exit"]: break
    # question = "selenium [python]"
    
    if question != "" and len(question) > 5:
            
        article_number = None
        article_code = "#$%AR"
        
        article_number, question = trat_code(article_code,question)
            
        question = question.replace(" ", "+").lower()
    
        topic = get_questions_link(question,article_number)
        if topic: 
            print(get_questions_text(topic['href']))
            print("\n# =============================================================================\n")
            print(get_answer(topic['href']))
            