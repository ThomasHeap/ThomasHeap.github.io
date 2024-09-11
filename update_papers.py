import requests
import json
from datetime import datetime
import os

AUTHOR_ID = os.environ.get('AUTHOR_ID')

def fetch_papers(author_id):
    url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}?fields=papers.title,papers.year,papers.authors,papers.venue,papers.url"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")
    data = response.json()
    return data.get('papers', [])

def generate_papers_markdown(papers):
    papers.sort(key=lambda x: x.get('year', 0), reverse=True)
    markdown = "---\nlayout: default\ntitle: Papers\n---\n\n## Published Papers\n\n"
    for paper in papers:
        authors = ', '.join([author.get('name', '') for author in paper.get('authors', [])])
        markdown += f"- [{paper.get('title', 'Untitled')}]({paper.get('url', '#')}) - {authors}, {paper.get('venue', 'N/A')}, {paper.get('year', 'N/A')}\n"
    return markdown

def generate_cv_markdown(papers):
    papers.sort(key=lambda x: x.get('year', 0), reverse=True)
    markdown = "### Selected Publications\n\n"
    for paper in papers[:5]:  # Only include the 5 most recent papers
        authors = ', '.join([author.get('name', '') for author in paper.get('authors', [])])
        markdown += f"- [{paper.get('title', 'Untitled')}]({paper.get('url', '#')}) - {authors}, {paper.get('venue', 'N/A')}, {paper.get('year', 'N/A')}\n"
    markdown += "\n[See all publications](/papers)"
    return markdown

def update_papers_page(papers):
    markdown = generate_papers_markdown(papers)
    with open('papers.md', 'w', encoding='utf-8') as f:
        f.write(markdown)
    print("Papers page updated.")

def update_cv_page(papers):
    cv_papers_markdown = generate_cv_markdown(papers)
    
    # Read the current CV content
    with open('cv.md', 'r', encoding='utf-8') as f:
        cv_content = f.read()
    
    # Split the content at the publications section
    parts = cv_content.split("### Selected Publications")
    if len(parts) != 2:
        raise Exception("Couldn't find '### Selected Publications' in cv.md")
    
    # Update the publications section
    updated_cv_content = parts[0] + cv_papers_markdown
    
    # Write the updated content back to cv.md
    with open('cv.md', 'w', encoding='utf-8') as f:
        f.write(updated_cv_content)
    print("CV page updated.")

def main():
    if not AUTHOR_ID:
        raise ValueError("AUTHOR_ID environment variable is not set")
    
    print(f"Fetching papers for author ID: {AUTHOR_ID}")
    papers = fetch_papers(AUTHOR_ID)
    print(f"Found {len(papers)} papers")
    
    update_papers_page(papers)
    update_cv_page(papers)
    
    print(f"Update completed at {datetime.now()}")

if __name__ == "__main__":
    main()