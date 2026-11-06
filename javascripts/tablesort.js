document$.subscribe(() => {
  for (const table of document.querySelectorAll(".sortable-table table")) {
    if (table.dataset.tablesort) continue;

    const headers = table.tHead.rows[0].cells;
    new Tablesort(table);

    for (const header of headers) {
      header.tabIndex = 0;
      header.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          header.click();
        }
      });
    }

    table.dataset.tablesort = "true";
  }
});
