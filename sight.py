import os
import cv2
import numpy as np

SCREENSHOT_DIR = "screenshots"
TEMPLATE_DIR = "templates"

def image_contains_template(filename, template):
    img = cv2.imread(filename)
    # template_img = cv2.imread(f"{TEMPLATE_DIR}/{template}")

    tmplt = cv2.imread(f"{TEMPLATE_DIR}/{template}", cv2.IMREAD_UNCHANGED)
    hh, ww = tmplt.shape[:2]

    # extract template mask as grayscale from alpha channel and make 3 channels
    tmplt_mask = tmplt[:,:,3]
    tmplt_mask = cv2.merge([tmplt_mask,tmplt_mask,tmplt_mask])

    # extract templt2 without alpha channel from tmplt
    tmplt2 = tmplt[:,:,0:3]

    # do template matching
    res = cv2.matchTemplate(img,tmplt2,cv2.TM_CCORR_NORMED, mask=tmplt_mask)
    # res = cv2.matchTemplate(img, template_img, cv2.TM_CCOEFF_NORMED)
    threshold = 0.96
    loc = np.where(res >= threshold)
    try:
        return loc[0]
    except IndexError:
        return None


if __name__ == '__main__':
    for screenshot in os.listdir(SCREENSHOT_DIR):
        if not screenshot.endswith(".png"):
            continue
        screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot)
        img = cv2.imread(screenshot_path)
        for template in os.listdir(TEMPLATE_DIR):
            if not template.endswith(".png"):
                continue
            contains = image_contains_template(screenshot_path, template)
            if contains.any():
                print(f"{screenshot} contains {template}")
