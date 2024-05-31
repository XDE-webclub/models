import reflex as rx
import base64
import io
from PIL import Image
import requests
import json

API_KEY = "***"
SECRET_KEY = "***"

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY,
    }
    return str(requests.post(url, params=params).json().get("access_token"))


def get_aiimg(prompt=None, style="Cinematic", size="768x768"):

    url = (
        "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/text2image/sd_xl?access_token="
        + get_access_token()
    )

    payload = json.dumps(
        {
            "prompt": str(prompt),
            "size": size,
            "n": 1,
            "steps": 20,
            "sampler_index": "Euler a",
            "style": style,
        }
    )
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    data = response.text

    base64_str = json.loads(data)["data"][0]["b64_image"]

    image_data = base64.b64decode(base64_str)

    image_data = io.BytesIO(image_data)

    return Image.open(image_data)

class ImgState(rx.State):
    image: Image.Image = None
    image_processing: bool = False
    image_made: bool = False

    def prompt_submit(self, form_data: dict):
        self.image_processing = True
        self.image_made = False
        yield
        self.image = get_aiimg(
            form_data["prompt"], form_data["style"], form_data["size"]
        )
        self.image_processing = False
        self.image_made = True
        yield


def aiimg() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.form(
                rx.hstack(
                    rx.input(
                        placeholder="提示词",
                        name="prompt",
                    ),
                    rx.input(
                        placeholder="风格",
                        name="style",
                    ),
                    rx.input(
                        placeholder="尺寸",
                        name="size",
                    ),
                    rx.button(
                        "生成", type="submit", # 
                        disabled=ImgState.image_processing
                        # disabled=True
                    ),
                ),
                on_submit=ImgState.prompt_submit,
                reset_on_submit=False,
            ),
            rx.divider(),
            rx.center(
                rx.cond(
                    ImgState.image_processing,
                    # True,
                    rx.chakra.circular_progress(is_indeterminate=True), # 转圈（1）

                    # 2
                    rx.cond(
                        ImgState.image_made,
                        rx.image(src=ImgState.image, width="200px", height="auto"),
                        # 留空
                    ),
                ),
                width="100%",
            ),
        ),
    )
