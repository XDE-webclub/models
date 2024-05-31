import joblib
# 加载模型
knn_from_joblib = joblib.load('knn_model.pkl')
import reflex as rx

class Knn_State(rx.State):
    predicted_name: str = ""
    iris_target_names: list = ["setosa", "versicolor", "virginica"]

    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        # 将字典的值转为浮点数，放置在新的列表中
        iris_example_list = [[float(v) for v in form_data.values()]]
        # 使用模型预测
        predict = knn_from_joblib.predict(iris_example_list)
        # 将预测结果转为花的名称
        self.predicted_name = self.iris_target_names[predict[0]]


def knn() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.form(
                rx.vstack(
                    rx.hstack(
                        rx.input(
                            placeholder="花萼长度",
                            name="sepal_length",
                        ),
                        rx.input(
                            placeholder="花萼宽度",
                            name="sepal_width",
                        ),
                    ),
                    rx.hstack(
                        rx.input(
                            placeholder="花瓣长度",
                            name="petal_length",
                        ),
                        rx.input(
                            placeholder="花瓣宽度",
                            name="petal_width",
                        ),
                    ),
                    rx.button("判断", type="submit"),
                ),
                on_submit=Knn_State.handle_submit,
                reset_on_submit=True,
            ),
            rx.text(Knn_State.predicted_name),
        ),
    )

