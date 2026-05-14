document.addEventListener('DOMContentLoaded', () => {
  /************************************************
   * 1) LIGHT / DARK THEME TOGGLE
   ************************************************/
  const root = document.documentElement;
  const themeBtn = document.getElementById('theme-toggle');

  // Initial theme (localStorage se read karo, warna light)
  const savedTheme = localStorage.getItem('theme');
  const initialTheme = savedTheme || 'light';
  root.setAttribute('data-theme', initialTheme);

  if (themeBtn) {
    themeBtn.textContent = initialTheme === 'dark' ? 'Light Mode' : 'Dark Mode';

    themeBtn.addEventListener('click', () => {
      const current = root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      themeBtn.textContent = next === 'dark' ? 'Light Mode' : 'Dark Mode';
    });
  }

  /************************************************
   * 2) SUBJECT → UNITS LOADING LOGIC (your code)
   ************************************************/
  const subjectCards = document.querySelectorAll('.subject-card');
  const unitsContainer = document.getElementById('units-container');
  const subjectTitle = document.getElementById('subject-title');

  // (Optional) section show/hide helper – agar use karna ho
  function showSection(id) {
    document.querySelectorAll('.section').forEach(sec => {
      sec.style.display = 'none';
    });
    const target = document.getElementById(id);
    if (target) {
      target.style.display = 'block';
    }
  }

  // Subject cards click
  subjectCards.forEach(card => {
    card.addEventListener('click', () => {
      subjectCards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');
      const slug = card.dataset.slug;
      loadUnits(slug);
      // Agar subject click pe koi section show karna ho:
      // showSection('units-section');
    });
  });

  // Units load function
  async function loadUnits(slug) {
    if (!unitsContainer) return;

    unitsContainer.innerHTML = '<p class="hint-text">Loading units...</p>';
    try {
      const res = await fetch(`/api/subject/${slug}/units/`);
      const data = await res.json();
      subjectTitle.textContent = data.subject || 'Units';

      if (!data.units || !data.units.length) {
        unitsContainer.innerHTML = '<p class="no-notes">No units yet.</p>';
        return;
      }

      unitsContainer.innerHTML = data.units.map(unit => `
        <div class="unit-card">
          <div class="unit-header">
            <span class="unit-badge">Unit ${unit.title}</span>
            <h3>${unit.title}</h3>
          </div>
          <div class="unit-notes">
            ${
              unit.notes.length
                ? unit.notes.map(n => `
                  <div class="unit-note-row">
                    <span class="note-title">${n.title}</span>
                    <button class="btn view-btn"
                      onclick="window.open('/note/${n.id}/view/', '_blank')">
                      View
                    </button>
                  </div>
                `).join('')
                : '<p class="no-notes">No notes in this unit.</p>'
            }
          </div>
        </div>
      `).join('');
    } catch (e) {
      unitsContainer.innerHTML = '<p class="no-notes">Error loading units.</p>';
    }
  }
});