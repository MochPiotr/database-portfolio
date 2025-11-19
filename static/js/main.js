console.log("main.js")

// dropdowna
document.addEventListener("DOMContentLoaded", function () {
  const dropdownToggle = document.getElementById("dropdown-toggle");
  const dropdownMenu = document.getElementById("dropdown-menu");
  const options = dropdownMenu.querySelectorAll(".dropdown-option");
  const selectedText = document.getElementById("selected-filters");

  dropdownToggle.addEventListener("click", function () {
    dropdownMenu.classList.toggle("active");
  });

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

  // wyboru dropdown
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

      // wywołanie filtra po każdej zmianie dropdown
      filterTableByStatus();
    });
  });

  // klik poza dropdownem – zamknij
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

document.addEventListener("DOMContentLoaded", () => {
  const lines = Array.from(document.querySelectorAll(".scroll-line"));
  if (lines.length === 0) return;

  // jeśli żadna linia nie ma data-final, ostatnia jako final
  if (!lines.some(line => line.dataset.final === "true")) {
    lines[lines.length - 1].dataset.final = "true";
  }

  let index = 0;
  const delay = 1200;          // czas między przejściami (ms)
  const transitionTime = 600;  

  // wyczyść wszystkie stany
  lines.forEach(line => line.classList.remove("visible", "exit", "enter", "final"));

  // pokaż pierwszą linię natychmiast
  lines[0].classList.add("visible");

  const nextLine = () => {
    const current = lines[index];
    const next = lines[index + 1];

    // jeśli nie ma następnej -> zatrzymaj animację i zostaw ostatnią
    if (!next) {
      if (current.dataset.final === "true") {
        current.classList.add("final");
      }
      return;
    }

    const nextIsFinal = next.dataset.final === "true";

    // animacja wyjścia aktualnej
    current.classList.remove("visible");
    current.classList.add("exit");

    // przygotuj kolejną linię (wchodzenie od dołu)
    next.classList.add("enter");

    // po czasie przejścia przenosimy klasę active
    setTimeout(() => {
      current.classList.remove("exit");
      next.classList.remove("enter");
      next.classList.add("visible");
      index++;

      // jeśli kolejna jest finalna, zatrzymaj animację
      if (nextIsFinal) {
        next.classList.add("final");
        return;
      }

      // odpal kolejną po opóźnieniu
      setTimeout(nextLine, delay);
    }, transitionTime);
  };

  // uruchom animację po 0.8 sekundy, żeby użytkownik widział pierwszą linię
  setTimeout(nextLine, 800);
});


/* MENU */
// Mobile menu toggle (sidebar wysuwany z dołu
document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.querySelector('menuToggle');    
  const mobileMenu = document.getElementById('mobileMenu'); 

  if (!toggleBtn || !mobileMenu) return; // zabezpieczenie, jeśli nie istnieją w tym templacie

  // Kliknięcie manue => otwórz / zamknij sidebar
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

  const account = document.getElementById('accountToggle');
  const mobileAccount = document.getElementById('mobileAccount');

  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      const isOpening = !mobileMenu.classList.contains('active');

      // Zanim otworzymy menu, zamknij drugie (konto)
      if (account && mobileAccount) {
        account.classList.remove('open');
        mobileAccount.classList.remove('active');
      }

      // Teraz przełącz menu
      hamburger.classList.toggle('open', isOpening);
      mobileMenu.classList.toggle('active', isOpening);
    });
  }

  if (account && mobileAccount) {
    account.addEventListener('click', () => {
      const isOpening = !mobileAccount.classList.contains('active');

      // Zanim otworzymy konto, zamknij menu
      if (hamburger && mobileMenu) {
        hamburger.classList.remove('open');
        mobileMenu.classList.remove('active');
      }

      // Teraz przełącz konto
      account.classList.toggle('open', isOpening);
      mobileAccount.classList.toggle('active', isOpening);
    });
  }
});




