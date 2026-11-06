import os, subprocess

def download_site(url, folder):
    os.makedirs(folder, exist_ok=True)
    try:
        subprocess.run(["wget", "--mirror", "--page-requisites",
                         "--convert-links", "--timeout=15",
                         "-P", folder, url], timeout=30)
    except Exception as e:
        print(f"Failed: {url} - {e}")

def download_list(filepath, output_dir):
    with open(filepath) as f:
        urls = [u.strip() for u in f if u.strip()]
    for i, url in enumerate(urls):
        if not url.startswith("http"):
            url = "http://" + url
        print(f"[{i+1}/{len(urls)}] {url}")
        download_site(url, f"{output_dir}/site_{i:04d}")

if __name__ == "__main__":
    download_list("data/phishing_urls.txt", "data/phishing")
    download_list("data/legitimate_urls.txt", "data/legitimate")