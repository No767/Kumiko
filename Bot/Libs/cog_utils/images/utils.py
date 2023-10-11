from io import BytesIO
from typing import Union

import discord
from PIL import Image, ImageChops, ImageDraw, ImageOps


async def obtain_avatar_bytes(user: Union[discord.User, discord.Member]) -> bytes:
    avatar = user.display_avatar
    return await avatar.read()


def process_image(avatar_bytes: bytes, colour: tuple[int]) -> BytesIO:
    with Image.open(BytesIO(avatar_bytes)) as im:

        # this creates a new image the same size as the user's avatar, with the
        # background colour being the user's colour.
        with Image.new("RGB", im.size, colour) as background:

            # this ensures that the user's avatar lacks an alpha channel, as we're
            # going to be substituting our own here.
            rgb_avatar = im.convert("RGB")

            # this is the mask image we will be using to create the circle cutout
            # effect on the avatar.
            with Image.new("L", im.size, 0) as mask:

                # ImageDraw lets us draw on the image, in this instance, we will be
                # using it to draw a white circle on the mask image.
                mask_draw = ImageDraw.Draw(mask)

                # draw the white circle from 0, 0 to the bottom right corner of the image
                mask_draw.ellipse([(0, 0), im.size], fill=255)

                # paste the alpha-less avatar on the background using the new circle mask
                # we just created.
                background.paste(rgb_avatar, (0, 0), mask=mask)

            # prepare the stream to save this image into
            final_buffer = BytesIO()

            # save into the stream, using png format.
            background.save(final_buffer, "png")

        # seek back to the start of the stream
        final_buffer.seek(0)

        return final_buffer


def process_circle_image(image_bytes: bytes):
    with Image.open(BytesIO(image_bytes)) as im:
        im = im.convert("RGBA")
        # get any current transparent values
        alpha = im.split()[-1]

        # create circle mask
        mask = Image.new("L", im.size)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, mask.width - 1, mask.height - 1), fill=255)
        # combine the masks
        mask = ImageChops.darker(mask, alpha)
        # put the transparency back to original image
        im.putalpha(mask)
        # use im for stuff

        border = ImageOps.expand(im, border=10, fill=(223, 196, 255))

        final = BytesIO()
        border.save(final, "png")
        final.seek(0)
        return final
