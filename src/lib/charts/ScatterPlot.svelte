<script>
    import * as d3 from "d3";

    export let data = [];
    export let coordenatesSufixes = [
        { sufix: "random" },
        { sufix: "line" },
        { sufix: "xor" },
    ];
    export let stepFixe = 20;
    export let progress = 0;

    // Config
    const config = {
        width: 400,
        height: 300,
        margin: { top: 20, right: 20, bottom: 20, left: 20 }
    };
    const colorMap = { '0': 'var(--color-orange)', '1': 'var(--color-blue)' };

    const innerW = config.width - config.margin.left - config.margin.right;
    const innerH = config.height - config.margin.top - config.margin.bottom;

    let vizContainer;
    let svg, g, x, y;

    // Precompute step metadata
    let stepsCenters = [];
    let interval = 0;
    let fixeInterval = 0;
    let innerInteravalRange = 0;

    $: {
        stepsCenters = [];
        if (coordenatesSufixes.length > 1) {
            interval = 100 / (coordenatesSufixes.length - 1);
            fixeInterval = interval * stepFixe / 100;
            innerInteravalRange = interval - 2 * fixeInterval;
            stepsCenters = coordenatesSufixes.map((_, i) => i * interval);
        }
    }

    // Initialize SVG once
    $: if (vizContainer && !svg) {
        svg = d3.select(vizContainer)
            .append("svg")
            .attr("viewBox", `0 0 ${config.width} ${config.height}`)
            .attr("preserveAspectRatio", "xMidYMid meet");

        g = svg.append("g")
            .attr("transform", `translate(${config.margin.left},${config.margin.top})`);

        x = d3.scaleLinear().range([0, innerW]).domain([-1, 1]);
        y = d3.scaleLinear().range([innerH, 0]).domain([-1, 1]);
    }

    // Compute progress state
    let currentSufix, prevSufix, nextSufix, innerProgress;

    $: {
        if (stepsCenters.length) {
            const i = d3.bisect(stepsCenters, progress);

            if (i === 0) {
                currentSufix = coordenatesSufixes[0].sufix;
                prevSufix = nextSufix = innerProgress = null;
            } else if (i === stepsCenters.length) {
                currentSufix = coordenatesSufixes.at(-1).sufix;
                prevSufix = nextSufix = innerProgress = null;
            } else {
                const center = stepsCenters[i - 1];
                const diff = progress - center;

                if (Math.abs(diff) < fixeInterval) {
                    currentSufix = coordenatesSufixes[i - 1].sufix;
                    prevSufix = nextSufix = innerProgress = null;
                } else if (diff < 0) {
                    currentSufix = null;
                    prevSufix = coordenatesSufixes[i - 2]?.sufix;
                    nextSufix = coordenatesSufixes[i - 1].sufix;
                    innerProgress = (progress - (stepsCenters[i - 2] + fixeInterval)) / innerInteravalRange;
                } else {
                    currentSufix = null;
                    prevSufix = coordenatesSufixes[i - 1].sufix;
                    nextSufix = coordenatesSufixes[i]?.sufix;
                    innerProgress = (progress - (stepsCenters[i - 1] + fixeInterval)) / innerInteravalRange;
                }
            }
        }
    }

    // Compute interpolated position
    function getPosition(d, axis) {
        const key = axis === 'x' ? 'x_' : 'y_';

        if (currentSufix) {
            return d[key + currentSufix];
        }
        const prev = d[key + prevSufix];
        const next = d[key + nextSufix];
        return prev * (1 - innerProgress) + next * innerProgress;
    }

    // Update chart
    $: if (data && svg && progress) {
        const update = g.selectAll(".circles")
            .data(data, d => d.key);

        update.exit().remove();

        const enter = update.enter()
            .append("g")
            .attr("class", "circles");

        enter.append('circle')
            .attr('fill', d => colorMap[d.class])
            .attr('r', 2);

        const merged = enter.merge(update);

        merged.select('circle')
            .transition().duration(300)
            .attr('cx', d => x(getPosition(d, 'x')))
            .attr('cy', d => y(getPosition(d, 'y')));
    }
</script>

<div class="scatter-plot">
    <div id="viz-container" bind:this={vizContainer}></div>
</div>

<style>
    .scatter-plot {
        height: 100%;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    #viz-container {
        width: 80%;
        aspect-ratio: 4 / 3;
    }
</style>
