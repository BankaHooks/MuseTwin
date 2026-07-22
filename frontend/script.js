const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const statusMsg = document.getElementById('statusMsg');
const resultsContainer = document.getElementById('resultsContainer');
const toast = document.getElementById('toast');

function showToast(text, isError = false) {
    toast.textContent = text;
    toast.style.background = isError ? 'rgba(255,70,70,0.9)' : 'var(--surface)';
    toast.classList.add('show');
    clearTimeout(toast._timeout);
    toast._timeout = setTimeout(() => toast.classList.remove('show'), 2500);
}

function setStatus(text, isError = false) {
    statusMsg.textContent = text;
    statusMsg.style.color = isError ? '#ff6b6b' : 'var(--text-secondary)';
}

function renderRecommendations(tracks) {
    const html = `
        <h3 style="margin-bottom:16px;">🎯 Found musical twins</h3>
        <div class="song-grid">
            ${tracks.map(t => `
                <div class="song-card">
                    <div class="song-card__title">${t.track}</div>
                    <div class="song-card__artist">${t.artist}</div>
                    <button class="song-card__play">▶ Listen</button>
                </div>
            `).join('')}
        </div>
    `;
    resultsContainer.innerHTML = html;
}

function renderMultipleMatches(matches) {
    const html = `
        <h4>Clarify the track:</h4>
        <ul class="multiple-matches">
            ${matches.map(m => `
                <li data-track="${m.track_name}" data-artist="${m.artist || ''}">
                    🎵 ${m.track_name} — ${m.artist || 'unknown'}
                </li>
            `).join('')}
        </ul>
    `;
    resultsContainer.innerHTML = html;
    document.querySelectorAll('.multiple-matches li').forEach(li => {
        li.addEventListener('click', () => {
            const track = li.dataset.track;
            const artist = li.dataset.artist;
            searchInput.value = `${track} ${artist}`.trim();
            fetchRecommendations(track, artist);
        });
    });
}

async function fetchRecommendations(trackName, artist = '') {
    searchBtn.disabled = true;
    searchBtn.innerHTML = '⏳ Searching...';
    setStatus('Searching for similar tracks...');
    resultsContainer.innerHTML = '';

    try {
        const params = new URLSearchParams({ track_name: trackName });
        if (artist) params.append('artist', artist);
        const response = await fetch(`/recommend?${params.toString()}`);
        if (!response.ok) throw new Error(`Error ${response.status}`);
        const data = await response.json();

        if (data.error) {
            setStatus(`❌ ${data.error}`, true);
            showToast('Track not found', true);
            return;
        }
        if (data.multiple_matches) {
            setStatus('Multiple matches found. Please clarify.');
            renderMultipleMatches(data.multiple_matches);
            return;
        }
        // handle possible typo "recommendations: "
        const recs = data.recommendations || data['recommendations: '];
        if (recs && Array.isArray(recs)) {
            renderRecommendations(recs);
            setStatus(`✅ Found ${recs.length} similar tracks`);
            showToast('Done!');
        } else {
            setStatus('Unexpected response format', true);
        }
    } catch (err) {
        console.error(err);
        setStatus('❌ Connection error', true);
        showToast('Network error', true);
    } finally {
        searchBtn.disabled = false;
        searchBtn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg> Search`;
    }
}

searchBtn.addEventListener('click', () => {
    const query = searchInput.value.trim();
    if (!query) {
        showToast('Please enter a track name', true);
        return;
    }
    fetchRecommendations(query);
});

searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') searchBtn.click();
});

document.querySelectorAll('.suggestion-tag').forEach(tag => {
    tag.addEventListener('click', () => {
        const q = tag.dataset.query;
        searchInput.value = q;
        fetchRecommendations(q);
    });
});

searchInput.focus();