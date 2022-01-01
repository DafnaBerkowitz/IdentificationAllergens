from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import codeProject
from plyer import filechooser
import CameraPic
Builder.load_file('template.kv')
IallergicEng=['Gluten','milk','peanuts','Soy','tuna','Eggs','Fish','nuts','tonsils']

class MyLayout(Widget):
    checks = []

    def checkbox_click(self, instance, value, topping):
       global tops
       if value == True:
         MyLayout.checks.append(topping)
         tops = ''
         for x in MyLayout.checks:
            tops = f'{tops} {IallergicEng[int(x)]}'
         self.ids.output_label.text = f'You Selected: {tops}'
         self.ids.endAnswer.text = ""
       else:
         MyLayout.checks.remove(topping)
         tops = ''
         for x in MyLayout.checks:
            tops = f'{tops} {IallergicEng[int(x)]}'
         self.ids.output_label.text = f'You Selected: {tops}'
         self.ids.endAnswer.text = ""


    def  say_hello(self):
        self.ids.endAnswer.text = codeProject.try3(MyLayout.checks, str(self.ids.Path.text))
    def upload_file(self):

        path = filechooser.open_file(title="Pick a CSV file..")
        self.ids.Path.text=str(path)
        print(path)
    def camera(self):
        from subprocess import Popen, PIPE
        process = Popen(['python3', 'CameraPic.py'], stdout=PIPE, stderr=PIPE)







class AwesomeApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    AwesomeApp().run()