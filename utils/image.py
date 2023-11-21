import base64


def img_to_bytes(img_path):
    img_bytes = open(img_path, "rb").read()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
def img_to_html(img_path):
    img_html = "<img src='data:image/jpeg;base64,{}' display='inline-block' width='40px' height='30px' class='img-fluid'>".format(
      img_to_bytes(img_path)
    )
    return img_html

