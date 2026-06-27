from database import criar_tabelas
from interface.login import Login

criar_tabelas()

app = Login()
app.mainloop()