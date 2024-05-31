import reflex as rx


def links(text, href):
    return rx.center(
        rx.link(text, href=href),
        border_radius="15px",
        border_width="thick",
        width="100%",
    )

def index() -> rx.Component:
    return rx.center(
        (
            rx.vstack(
                rx.heading("欢迎使用AI模型库!",padding="10px"),
                links("鸢尾花模型识别", href="/knn"),
                links("文生图模型体验", href="/aiimg"),
                links("实时训练的分类器", href="/knntrain"),
                links("连续对话模型体验", href="/chat"),
            ),
        ),
    )
