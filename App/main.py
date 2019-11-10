from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.video import Video
from database import DataBase
###############################################################################################

class Logado(Screen):
    def btn(self):
        notification()

class TelaDeLog (Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def ValidaLog(self):
        if db.validate(self.email.text, self.password.text):
            Logado.current = self.email.text
            self.reset()
            sm.current = "logado"
        else:
            invalidLogin()

    def criaLog(self):
        self.reset()
        sm.current = "cria"

    def reset(self):
        self.email.text = ""
        self.password.text = ""

class NovaConta(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def salvar(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "tela"
            else:
                invalidForm()
        else:
            invalidForm()

    def voltar(self):
        self.reset()
        sm.current = "tela"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""
    
class AtendeChamada(Screen): #tela da chamada#
    def liberar(self):
        abrePortaum()
        sm.current = "logado"
    def negar(self):
        sm.current = "logado"

class Chamada(FloatLayout): #popup da chamada#
    pass

class WindowManager(ScreenManager):
    pass

##############################################################################################

kv = Builder.load_file("my.kv")
db = DataBase("users.txt")
sm = WindowManager()

screens = [TelaDeLog(name="tela"),Logado(name="logado"),NovaConta(name="cria"),AtendeChamada(name="atende")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "tela"

###############################################################################################

def abrePortaum():
    #precisa definir a conexão#
    pop = Popup(title='Visitante Liberado',
                content=Label(text='Voce autorizou a entrada'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def notification():
    show = Chamada()
    popupWindow = Popup(title="Alguem na Portaria", content=show,size_hint=(None,None),size=(400,400))
    popupWindow.open()

def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()

################################################################################################
    
class MyMainApp(App):
    def build(self):
        return sm

    

if __name__ == "__main__":
    MyMainApp().run()
