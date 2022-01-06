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


IallergicEng=['Gluten','Milk','Peanuts','Soy','Tuna','Eggs','Fish','Nuts','Tonsils']

'''
for AllergScreen
'''
class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Custom list item.'''
    icon = StringProperty("android")

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''
    def on_active(self, rcb, value):

            self.data = value
        #for using icons
class IconListItem(OneLineIconListItem):
    icon = StringProperty()


'''
Application opening screen
'''
class MenuScreen(Screen):
   pass


'''
Screen for selecting the desired allergens for testing
'''
class AllergScreen(Screen):
    '''
    initialization
    '''
    def on_enter(self, *args):

        x = len(self.ids.scroll.children)
        if (x == 0):#In order not to reboot the list every time you return to the screen
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


      # return a list of all the items that marked

    def save_checked(self):

        allergList=[]
        mdlist = self.ids.scroll  # get reference to the MDList
        for item in mdlist.children:
            if isinstance(item, ListItemWithCheckbox):  # only interested in the ListItemWithCheckboxes- isinstance cheking if item is ListItemWithCheckbox
                cb = item.ids.cb  # use the id defined in kv
                if cb.active:  # only print selected items
                    allergList.append(IallergicEng.index(item.text))# insert to the list the index of the item 
        
        return allergList




'''
 screen to upload/take a product picture 
'''
class UploadScreen(Screen):
    cameraActive = BooleanProperty(False)
    capture = cv2.VideoCapture()

    def start_camera(self):
            # if the camera turn off
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
                #take the last frame and save
                ret,frame = self.capture.read()
                good=cv2.imwrite('frame1.jpg', frame)
                self.cameraActive = False
                # set on the screen
                self.capture.release()
                self.ids.my_image.source = 'frame1.jpg'


                if good:
                  print ("good")



        return self.capture

    def on_upload_back(self):
        self.cameraActive = False
        self.ids.camera_button.text = 'Start Camera'

        self.ids.my_image.source="frame1.jpg"
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
        #Arranging the path
        pathstr = pathstr.replace('\\\\', "/")
        pathstr = pathstr.replace("[\'", "")
        pathstr = pathstr.replace("\']", "")
        self.ids.my_image.source=pathstr

#to pick a language and send all the information to proccess
class Lang(Screen):
    dropdown = DropDown()
    #initialization
    def  on_enter(self, *args):
        self.ids.ansLabel.text = ""  # Receiving a final answer
        Lang.hide_widget(self.ids.field, False)
        Lang.hide_widget(self.ids.startProcess, False)

        global dropdown
        lna = ["English", "Spanish", "Russian", "French"]

        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "flag-outline",
                "font_name": "Sticky Notes.ttf",
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

    # for Hide Widget accroding our need
    def hide_widget(wid, dohide=True):
        if hasattr(wid, 'saved_attrs'):
            if not dohide:
                wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
                del wid.saved_attrs
        elif dohide:
            wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True

    # Organize all the information accumulated from the user throughout the process and send for processing
    def startProcess(self):
      lang=self.ids.field.text#language
      allerg=AllergScreen.save_checked(self.manager.screens[2])#List of allergens
      path= self.manager.screens[1].ids.my_image.source
      whynot,caneat=codeProject.Answer_processing(allerg,path,lang)#sending to processing
      strAnswer=""
      if not caneat:
           strAnswer="The product contains from your list: \n"
           strAnswer+=whynot
           strAnswer+="\n"+"           Do not eat!"
      else:
          strAnswer="This product does not contain products\n    from your list of allergens.\n       enjoy your meal!"

      self.ids.ansLabel.text=strAnswer#Receiving a final answer
      Lang.hide_widget(self.ids.field,True)
      Lang.hide_widget(self.ids.startProcess, True)
      if not caneat:
          self.ids.ansLabel.color=.54,.09,.09

      else:
          self.ids.ansLabel.color = .03, .6, .9, 1






class Identification_AllergensApp(MDApp):
    
    def build(self):
        self.icon = '2Eat.png'
        kv = Builder.load_file("template.kv")
        return kv






if __name__ == "__main__":
    Identification_AllergensApp().run()