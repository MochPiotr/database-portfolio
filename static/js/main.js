console.log("main.js")

document.addEventListener("DOMContentLoaded", function () {
  const dropdownToggle = document.getElementById("dropdown-toggle");
  const dropdownMenu = document.getElementById("dropdown-menu");
  const options = dropdownMenu.querySelectorAll(".dropdown-option");
  const selectedText = document.getElementById("selected-filters");

  // 🔻 otwieranie / zamykanie dropdowna
  dropdownToggle.addEventListener("click", function () {
    dropdownMenu.classList.toggle("active");
  });

  // 🔹 funkcja filtrowania tabeli po Statusie (5 kolumna)
  function filterTableByStatus() {
    const rows = document.querySelectorAll(".table_row");
    const activeStatuses = Array.from(options)
      .filter(opt => opt.classList.contains("active") && opt.dataset.value !== "all")
      .map(opt => opt.dataset.value.toLowerCase());

    rows.forEach(row => {
      const cells = row.querySelectorAll(".table_cell");
      const statusCell = cells[4]; // 5 kolumna = Status
      const statusText = statusCell ? statusCell.textContent.trim().toLowerCase() : "";

      // jeśli "All" wybrane lub brak aktywnych, pokaż wszystkie
      if (activeStatuses.length === 0 || activeStatuses.includes("all")) {
        row.style.display = "";
      } else {
        row.style.display = activeStatuses.includes(statusText) ? "" : "none";
      }
    });
  }

  // 🔹 logika wyboru dropdown
  options.forEach(option => {
    option.addEventListener("click", function (e) {
      const checkIcon = this.querySelector(".check-icon");

      // jeśli kliknięto "All", resetujemy wszystko
      if (this.dataset.value === "all") {
        options.forEach(opt => {
          opt.classList.remove("active");
          opt.querySelector(".check-icon").classList.add("hidden");
        });
        this.classList.add("active");
        checkIcon.classList.remove("hidden");
        selectedText.textContent = "All Status";
      } else {
        // jeśli kliknięto inną opcję, odznacz "All"
        const allOption = dropdownMenu.querySelector('[data-value="all"]');
        allOption.classList.remove("active");
        allOption.querySelector(".check-icon").classList.add("hidden");

        // przełącz aktywność klikniętej opcji
        this.classList.toggle("active");
        checkIcon.classList.toggle("hidden");

       
      }

      // 🔹 wywołanie filtra po każdej zmianie dropdown
      filterTableByStatus();
    });
  });

  // 🔹 klik poza dropdownem – zamknij
  document.addEventListener("click", function (e) {
    if (!dropdownToggle.contains(e.target) && !dropdownMenu.contains(e.target)) {
      dropdownMenu.classList.remove("active");
    }
  });
});




document.addEventListener("DOMContentLoaded", function() {
  const headerCells = document.querySelectorAll(".table_header .table_cell[data-type]");
  const table = document.querySelector(".table");

  headerCells.forEach((headerCell, columnIndex) => {
    const icon = headerCell.querySelector(".material-symbols-outlined");
    let ascending = true;

    if (icon) {
      icon.addEventListener("click", function() {
        const type = headerCell.dataset.type;
        const rows = Array.from(document.querySelectorAll(".table_row"));

        rows.sort((a, b) => {
          const aVal = a.querySelectorAll(".table_cell")[columnIndex].innerText.trim();
          const bVal = b.querySelectorAll(".table_cell")[columnIndex].innerText.trim();

          // typy danych
          if (type === "number") {
            const numA = parseFloat(aVal) || 0;
            const numB = parseFloat(bVal) || 0;
            return ascending ? numA - numB : numB - numA;
          }

          if (type === "date") {
            const dateA = new Date(aVal);
            const dateB = new Date(bVal);
            return ascending ? dateA - dateB : dateB - dateA;
          }

          // domyślnie alfabetycznie
          return ascending
            ? aVal.localeCompare(bVal, 'pl', { sensitivity: 'base' })
            : bVal.localeCompare(aVal, 'pl', { sensitivity: 'base' });
        });

        // odświeżenie DOM
        rows.forEach(r => r.remove());
        rows.forEach(r => table.appendChild(r));

        // zmiana kierunku i ikony
        ascending = !ascending;
        icon.textContent = ascending ? "keyboard_arrow_down" : "keyboard_arrow_up";
      });
    }
  });
});






document.addEventListener("DOMContentLoaded", function() {
  const searchInput = document.querySelector(".search .input");
  if (!searchInput) return;

  searchInput.addEventListener("input", function() {
    const query = this.value.toLowerCase().trim();
    const rows = document.querySelectorAll(".table_row");

    rows.forEach(row => {
      const cells = row.querySelectorAll(".table_cell");
      let matched = false;

      for (let cell of cells) {
        const text = cell.innerText.toLowerCase().trim();
        if (query !== "" && text.includes(query)) {
          matched = true;
          break;
        }
      }

      row.style.display = matched ? "" : "none";

      if (query === "") row.style.display = "";
    });
  });
});


document.addEventListener("DOMContentLoaded", function() {
  const searchInput = document.querySelector(".search .input");
  if (!searchInput) return;

  searchInput.addEventListener("input", function() {
    const query = this.value.toLowerCase().trim();
    const cards = document.querySelectorAll(".contact-card");

    cards.forEach(card => {
      let matched = false;

      // pobieramy wszystkie teksty w karcie, które chcemy przeszukać
      const texts = [
        card.querySelector(".contact-header-name h3")?.innerText, // imię i nazwisko
        card.querySelector(".title")?.innerText,                  // stanowisko
        card.querySelector(".company")?.innerText,                // firma / lead
        card.querySelector(".contact-info h2:nth-child(1)")?.innerText, // email
        card.querySelector(".contact-info h2:nth-child(2)")?.innerText  // telefon
      ];

      // sprawdzamy każde pole osobno
      for (let text of texts) {
        if (!text) continue;
        if (text.toLowerCase().includes(query) && query !== "") {
          matched = true;
          break;
        }
      }

      card.style.display = matched ? "" : "none";

      // jeśli input pusty, pokaż wszystkie karty
      if (query === "") card.style.display = "";
    });
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const initScrollLogic = () => {
    const scrollViews = Array.from(document.querySelectorAll('.scroll-view'));
    const scrollView = scrollViews.find(el => {
      const rect = el.getBoundingClientRect();
      return rect.width > 0 && rect.height > 0;
    });

    if (!scrollView) return;

    const lines = Array.from(scrollView.querySelectorAll('.scroll-line'));
    if (lines.length === 0) return;

    let timeoutId = null;

    // 🔹 Wybór aktywnej linii: najbliżej środka
    const updateActive = () => {
      const center = scrollView.scrollTop + scrollView.clientHeight / 2;
      let closest = null;
      let minDist = Infinity;

      lines.forEach(line => {
        const lineCenter = line.offsetTop + line.offsetHeight / 2;
        const dist = Math.abs(center - lineCenter);
        if (dist < minDist) {
          minDist = dist;
          closest = line;
        }
      });

      lines.forEach(l => l.classList.remove('active'));
      if (closest) closest.classList.add('active');
      return closest;
    };

    // 🔹 Snap do środka
    const snap = () => {
      const active = scrollView.querySelector('.scroll-line.active');
      if (!active) return;
      const target =
        active.offsetTop - scrollView.clientHeight / 2 + active.offsetHeight / 2;
      scrollView.scrollTo({ top: target, behavior: 'smooth' });
    };

    scrollView.addEventListener('scroll', () => {
      updateActive();
      clearTimeout(timeoutId);
      timeoutId = setTimeout(snap, 120); // delikatne snapowanie
    });

    // 🔹 Start: pierwsza linia wyśrodkowana
    requestAnimationFrame(() => {
      lines.forEach(l => l.classList.remove('active'));
      lines[0].classList.add('active');
      const target =
        lines[0].offsetTop - scrollView.clientHeight / 2 + lines[0].offsetHeight / 2;
      scrollView.scrollTo({ top: target, behavior: 'auto' });
    });
  };

  window.addEventListener('load', initScrollLogic);
});

/* MENU */
// --- Mobile menu toggle (sidebar wysuwany z dołu) ---
document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.querySelector('menuToggle');      // Twój hamburger (span)
  const mobileMenu = document.getElementById('mobileMenu'); // Sidebar z kategoriami

  if (!toggleBtn || !mobileMenu) return; // zabezpieczenie, jeśli nie istnieją w tym templacie

  // Kliknięcie hamburgera => otwórz / zamknij sidebar
  toggleBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('active');
    toggleBtn.classList.toggle('open'); // opcjonalnie — dla animacji ikony
  });

  // Kliknięcie w link w menu => zamknij sidebar
  mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      mobileMenu.classList.remove('active');
      toggleBtn.classList.remove('open');
    });
  });

  // (Opcjonalnie) kliknięcie poza sidebar => zamknij
  document.addEventListener('click', (e) => {
    const clickedInsideMenu = mobileMenu.contains(e.target);
    const clickedHamburger = toggleBtn.contains(e.target);
    if (!clickedInsideMenu && !clickedHamburger) {
      mobileMenu.classList.remove('active');
      toggleBtn.classList.remove('open');
    }
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const hamburger = document.getElementById('menuToggle');
  const mobileMenu = document.getElementById('mobileMenu');

  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('open');
      mobileMenu.classList.toggle('active'); // jeśli masz animację sidebaru
    });
  }
});
