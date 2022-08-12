import requests
from bs4 import BeautifulSoup
from os import mkdir, path


def get_image(condition, image_url):
    #####  ##### CODE FROM STACKOVERFLOW ###### ########
    # ####  https://stackoverflow.com/a/60847710  #### #
    #####  #####                         ###### ########
    """
    Get image based on url.
    :return: Image name if everything OK, False otherwise
    """
    image_name = path.split(image_url)[1]
    try:
        image = requests.get(image_url)
    except OSError:  # Little too wide, but work OK, no additional imports needed. Catch all conection problems
        return False
    if image.status_code == 200:  # we could have retrieved error page
        try:
            mkdir(path.join(path.dirname(path.realpath(__file__)), "images", condition))
        except FileExistsError:
            pass
        base_dir = path.join(path.dirname(path.realpath(__file__)), "images", condition) # Use your own path or "" to use current working directory. Folder must exist.
        with open(path.join(base_dir, image_name), "wb") as f:
            f.write(image.content)
        return image_name

def retrieve_web_page(url):
    webpage = requests.get(url)
    return BeautifulSoup(webpage.text, "html.parser")

def format_condition(condition):
    return condition.rstrip().lstrip().title()

def web(url):
    dom = retrieve_web_page(url)
    for link in dom.select('.nhsuk-card.nhsuk-card--feature li a'):
        images(url.replace("/conditions/", "")+link.get('href'))
        dom2 = retrieve_web_page(url)
        condition = ""

        try:
            condition = dom2.select_one(".nhsuk-caption-xl.nhsuk-caption--bottom").text.replace("-", "")
        except AttributeError:
            condition = dom2.select_one("h1").text
        
        images = dom2.select(".nhsuk-image__img")

        for image in images:
            image_url = image.attrs['srcset'].split(",\n      ")[-1].split(" ")[0]
            get_image(format_condition(condition), image_url)
        
        print(condition, "-", len(images), "images found")

web("https://www.nhs.uk/conditions/")