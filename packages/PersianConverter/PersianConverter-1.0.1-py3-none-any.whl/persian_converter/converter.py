import arabic_reshaper
from bidi.algorithm import get_display

def fprint(text='سلام من کمیلیان هستم'):
    persian_text = text
    reshaped_text = arabic_reshaper.reshape(persian_text)
    farsi_text = get_display(reshaped_text)
    return farsi_text

# How to Usage 
print(fprint('این یک تست است'))
print(fprint('this is test'))