from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

Window.clearcolor = (0.96, 0.96, 0.96, 1)

class GolButton(Button):
    def __init__(self, bg_color, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)
        self.bg_color = bg_color
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=(80,))
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.rect.radius = (min(self.size) / 2,)

class ModernCalculator(App):
    def build(self):
        main_layout = BoxLayout(orientation="vertical", padding=15, spacing=10)
        display_box = BoxLayout(orientation="vertical", size_hint=(1, 0.32), padding=(10, 10))
        self.expr_label = Label(text="", font_size="44sp", bold=True, color=(0.1, 0.1, 0.1, 1), halign="right", valign="bottom")
        self.expr_label.bind(size=self.expr_label.setter("text_size"))
        self.preview_label = Label(text="", font_size="28sp", color=(0.45, 0.45, 0.45, 1), halign="right", valign="top")
        self.preview_label.bind(size=self.preview_label.setter("text_size"))
        display_box.add_widget(self.expr_label)
        display_box.add_widget(self.preview_label)
        main_layout.add_widget(display_box)
        buttons = [
            ["AC", "%", "[×]", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["00", "0", ".", "="]
        ]
        grid = GridLayout(cols=4, spacing=12, size_hint=(1, 0.68))
        for row in buttons:
            for b in row:
                if b == "=":
                    bg_rang, txt_rang = (1, 0.45, 0, 1), (1, 1, 1, 1)
                elif b in ["AC", "%", "[×]", "÷", "×", "-", "+"]:
                    bg_rang, txt_rang = (0.88, 0.88, 0.88, 1), (0.1, 0.1, 0.1, 1)
                else:
                    bg_rang, txt_rang = (0.91, 0.91, 0.91, 1), (0.1, 0.1, 0.1, 1)
                btn = GolButton(bg_color=bg_rang, text=b, color=txt_rang, font_size="26sp", bold=True)
                btn.bind(on_press=self.button_daba)
                grid.add_widget(btn)
        main_layout.add_widget(grid)
        return main_layout

    def update_preview(self):
        abhi = self.expr_label.text
        if abhi == "":
            self.preview_label.text = ""
            return
        try:
            clean = abhi.rstrip("÷×-+%.")
            if any(op in clean for op in ["÷", "×", "-", "+", "%"]):
                hisab = clean.replace("×", "*").replace("÷", "/").replace("%", "/100")
                res = round(eval(hisab), 6)
                if res == int(res):
                    res = int(res)
                self.preview_label.text = str(res)
            else:
                self.preview_label.text = ""
        except:
            self.preview_label.text = ""

    def button_daba(self, instance):
        text = instance.text
        abhi = self.expr_label.text
        if text == "AC":
            self.expr_label.text = ""
            self.preview_label.text = ""
        elif text == "[×]":
            self.expr_label.text = abhi[:-1]
            self.update_preview()
        elif text == "=":
            if self.preview_label.text != "":
                self.expr_label.text = self.preview_label.text
                self.preview_label.text = ""
        elif text in ["÷", "×", "+", "%"] and abhi == "":
            pass
        else:
            self.expr_label.text = text if abhi == "Error" else abhi + text
            self.update_preview()

ModernCalculator().run()
      
