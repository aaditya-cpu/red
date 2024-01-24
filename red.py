import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def is_valid_url(url):
	"""
    Checks whether `url` is a valid URL.
    """
	parsed = urlparse(url)
	return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_images(url):
	"""
    Returns all image URLs on a single `url`
    """
	soup = BeautifulSoup(requests.get(url).content, "html.parser")
	urls = []
	for img in soup.find_all("img"):
		img_url = img.attrs.get("src")
		if not img_url:
			# if img does not contain src attribute, just skip
			continue
		img_url = urljoin(url, img_url)
		try:
			pos = img_url.index("?")
			img_url = img_url[:pos]
		except ValueError:
			pass
		if is_valid_url(img_url):
			urls.append(img_url)
	return urls


def download(url, pathname):
	"""
    Downloads a file given an URL and puts it in the folder `pathname`
    """
	if not os.path.isdir(pathname):
		os.makedirs(pathname)
	response = requests.get(url)
	filename = os.path.join(pathname, url.split("/")[-1])
	with open(filename, "wb") as f:
		f.write(response.content)


def main(url, path):
	# get all images
	imgs = get_all_images(url)
	for img in imgs:
		# for each img, download it
		download(img, path)


if __name__ == "__main__":
	url = "http://nitiraj.net"  # replace with your URL
	path = "downloaded_files"  # local directory to save downloaded files
	main(url, path)
