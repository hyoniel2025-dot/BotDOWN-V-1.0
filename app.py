import threading,http.server,socketserver,requests,os,json,asyncio
from pathlib import Path
from pyrogram import Client,filters
from configs import api_id,api_hash,token,ia_access_key,ia_secret_key
import py7zr

bot=Client("client",api_id,api_hash,bot_token=token)

# =========================
# SPLIT + COMPRESS
# =========================
def split_file(file_path,chunk_size=99*1024*1024):
    file_path=Path(file_path)
    chunks=[]
    with open(file_path,'rb') as f:
        i=0
        while True:
            chunk=f.read(chunk_size)
            if not chunk: break
            part=file_path.parent/f"{file_path.stem}_part{i}"
            with open(part,'wb') as cf: cf.write(chunk)
            chunks.append(part)
            i+=1
    return chunks

def compress_chunk(chunk):
    chunk=Path(chunk)
    out=chunk.with_suffix(".7z")
    with py7zr.SevenZipFile(out,'w') as z:
        z.write(chunk,chunk.name)
    chunk.unlink()
    return out

def upload(file):
    file=Path(file)
    identifier=file.stem.split("_part")[0].lower()
    auth=(ia_access_key,ia_secret_key)
    requests.post(f"https://archive.org/metadata/{identifier}",auth=auth,data=json.dumps({
        "collection":"opensource","title":identifier,"mediatype":"software"
    }))
    with open(file,'rb') as f:
        r=requests.put(f"https://s3.us.archive.org/{identifier}/{file.name}",auth=auth,data=f)
    if r.status_code in [200,201]:
        url=f"https://archive.org/download/{identifier}/{file.name}"
        file.unlink()
        return url

# =========================
# START
# =========================
@bot.on_message(filters.command("start"))
async def start(_,m):
    await m.reply_text("Envíame archivo o link 📥")

# =========================
# TELEGRAM FILES
# =========================
@bot.on_message(filters.document|filters.video|filters.audio)
async def tg(_,m):
    path=await m.download()
    await m.reply_text("Procesando...")
    chunks=split_file(path)
    Path(path).unlink()
    urls=[]
    for c in chunks:
        z=compress_chunk(c)
        u=upload(z)
        if u: urls.append(u)
    await m.reply_text("✅\n"+"\n".join(urls))

# =========================
# LINKS
# =========================
@bot.on_message(filters.text)
async def link(_,m):
    url=m.text.strip()
    if url.startswith("http"):
        try:
            name=url.split("/")[-1] or "file"
            r=requests.get(url,stream=True)
            with open(name,"wb") as f:
                for c in r.iter_content(1024):
                    if c:f.write(c)
            await m.reply_text("Procesando...")
            chunks=split_file(name)
            Path(name).unlink()
            urls=[]
            for c in chunks:
                z=compress_chunk(c)
                u=upload(z)
                if u: urls.append(u)
            await m.reply_text("✅\n"+"\n".join(urls))
        except:
            await m.reply_text("Error ❌")

# =========================
# WEB
# =========================
def web():
    port=int(os.environ.get("PORT",10000))
    with socketserver.TCPServer(("",port),http.server.SimpleHTTPRequestHandler) as s:
        s.serve_forever()

# =========================
# MAIN
# =========================
async def main():
    threading.Thread(target=web,daemon=True).start()
    await bot.start()
    print("Bot iniciado")
    await asyncio.Event().wait()

if __name__=="__main__":
    asyncio.run(main())async def tg(_,m):
    path=await m.download()
    await m.reply_text("Procesando...")
    chunks=split_file(path)
    Path(path).unlink()
    urls=[]
    for c in chunks:
        z=compress_chunk(c)
        u=upload(z)
        if u: urls.append(u)
    await m.reply_text("✅\n"+"\n".join(urls))

# =========================
# LINKS
# =========================
@bot.on_message(filters.text)
async def link(_,m):
    url=m.text.strip()
    if url.startswith("http"):
        try:
            name=url.split("/")[-1] or "file"
            r=requests.get(url,stream=True)
            with open(name,"wb") as f:
                for c in r.iter_content(1024):
                    if c:f.write(c)
            await m.reply_text("Procesando...")
            chunks=split_file(name)
            Path(name).unlink()
            urls=[]
            for c in chunks:
                z=compress_chunk(c)
                u=upload(z)
                if u: urls.append(u)
            await m.reply_text("✅\n"+"\n".join(urls))
        except:
            await m.reply_text("Error ❌")

# =========================
# WEB
# =========================
def web():
    port=int(os.environ.get("PORT",10000))
    with socketserver.TCPServer(("",port),http.server.SimpleHTTPRequestHandler) as s:
        s.serve_forever()

# =========================
# MAIN
# =========================
async def main():
    threading.Thread(target=web,daemon=True).start()
    await bot.start()
    print("Bot iniciado")
    await asyncio.Event().wait()

if __name__=="__main__":
    asyncio.run(main())    }))
    with open(file,'rb') as f:
        r=requests.put(f"https://s3.us.archive.org/{identifier}/{file.name}",auth=auth,data=f)
    if r.status_code in [200,201]:
        url=f"https://archive.org/download/{identifier}/{file.name}"
        file.unlink()
        return url

@bot.on_message(filters.command("start"))
def start(_,m): m.reply_text("Envíame archivo o link 📥")

@bot.on_message(filters.document|filters.video|filters.audio)
def tg(_,m):
    path=m.download()
    m.reply_text("Procesando...")
    chunks=split_file(path)
    Path(path).unlink()
    urls=[]
    for c in chunks:
        z=compress_chunk(c)
        u=upload(z)
        if u: urls.append(u)
    m.reply_text("✅\n"+"\n".join(urls))

@bot.on_message(filters.text)
def link(_,m):
    url=m.text.strip()
    if url.startswith("http"):
        try:
            name=url.split("/")[-1] or "file"
            r=requests.get(url,stream=True)
            with open(name,"wb") as f:
                for c in r.iter_content(1024):
                    if c:f.write(c)
            m.reply_text("Procesando...")
            chunks=split_file(name)
            Path(name).unlink()
            urls=[]
            for c in chunks:
                z=compress_chunk(c)
                u=upload(z)
                if u: urls.append(u)
            m.reply_text("✅\n"+"\n".join(urls))
        except:
            m.reply_text("Error ❌")

def web():
    port=int(os.environ.get("PORT",10000))
    with socketserver.TCPServer(("",port),http.server.SimpleHTTPRequestHandler) as s:
        s.serve_forever()

if __name__=="__main__":
    threading.Thread(target=web,daemon=True).start()
    bot.run()
