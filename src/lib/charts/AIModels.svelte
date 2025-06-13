<script>
  import { onMount } from "svelte";
  import * as d3 from "d3";
  import { base } from "$app/paths";

  let data = [];
  const width = 960;
  const height = 500;
  const margin = { top: 40, right: 30, bottom: 60, left: 80 };

  let xScale, yScale;
  let xAxisGroup, yAxisGroup;

  // hover / seleção fixa
  let hoveredDatum = null;
  let fixedDatum   = null;
  $: current = fixedDatum || hoveredDatum;

  // toggle de visão
  let viewByOrg = false;

  // escalas de cor
  let domainColorScale;
  let orgColorScale;

  const formatYear  = d3.timeFormat("%Y");
  const formatFlops = (n) => n.toExponential(2);

  onMount(async () => {
    const raw = await d3.csv(`${base}/data/notable_models.csv`, row => ({
      name: row["Model"]?.trim() ?? "",
      pubDate: row["Publication date"]
        ? new Date(row["Publication date"])
        : new Date(),
      flops: row["Training compute (FLOP)"]
        ? +row["Training compute (FLOP)"].replace(/,/g, "")
        : NaN,
      domain: row["Domain"]?.trim() ?? "Other",
      organization: row["Organization"]?.trim() ?? "Other"
    }));

    data = raw
      .filter(d =>
        d.name &&
        !isNaN(d.pubDate.getTime()) &&
        !isNaN(d.flops) &&
        d.flops > 0
      )
      .sort((a,b) => a.pubDate - b.pubDate);

    // escalas dos eixos
    xScale = d3.scaleTime()
      .domain(d3.extent(data, d => d.pubDate))
      .range([margin.left, width - margin.right]);

    const allFlops = data.map(d => d.flops);
    yScale = d3.scaleLog()
      .base(10)
      .domain([d3.min(allFlops), d3.max(allFlops)])
      .range([height - margin.bottom, margin.top]);

    // escala de domínio
    const domains = Array.from(new Set(data.map(d => d.domain)));
    domainColorScale = d3.scaleOrdinal()
      .domain(domains)
      .range(d3.schemeCategory10);

    // escala de organização
    const orgs = Array.from(new Set(data.map(d => d.organization)));
    orgColorScale = d3.scaleOrdinal()
      .domain(orgs)
      .range(d3.schemeCategory10);
  });

  // desenha eixos
  $: if (xScale && xAxisGroup) {
    d3.select(xAxisGroup).call(
      d3.axisBottom(xScale)
        .ticks(d3.timeYear.every(5))
        .tickFormat(d3.timeFormat("%Y"))
    );
  }
  $: if (yScale && yAxisGroup) {
    d3.select(yAxisGroup).call(
      d3.axisLeft(yScale).ticks(10, ".0e")
    );
  }

  // tooltip
  function showTooltip(d) {
    const tt = document.getElementById("tooltip");
    if (!tt) return;
    tt.innerHTML = `
      <strong>${d.name}</strong><br/>
      Year: ${formatYear(d.pubDate)}<br/>
      FLOPs: ${formatFlops(d.flops)}<br/>
      Domain: ${d.domain}<br/>
      Org: ${d.organization}
    `;
    tt.style.visibility = "visible";
    document.addEventListener("mousemove", moveTooltip);
  }
  function hideTooltip() {
    const tt = document.getElementById("tooltip");
    if (!tt) return;
    tt.style.visibility = "hidden";
    document.removeEventListener("mousemove", moveTooltip);
  }
  function moveTooltip(e) {
    const tt = document.getElementById("tooltip");
    const container = document.querySelector(".chart-container");
    if (!tt || !container) return;
    const rect = container.getBoundingClientRect();
    tt.style.left = `${e.clientX - rect.left + 10}px`;
    tt.style.top  = `${e.clientY - rect.top  + 10}px`;
  }

  // hover / click handlers
  function handleCircleMouseEnter(d) {
    hoveredDatum = d;
    showTooltip(d);
  }
  function handleCircleMouseLeave() {
    hoveredDatum = null;
    if (!fixedDatum) hideTooltip();
  }
  function handleCircleClick(d) {
    fixedDatum = d;
    showTooltip(d);
  }
  // ao clicar em qualquer outro lugar do container, limpa a seleção fixa
  function handleContainerClick() {
    fixedDatum = null;
    hideTooltip();
  }
</script>

<main>
  <!-- Toggle de visão -->
  <button class="toggle-btn" on:click={() => (viewByOrg = !viewByOrg)}>
    {viewByOrg ? "View Default" : "View by Organization"}
  </button>

  <div class="chart-container" on:click={handleContainerClick}>
    {#if !data.length}
      <p>Carregando dados…</p>
    {:else}
      <!-- SVG sem stopPropagation no click -->
      <svg {width} {height}>
        <!-- Título -->
        <text
          x={width/2}
          y={margin.top/2}
          text-anchor="middle"
          font-size="16px"
          font-weight="bold"
        >
          Notable AI Models: Training Compute vs Publication Date
        </text>

        <!-- Deep Learning Era -->
        <rect
          x={xScale(new Date(2010,0,1))}
          y={margin.top}
          width={xScale(new Date(2025,0,1)) - xScale(new Date(2010,0,1))}
          height={height - margin.top - margin.bottom}
          fill="lightblue"
          opacity="0.2"
        />

        <!-- Eixos -->
        <g
          class="axis x-axis"
          transform={`translate(0, ${height - margin.bottom})`}
          bind:this={xAxisGroup}
        />
        <g
          class="axis y-axis"
          transform={`translate(${margin.left},0)`}
          bind:this={yAxisGroup}
        />
        <text
          x={width/2}
          y={height - margin.bottom/3}
          text-anchor="middle"
          font-size="12px"
        >
          Publication Date
        </text>
        <text
          transform={`translate(${margin.left/3}, ${height/2}) rotate(-90)`}
          text-anchor="middle"
          font-size="12px"
        >
          Training Compute (FLOP) [log scale]
        </text>

        <!-- Pontos: stopPropagation apenas aqui -->
        {#each data as d (d.name)}
          <circle
            cx={xScale(d.pubDate)}
            cy={yScale(d.flops)}
            r="4"
            class="point"
            style="
              fill: {current === d
                ? (viewByOrg
                    ? orgColorScale(d.organization)
                    : domainColorScale(d.domain))
                : 'teal'};
              opacity: {current === d ? 1 : 0.7}
            "
            on:mouseenter={() => handleCircleMouseEnter(d)}
            on:mouseleave={handleCircleMouseLeave}
            on:click|stopPropagation={() => handleCircleClick(d)}
            aria-hidden="true"
          />
        {/each}

        <!-- Anotação GPT-4 -->
        {#each data.filter(d => d.name === "GPT-4") as d}
          <text
            x={xScale(d.pubDate) + 6}
            y={yScale(d.flops) - 6}
            class="annotation"
          >
            GPT-4
          </text>
        {/each}
      </svg>

      <!-- Espaço reservado para legenda -->
      <div class="legend-below">
        {#if current}
          <div
            class="color-box"
            style="background-color:
              {viewByOrg
                ? orgColorScale(current.organization)
                : domainColorScale(current.domain)
              }"
          ></div>
          <div class="legend-text">
            {viewByOrg ? current.organization : current.domain}
          </div>
        {/if}
      </div>

      <!-- Tooltip -->
      <div id="tooltip"></div>
    {/if}
  </div>
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .toggle-btn {
    background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%);
    color: #fff;
    border: none;
    border-radius: 0.375rem;
    padding: 0.6rem 1.2rem;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0, 13, 255, 0.2);
    transition:
      background 0.2s ease,
      transform 0.1s ease,
      box-shadow 0.2s ease;
    align-self: start;
  }
  .toggle-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 13, 255, 0.3);
  }
  .toggle-btn:active {
    transform: translateY(0);
    box-shadow: 0 3px 6px rgba(0, 13, 255, 0.2);
  }
  .toggle-btn:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(107, 115, 255, 0.5);
  }

  .chart-container {
    position: relative;
  }

  svg {
    font-family: sans-serif;
    background-color: #fafafa;
    border: 1px solid #ddd;
  }

  .point {
    cursor: pointer;
  }

  .annotation {
    font-size: 10px;
    fill: #333;
  }

  .legend-below {
    display: flex;
    align-items: center;
    margin-top: 0.5rem;
    min-height: 1.2em;
  }
  .legend-below .color-box {
    width: 12px;
    height: 12px;
    margin-right: 6px;
    border: 1px solid #666;
  }
  .legend-below .legend-text {
    font-size: 0.9rem;
  }

  #tooltip {
    position: absolute;
    visibility: hidden;
    background: rgba(255,255,255,0.95);
    padding: 6px;
    border: 1px solid #ccc;
    border-radius: 4px;
    pointer-events: none;
    font-size: 0.9rem;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
    z-index: 10;
  }
</style>
