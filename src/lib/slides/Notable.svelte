<script>
    import { onMount } from "svelte";
    import * as d3 from "d3";

    let data = [];
    const width = 960;
    const height = 500;
    const margin = { top: 40, right: 30, bottom: 60, left: 80 };

    let xScale;
    let yScale;
    let xAxisGroup;
    let yAxisGroup;

    const formatYear = d3.timeFormat("%Y");
    const formatFlops = (n) => n.toExponential(2);

    onMount(async () => {
        const raw = await d3.csv(`/data/notable_models.csv`, (row) => {
            return {
                name: row["Model"]?.trim() ?? "",
                pubDate: row["Publication date"]
                    ? new Date(row["Publication date"])
                    : new Date(""),
                flops: row["Training compute (FLOP)"]
                    ? +row["Training compute (FLOP)"].replace(/,/g, "")
                    : NaN,
            };
        });

        data = raw
            .filter(
                (d) =>
                    d.name !== "" &&
                    !isNaN(d.pubDate.getTime()) &&
                    !isNaN(d.flops) &&
                    d.flops > 0,
            )
            .sort((a, b) => a.pubDate.getTime() - b.pubDate.getTime());

        xScale = d3
            .scaleTime()
            .domain(d3.extent(data, (d) => d.pubDate))
            .range([margin.left, width - margin.right]);

        const allFlops = data.map((d) => d.flops);
        const yMin = d3.min(allFlops);
        const yMax = d3.max(allFlops);
        yScale = d3
            .scaleLog()
            .base(10)
            .domain([yMin, yMax])
            .range([height - margin.bottom, margin.top]);
    });

    $: if (xScale && xAxisGroup) {
        const xAxis = d3
            .axisBottom(xScale)
            .ticks(d3.timeYear.every(5))
            .tickFormat(d3.timeFormat("%Y"));
        d3.select(xAxisGroup).call(xAxis);
    }

    $: if (yScale && yAxisGroup) {
        const yAxis = d3.axisLeft(yScale).ticks(10, ".0e");
        d3.select(yAxisGroup).call(yAxis);
    }

    function showTooltip(datum) {
        const tt = document.getElementById("tooltip");
        if (!tt) return;

        tt.innerHTML = `
        <strong>${datum.name}</strong><br/>
        Year: ${formatYear(datum.pubDate)}<br/>
        FLOPs: ${formatFlops(datum.flops)}
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

        const offsetX = e.clientX - rect.left + 10;
        const offsetY = e.clientY - rect.top + 10;

        tt.style.left = `${offsetX}px`;
        tt.style.top = `${offsetY}px`;
    }
</script>

<main>
    <div class="chart-container">
        {#if data.length === 0}
            <p>Carregando dados…</p>
        {:else}
            <svg {width} {height}>
                <text
                    x={width / 2}
                    y={margin.top / 2}
                    text-anchor="middle"
                    font-size="16px"
                    font-weight="bold"
                >
                    Notable AI Models: Training Compute vs Publication Date
                </text>

                <rect
                    x={xScale(new Date(2010, 0, 1))}
                    y={margin.top}
                    width={xScale(new Date(2025, 0, 1)) -
                        xScale(new Date(2010, 0, 1))}
                    height={height - margin.top - margin.bottom}
                    fill="lightblue"
                    opacity="0.2"
                />

                <g
                    class="axis x-axis"
                    transform={`translate(0, ${height - margin.bottom})`}
                    bind:this={xAxisGroup}
                ></g>

                <g
                    class="axis y-axis"
                    transform={`translate(${margin.left}, 0)`}
                    bind:this={yAxisGroup}
                ></g>

                <text
                    x={width / 2}
                    y={height - margin.bottom / 3}
                    text-anchor="middle"
                    font-size="12px"
                >
                    Publication Date
                </text>

                <text
                    transform={`translate(${margin.left / 3}, ${height / 2}) rotate(-90)`}
                    text-anchor="middle"
                    font-size="12px"
                >
                    Training Compute (FLOP) [log scale]
                </text>

                {#each data as d (d.name)}
                    <circle
                        class="point"
                        cx={xScale(d.pubDate)}
                        cy={yScale(d.flops)}
                        r="4"
                        on:mouseenter={() => showTooltip(d)}
                        on:mouseleave={hideTooltip}
                        aria-hidden="true"
                    />
                {/each}

                {#each data.filter((d) => d.name === "GPT-4") as d}
                    <text
                        x={xScale(d.pubDate) + 6}
                        y={yScale(d.flops) - 6}
                        class="annotation"
                    >
                        GPT-4
                    </text>
                {/each}
            </svg>

            <div class="legend">
                <div class="legend-box"></div>
                <div>Deep Learning Era (2010–2025)</div>
            </div>

            <div id="tooltip"></div>
        {/if}
    </div>
</main>

<style>
    main {
        display: flex;
        gap: 2rem;
        padding: 1rem;
    }

    .chart-container {
        flex: 1 1 70%;
        position: relative;
    }

    svg {
        font-family: sans-serif;
        background-color: #fafafa;
        border: 1px solid #ddd;
    }

    .point {
        fill: teal;
        opacity: 0.7;
    }

    #tooltip {
        position: absolute;
        visibility: hidden;
        background: rgba(255, 255, 255, 0.95);
        padding: 6px;
        border: 1px solid #ccc;
        border-radius: 4px;
        pointer-events: none;
        font-size: 0.9rem;
        box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.1);
        z-index: 10;
    }

    .annotation {
        font-size: 10px;
        fill: #333;
    }

    .legend {
        display: flex;
        align-items: center;
        margin-top: 0.5rem;
        font-family: sans-serif;
        font-size: 14px;
        color: #333;
    }

    .legend-box {
        width: 20px;
        height: 20px;
        background-color: lightblue;
        opacity: 0.2;
        border: 1px solid #999;
        margin-right: 0.5rem;
    }
</style>
