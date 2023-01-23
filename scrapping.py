from bs4 import BeautifulSoup
import requests
import csv

# https://www.allocine.fr/film/fichefilm-23839/critiques/spectateurs/star-0/  Scream 3                    30
# https://www.allocine.fr/film/fichefilm-50581/critiques/spectateurs/         Ocean's Twelve              67
# https://www.allocine.fr/film/fichefilm-109678/critiques/spectateurs/star-0/ Borat                       89
# https://www.allocine.fr/film/fichefilm-271379/critiques/spectateurs/        Shadow The Cloud            9
# https://www.allocine.fr/film/fichefilm-109173/critiques/spectateurs/star-0/ Pirahna 3D                  100
# https://www.allocine.fr/film/fichefilm-209778/critiques/spectateurs/        Spiderman Homecoming        66
# https://www.allocine.fr/film/fichefilm-288439/critiques/spectateurs/star-0/ Pray                        30
# https://www.allocine.fr/film/fichefilm-27448/critiques/spectateurs/star-0/  Hannibal                    32
# https://www.allocine.fr/film/fichefilm-126148/critiques/spectateurs/        Vicky Cristina Barcelona    74
# https://www.allocine.fr/film/fichefilm-37178/critiques/spectateurs/         Tueurs nés                  33
# https://www.allocine.fr/film/fichefilm-118343/critiques/spectateurs/        28 semaines plus tard       89



class Allo_cine:

    @staticmethod
    def get_all_pages():
        urls =[]
        page_number = 1

        for i in range(89):
            i = f"https://www.allocine.fr/film/fichefilm-118343/critiques/spectateurs/?page={page_number}"
            page_number += 1
            urls.append(i)
        return urls

    @staticmethod
    def scrap(url):
        r = requests.get(url)
        soupe = BeautifulSoup(r.content, "html.parser")
        utilisateurs = soupe.find_all("div", {"class": "hred review-card cf"})

        for utilisateur in utilisateurs:
            try:
                note= utilisateur.find("span", {"class": "stareval-note"}).text.strip()
                commentaire = utilisateur.find("div", {"class": "content-txt review-card-content"}).text.strip().replace('"', "''")
            except AttributeError as e:
                print(e)

            chemin = r"""./csv/28_jour_brief.csv"""
            with open(chemin, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([f"{note}", f"{commentaire}"])
                # f.write(f"{note}\n")
                # f.write(f"{commentaire}\n\n")


    @staticmethod
    def scrap_all():
        pages = Allo_cine.get_all_pages()

        for page in pages:
            Allo_cine.scrap(url = page)
            print(f"On scrape {page}")

Allo_cine.scrap_all()