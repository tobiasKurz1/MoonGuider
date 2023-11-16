from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

import cv2
import sys



class TouchableImage(Image):
    def __init__(self, image_cv2, image_number, **kwargs):
        super(TouchableImage, self).__init__(**kwargs)
        self.texture = self.create_texture(image_cv2)
        self.image_number = image_number

        # Add a red square in the top-right corner
        with self.canvas:
            Color(1, 0, 0)  # Set color to red
            self.square = Rectangle(pos=(self.width - 50, self.height - 50), size=(50, 50))

    def create_texture(self, image_cv2):
        buf1 = cv2.flip(image_cv2, 0)
        buf = buf1.tobytes()
        texture = self.texture
        if not texture:
            texture = self.texture = Texture.create(size=(image_cv2.shape[1], image_cv2.shape[0]))
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        return texture

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.is_on_red_square(touch):
                print("Stopping")
                App.get_running_app().stop()  # Terminate the application
            else:
                print(f"Clicked on image {self.image_number}")

    def is_on_red_square(self, touch):
        red_square_pos = self.to_window(self.width - 50, self.height - 50)
        red_square_size = (50, 50)
        return (
            red_square_pos[0] <= touch.pos[0] <= (red_square_pos[0] + red_square_size[0]) and
            red_square_pos[1] <= touch.pos[1] <= (red_square_pos[1] + red_square_size[1])
        )


class CustomApp(App):
    def build(self):
        layout = GridLayout(cols=2)
        for i in range(4):
            touchable_image = TouchableImage(image_cv2=images_cv2[i], image_number=i + 1)
            layout.add_widget(touchable_image)
        return layout

    def on_stop(self):
        sys.exit()

# Example usage:
image1 = cv2.imread("Output/1_Grey.jpg")  # Replace with the actual path
image2 = cv2.imread("Output/2_Threshold.jpg")  # Replace with the actual path
image3 = cv2.imread("Output/3_Blur.jpg")  # Replace with the actual path
image4 = cv2.imread("Output/Final.jpg")  # Replace with the actual path

images_cv2 = [image1, image2, image3, image4]

if __name__ == '__main__':
    CustomApp().run()

