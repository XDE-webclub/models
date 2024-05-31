from rxconfig import config
import reflex as rx
from my_app_name.index_page import index
from my_app_name.knn_page import knn
from my_app_name.aiimg_page import aiimg
from my_app_name.knntrain_page import knntrain
from my_app_name.chat_page import chats

app = rx.App()
app.add_page(index, route="/")
app.add_page(knn, route="/knn")
app.add_page(aiimg, route="/aiimg")
app.add_page(knntrain, route="/knntrain")
app.add_page(chats,route="/chat")
