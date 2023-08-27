from PIL import Image, ImageDraw, ImageChops
from ..constants import Assets
from io import BytesIO

class Functions:
    def user_not_found_err():
        avatar = Assets.default_avatar
        name = "User"
        return avatar, name
    
    async def open_avatar(u_avatar):
        avatar = u_avatar.replace(size=256)
        data = BytesIO(await avatar.read())
        avatar = Image.open(data).convert("RGBA")
        return avatar

    def circle(pfp, size = (215,215)):
        pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")

        bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
        mask = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill = 255)
        mask = mask.resize(pfp.size, Image.LANCZOS)
        mask = ImageChops.darker(mask, pfp.split()[-1])
        pfp.putalpha(mask)

        return pfp