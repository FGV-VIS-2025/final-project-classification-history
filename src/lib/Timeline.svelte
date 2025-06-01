<script>
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import data from "../data/models_timeline.json";
  
    let container;
  
    onMount(() => {
      const margin = { top: 20, right: 20, bottom: 40, left: 100 };
      const width = container.clientWidth - margin.left - margin.right;
      const height = 400 - margin.top - margin.bottom;
  
      const parseDate = d3.timeParse("%Y-%m-%d");
      data.forEach(d => {
        d.parsedDate = parseDate(d.date);
      });
  
      const categories = Array.from(new Set(data.map(d => d.category)));
  
      const yScale = d3
        .scaleBand()
        .domain(categories)
        .range([0, height])
        .padding(0.3);
  
      const minDate = d3.min(data, d => d.parsedDate);
      const maxDate = d3.max(data, d => d.parsedDate);
      const xScale = d3
        .scaleTime()
        .domain([d3.timeYear.offset(minDate, -1), d3.timeYear.offset(maxDate, 1)])
        .range([0, width]);
  
      const svg = d3
        .select(container)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);
  
      const xAxis = d3
        .axisBottom(xScale)
        .ticks(d3.timeYear.every(2))
        .tickFormat(d3.timeFormat("%Y"));
      svg
        .append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(xAxis)
        .selectAll("text")
        .attr("transform", "rotate(-45)")
        .style("text-anchor", "end");
  
      const yAxis = d3.axisLeft(yScale);
      svg.append("g").call(yAxis);
  
      const tooltip = d3
        .select("body")
        .append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);
  
      svg
        .selectAll("circle")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", d => xScale(d.parsedDate))
        .attr("cy", d => yScale(d.category) + yScale.bandwidth() / 2)
        .attr("r", 8)
        .attr("fill", d => {
          const palette = d3.schemeTableau10;
          const idx = categories.indexOf(d.category);
          return palette[idx % palette.length];
        })
        .on("mouseover", (event, d) => {
          tooltip
            .transition()
            .duration(200)
            .style("opacity", 0.95);
  
          tooltip
            .html(`
              <div class="tooltip-card">
                <h4>${d.name} (${d.date.slice(0, 4)})</h4>
                <p><strong>Autores:</strong> ${d.authors}</p>
                <p>${d.description}</p>
                ${d.paper ? `<p><a href="${d.paper}" target="_blank">Ler Paper</a></p>` : ""}
              </div>
            `)
            .style("left", event.pageX + 15 + "px")
            .style("top", event.pageY - 28 + "px");
        });
  
      svg
        .selectAll("text.label")
        .data(data)
        .enter()
        .append("text")
        .attr("class", "label")
        .attr("x", d => xScale(d.parsedDate))
        .attr("y", d => yScale(d.category) + yScale.bandwidth() / 2 - 12)
        .attr("text-anchor", "middle")
        .attr("font-size", "10px")
        .text(d => d.name);
  
      d3.select("body").on("click", (event) => {
        const target = event.target;
        if (
          target.tagName.toLowerCase() !== "circle" &&
          !target.closest(".tooltip-card")
        ) {
          tooltip
            .transition()
            .duration(200)
            .style("opacity", 0);
        }
      });
    });
  </script>
  
  <style>
    :global(div#timeline-container) {
      width: 100%;
    }
  
    :global(.tooltip) {
      position: absolute;
      pointer-events: none;
      background: #ffffffcc;
      border: 1px solid #999;
      border-radius: 4px;
      padding: 8px;
      font-size: 12px;
      box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.2);
      max-width: 220px;
      line-height: 1.3;
      color: #333;
      z-index: 10;
    }
  
    .tooltip-card {
      display: flex;
      flex-direction: column;
    }
  
    .tooltip-card h4 {
      margin: 0 0 4px 0;
      font-size: 14px;
    }
  
    .tooltip-card p {
      margin: 2px 0;
    }
  
    .tooltip-card a {
      color: #0366d6;
      text-decoration: none;
    }
  
    .tooltip-card a:hover {
      text-decoration: underline;
    }
  </style>
  
  <div id="timeline-container" bind:this={container}></div>
  