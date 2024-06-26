import requests
from bs4 import BeautifulSoup

def scrape_article(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # on extrait les données 
        title = soup.find('h1').text

        date_published = None
        
        # on extrait la date de publication dans une balise <time>
        time_tag = soup.find('time')
        if time_tag and 'datetime' in time_tag.attrs:
            date_published = time_tag['datetime']
        
      
        
        # on extrait le contenu de l'article
        content = ''
        
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            content += p.text + '\n'
        # on extrait l'auteur de l'article
        author = None
        author_tag = soup.find('span', class_='author')
        if author_tag:
            author = author_tag.text.strip()
        return {
            'title': title,
            'date_published': date_published,
            'content': content,
            'author': author
        }
    else:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")
        return None

def scrape_article_For_ML(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # on extrait les données 
        title = soup.find('h1').text      
      
        
        # on extrait le contenu de l'article
        content = ''
        
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            content += p.text + '\n'
       
        return {
            title,
            content,
        }
    else:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")
        return None

def findUrlHref(base_url):
    unique_urls = set() #on cherche à ne pas avoir de doublons

    page_num = 1
    while True:
        page_url = f"{base_url}/blog/page/{page_num}"
        
        response = requests.get(page_url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            all_a_tags = soup.find_all('a', href=True)  # Trouver tous les <a> tags avec l'attribut href car on a remaqué que les urls se trouvaient deans ces balises lorque on a inspecté le site.
            
            # on filtre les deux premiers et le dernier lien car ils ne sont pas relevants
            filtered_a_tags = all_a_tags[2:-1] if len(all_a_tags) > 3 else all_a_tags
            
            # on récupére les href attributs
            page_urls = [tag['href'] for tag in filtered_a_tags]
            unique_urls.update(page_urls)
            
            # on regarde s'il y a une page suivante dans le blog
            next_page_link = soup.find('a', class_='next page-numbers')
            if not next_page_link:
                break  #on sort de la boucle  s'il n'y a pas de lien vers la page suivante
            
            page_num += 1  # sinon on passe à la page suivante

    return list(unique_urls) 

