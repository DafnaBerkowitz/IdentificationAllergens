from kivy.uix import dropdown
from kivy.uix.dropdown import DropDown


from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.camera import Camera
import cv2
from kivy.properties import BooleanProperty
from kivymd.theming import ThemeManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem, MDList, OneLineIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
from kivy.uix.scrollview import ScrollView
from plyer import filechooser
import codeProject

tops=''
IallergicEng=['Gluten','Milk','Peanuts','Soy','Tuna','Eggs','Fish','Nuts','Tonsils']
class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Custom list item.'''
    icon = StringProperty("android")
class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''
    def on_active(self, rcb, value):

            self.data = value

class MenuScreen(Screen):
   pass









class UploadScreen(Screen):
    cameraActive = BooleanProperty(False)
    capture = cv2.VideoCapture()

    def start_camera(self):

        if not self.cameraActive:
            self.ids.camera_button.text = 'Stop Camera'
            self.image = self.ids.my_image
            self.capture = cv2.VideoCapture(0)
            if self.capture.isOpened():
                self.cameraActive = True
                Clock.schedule_interval(self.update, 1.0 / 10.0)
            else:
                print('Cannot Open the Camera at index 0')
        else:
            self.cameraActive = False
            self.ids.camera_button.text = 'Start Camera'
            if self.capture.isOpened():
                ret,frame = self.capture.read()
                cv2.imwrite('frame.jpg', frame)
                self.cameraActive = False
                self.ids.my_image.source ='frame.jpg'
                self.capture.release()


        return self.capture

    def on_upload_back(self):
        self.cameraActive = False
        self.ids.camera_button.text = 'Start Camera'
        if self.capture.isOpened():
            ret, frame = self.capture.read()
            cv2.imwrite('frame.jpg', frame)
            image = cv2.imread(frame.jpg)
            self.ids.my_image = image
            self.capture.release()

        self.manager.current = 'allerg'

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.image.texture = image_texture
            self.ids.my_image = self.image

    def upload_file(self):

        path = filechooser.open_file(title="Pick a CSV file..")
        pathstr=str(path)
        pathstr = pathstr.replace('\\\\', "/")
        pathstr = pathstr.replace("[\'", "")
        pathstr = pathstr.replace("\']", "")
        self.ids.my_image.source=pathstr

class Lang(Screen):
    dropdown = DropDown()
    def  on_enter(self, *args):

        global dropdown
        lna = ["English", "Spanish", "Russian", "French"]

        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "flag-outline",
                "height":dp(56),
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_item(x),
            }  for i in lna]

        dropdown = MDDropdownMenu(
            caller=self.ids.field,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )
        dropdown.open()



    def set_item(self, text__item):
            self.ids.field.text = text__item
            dropdown.dismiss()






    def startProcess(self):
      lang=self.ids.field.text
      allerg=AllergScreen.save_checked(self.manager.screens[2])
      path= self.manager.screens[1].ids.my_image.source
      str=codeProject.try3(allerg,path,lang)
    


      self.ids.ansLabel.text=str




class IconListItem(OneLineIconListItem):
    icon = StringProperty()
class AllergScreen(Screen):
    def on_enter(self, *args):

        x=len(self.ids.scroll.children)
        if (x== 0):
         icons = list(md_icons.keys())

         self.ids.scroll.add_widget(ListItemWithCheckbox(text=f"Gluten" , icon="bread-slice"))
         self.ids.scroll.add_widget( ListItemWithCheckbox(text=f"Milk", icon="cow"))
         self.ids.scroll.add_widget(ListItemWithCheckbox(text=f"Peanuts", icon="peanut"))
         self.ids.scroll.add_widget(ListItemWithCheckbox(text=f"Soy", icon="soy-sauce"))
         self.ids.scroll.add_widget(ListItemWithCheckbox(text=f"Tuna", icon="fish"))
         self.ids.scroll.add_widget(ListItemWithCheckbox(text=f"Eggs", icon="egg"))
         self.ids.scroll.add_widget(ListItemWithCheckbox(text=f"Fish", icon="fish"))
         self.ids.scroll.add_widget(ListItemWithCheckbox(text=f"Nuts", icon="nut"))
         self.ids.scroll.add_widget(ListItemWithCheckbox(text=f"Tonsils", icon="nut"))


    def save_checked(self):

        allergList=[]
        mdlist = self.ids.scroll  # get reference to the MDList
        for wid in mdlist.children:
            if isinstance(wid, ListItemWithCheckbox):  # only interested in the ListItemWithCheckboxes
                cb = wid.ids.cb  # use the id defined in kv
                if cb.active:  # only print selected items
                    allergList.append(IallergicEng.index(wid.text))
        print(allergList)
        return allergList
class DemoApp(MDApp):
    
    def build(self):


        kv = Builder.load_file("template.kv")
        return kv






if __name__ == "__main__":
    DemoApp().run()