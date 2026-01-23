# EXECUTAR REQUIREMTNS.TXT
# pip install -r requirements.txt

#Criado Banco de Dados
flask shell

db.create_all()
exit()



>>> db.drop_all()
>>> db.create_all()