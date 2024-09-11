async function fetchPapers(authorId) {
    const response = await fetch(`https://api.semanticscholar.org/graph/v1/author/${authorId}?fields=papers.title,papers.year,papers.authors,papers.venue,papers.url`);
    const data = await response.json();
    return data.papers;
}

function displayPapers(papers, elementId = 'papers-list') {
    const papersList = document.getElementById(elementId);
    papers.sort((a, b) => b.year - a.year); // Sort by year, most recent first

    papers.forEach(paper => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = paper.url;
        a.textContent = paper.title;
        li.appendChild(a);

        const authors = paper.authors.map(author => author.name).join(', ');
        li.appendChild(document.createTextNode(` - ${authors}, ${paper.venue}, ${paper.year}`));

        papersList.appendChild(li);
    });
}

async function initPapers() {
    const authorId = 'YOUR_SEMANTIC_SCHOLAR_AUTHOR_ID'; // Replace with your Semantic Scholar Author ID
    const papers = await fetchPapers(authorId);

    if (document.getElementById('papers-list')) {
        displayPapers(papers, 'papers-list');
    }

    if (document.getElementById('cv-papers-list')) {
        displayPapers(papers.slice(0, 5), 'cv-papers-list'); // Display only the 5 most recent papers in CV
    }
}

window.onload = initPapers;
