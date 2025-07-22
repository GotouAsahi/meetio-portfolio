from django.core import mail
from django.template.loader import render_to_string

# メール送信用メソッド
def send_mail(email):
    plaintext = render_to_string("./template/template.txt")
    html_text = render_to_string("./template/template.html")
    
    mail.send_mail(
        title = "たいとるだよ",
        message = "本文だよ",
        from_email = "送信元だよ",
        recipient_list=[email], # わからないよ
        html_message=html_text  # HTML形式だよ
    )