import requests
import os
import re
import io
import time
from PIL import Image

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


DOWNLOAD_FOLDER = r"C:\Users\Jedle\PycharmProjects\Ai-Image-Detection\images\scrapedImages"

SUBREDDIT = 'pics'
TARGET_IMAGE_COUNT = 450
MIN_WIDTH = 600
MIN_HEIGHT = 600


def download_images():
    # 1. Create folder
    if not os.path.exists(DOWNLOAD_FOLDER):
        try:
            os.makedirs(DOWNLOAD_FOLDER)
            print(f"Created folder: {DOWNLOAD_FOLDER}")
        except OSError as e:
            print(f"Error creating folder: {e}")
            return

    print(f"Scraping r/{SUBREDDIT} without API key...")

    headers = {'User-Agent': USER_AGENT}
    count = 0
    after_token = None

    while count < TARGET_IMAGE_COUNT:

        url = f"https://www.reddit.com/r/{SUBREDDIT}.json?limit=100"
        if after_token:
            url += f"&after={after_token}"

        try:
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                print(f"Error accessing Reddit: {response.status_code}")
                break

            data = response.json()
            posts = data['data']['children']

            if not posts:
                print("No more posts found.")
                break


            for post in posts:
                if count >= TARGET_IMAGE_COUNT:
                    break

                post_data = post['data']
                image_url = post_data.get('url_overridden_by_dest', post_data.get('url'))
                title = post_data.get('title', 'untitled')


                if image_url and image_url.endswith(('.jpg', '.jpeg', '.png')):
                    try:

                        img_resp = requests.get(image_url, headers=headers, timeout=10)
                        if img_resp.status_code == 200:
                            image_bytes = io.BytesIO(img_resp.content)

                            try:

                                img = Image.open(image_bytes)
                                width, height = img.size

                                if width >= MIN_WIDTH and height >= MIN_HEIGHT:

                                    clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
                                    clean_title = clean_title[:100].strip()
                                    ext = image_url.split('.')[-1]

                                    filename = f"{count + 1}_{clean_title}.{ext}"
                                    full_path = os.path.join(DOWNLOAD_FOLDER, filename)


                                    with open(full_path, 'wb') as f:
                                        f.write(img_resp.content)

                                    print(f"[{count + 1}/{TARGET_IMAGE_COUNT}] Saved: {width}x{height} - {clean_title}")
                                    count += 1

                            except Exception as e:

                                pass

                    except Exception as e:
                        print(f"Error downloading {image_url}: {e}")


            after_token = data['data']['after']
            if not after_token:
                break


            time.sleep(2)

        except Exception as e:
            print(f"Critical Error: {e}")
            break

    print("Done!")


if __name__ == '__main__':
    download_images()