(() => {
  let chart;
  let resize;
  let theme;

  document$.subscribe(() => {
    resize?.disconnect();
    theme?.disconnect();
    chart?.destroy();
    chart = undefined;
    const container = document.querySelector(".size-history");
    if (!container || typeof uPlot === "undefined") return;

    const data = JSON.parse(document.getElementById("size-history-data").textContent);
    const metrics = [
      { key: "total", label: "Total", dash: [] },
      { key: "best", label: "Best", dash: [8, 3] },
      { key: "alt", label: "Alt", dash: [3, 3] },
      { key: "realistic", label: "Realistic", dash: [10, 3, 2, 3] },
    ];
    const timestamp = new Intl.DateTimeFormat("en", {
      timeZone: "UTC", dateStyle: "medium", timeStyle: "short",
    });
    const color = (name) => getComputedStyle(container).getPropertyValue(name).trim();

    chart = new uPlot({
      width: container.clientWidth,
      height: container.clientWidth < 500 ? 280 : 340,
      tzDate: (time) => uPlot.tzDate(new Date(time * 1000), "UTC"),
      cursor: { y: false, drag: { x: true, y: false } },
      scales: { y: { range: (plot, min, max) => [0, Math.max(1, max * 1.05)] } },
      series: [
        { label: "", value: (plot, value) => value == null ? "—" : timestamp.format(value * 1000) },
        ...metrics.map((metric) => ({
          label: metric.label, width: 2, dash: metric.dash,
          stroke: () => color(`--history-${metric.key}`),
          value: (plot, value) => value == null ? "—" : `${value.toFixed(2)} TiB`,
          points: { show: false },
        })),
      ],
      axes: [
        { stroke: () => color("--md-default-fg-color"), grid: { show: false } },
        {
          label: "TiB", size: 52,
          stroke: () => color("--md-default-fg-color"),
          grid: { stroke: () => color("--md-default-fg-color--lightest") },
          values: (plot, ticks) => ticks.map((value) => String(Number(value.toFixed(2)))),
        },
      ],
    }, data, container);
    resize = new ResizeObserver(() => {
      const width = container.clientWidth;
      if (chart.width !== width) chart.setSize({ width, height: width < 500 ? 280 : 340 });
    });
    resize.observe(container);
    theme = new MutationObserver(() => chart.redraw(false, true));
    theme.observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
  });
})();
