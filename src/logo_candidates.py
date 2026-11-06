def get_image_candidates(driver, local_html_path):
    driver.get(f"file:///{local_html_path}")
    driver.implicitly_wait(3)
    viewport_w = driver.execute_script("return window.innerWidth")
    viewport_h = driver.execute_script("return window.innerHeight")

    images = driver.find_elements("tag name", "img")
    candidates = []
    for img in images:
        try:
            loc = img.location
            size = img.size
            if size['width'] > 10 and size['height'] > 10 and loc['y'] < viewport_h:
                candidates.append({
                    "src": img.get_attribute("src"),
                    "x": loc['x'], "y": loc['y'],
                    "width": size['width'], "height": size['height'],
                    "viewport_w": viewport_w, "viewport_h": viewport_h
                })
        except Exception:
            continue
    return candidates