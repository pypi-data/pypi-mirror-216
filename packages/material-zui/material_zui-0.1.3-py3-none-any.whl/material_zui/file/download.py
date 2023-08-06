from urllib.request import urlopen


def download(url: str, output_path: str):
    mp4File = urlopen(url)
    with open(output_path, "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break
