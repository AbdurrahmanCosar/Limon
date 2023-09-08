"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""
from discord import Embed
from discord.ext import commands
from cogs.utils.database.admin_db import get_collection
from cogs.utils.downloader import ImageDownloader

class WriteToDatabase:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @property
    async def image_dict(self) -> dict:
        data, _ = await get_collection(self.bot)
        return data['images']

    async def load_image(self, name:str, url: str) -> None:
        data, collection = await get_collection(self.bot)
        data["images"].update({name:url})
        await collection.replace_one({"id": "admin"}, data)


    async def remove_image(self, name: str) -> None:
        data, collection = await get_collection(self.bot)
        data['images'].pop(name)
        await collection.replace_one({"id": "admin"}, data)


class ImagesCommands(commands.Cog, WriteToDatabase):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @commands.group(invoke_without_command=True, hidden=True)
    @commands.is_owner()
    async def image(self, ctx):
        if ctx.invoked_subcommand is None:
            process_type = ("`image load`", "`image remove`", "`image show`", "`image download`")
            process_type = '\n'.join(process_type)
            await ctx.send(f'Geçersiz komut kullanımı! Hangi işlemi yapmak istiyorsunuz...\n{process_type}')

    @image.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, name:str, url: str):
        if not name or not url:
            command_help = "image load imageName imageURL"
            return await ctx.send(content = f"Eksik argüman girdiniz. Doğru kullanım: `{command_help}`")

        if name in await self.image_dict:
            return await ctx.send(content = "Bu isimde bir görsel zaten mevcut.")

        embed = Embed(description = f"[{name}]({url}) yüklendi!")
        await self.load_image(name, url)
        await ctx.send(embed = embed)

    @image.command(hidden=True)
    @commands.is_owner()
    async def remove(self, ctx, name:str):
        if not name:
            command_help = "image remove imageName"
            return await ctx.send(content = f"Eksik argüman girdiniz. Doğru kullanım: `{command_help}`")

        if name not in await self.image_dict:
            return await ctx.send(content = "Bu isimde bir görsel __bulunmuyor!__")

        await self.remove_image(name)
        await ctx.send(content = "Görsel silindi!")

    @image.command(hidden=True)
    @commands.is_owner()
    async def show(self, ctx):
        image_dict = await self.image_dict
        images = [f"[{key}]({value})" for key, value in image_dict.items()]
        images = "\n".join(images) if len(images) > 0 else "Hiç görsel bulunmuyor!"
        embed = Embed(description = images)
        await ctx.send(embed = embed)

    @image.command(hidden=True)
    @commands.is_owner()
    async def download(self, ctx):
        msg = await ctx.send(content = "İndirme başlatılıyor..")
        image_dict = await self.image_dict
        downloader = await ImageDownloader(image_dict).start_download()

        if downloader is True:
            return await msg.edit(content = f"İndirme tamamlandı! `({len(image_dict)})`")
        await msg.edit(content = "Bir hata oluştu!")

async def setup(bot: commands.Bot):
    await bot.add_cog(ImagesCommands(bot))
