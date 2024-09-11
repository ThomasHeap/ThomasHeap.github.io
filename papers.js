async function fetchPapers(authorId) {
    const response = await fetch(`https://api.semanticscholar.org/graph/v1/author/${authorId}?fields=papers.title,papers.year,papers.authors,papers.venue,papers.url`);
    const data = await response.json();
    return data.papers;
}

function displayPapers(papers) {
    const papersList = document.getElementById('papers-list');
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

async function init() {
    const authorId = '2217761036'; // Replace with your Semantic Scholar Author ID
    const papers = await fetchPapers(authorId);
    displayPapers(papers);
}

window.onload = init;