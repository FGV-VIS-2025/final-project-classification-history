<script>
    import { createEventDispatcher, onMount } from "svelte";
    import * as d3 from "d3";
    import { base } from "$app/paths";
  
    const filenameMap = {
      "Support Vector Machine":    "svm_arch.png",
      "Random Forest":             "rf_arch.png",
      "Gradient Boosting Machine": "gbm_arch.png",
      "AlexNet":                   "alexnet_arch.png",
      "VGG":                       "vgg_arch.png",
      "ResNet":                    "resnet_arch.png",
      "XGBoost":                   "xgboost_arch.png",
      "BERT":                      "bert_arch.png",
      "ViT":                       "vit_arch.png",
      "Swin Transformer":          "swin_arch.png"
    };
  
    const dispatch = createEventDispatcher();
    let container;
    
    let data = [];
    let categories = [];
    let colorScale;
  
    onMount(async () => {
      const parseDate = d3.timeParse("%Y-%m-%d");
      data = await d3.json(`${base}/data/models_timeline.json`);
      data.forEach(d => {
        d.parsedDate = parseDate(d.date);
        d.imgPath    = `${base}/architectures/${filenameMap[d.name] || "not_found.png"}`;
        d.year       = d.date.slice(0, 4);
      });
  
      categories  = Array.from(new Set(data.map(d => d.category)));
      colorScale  = d3.scaleOrdinal(d3.schemeTableau10).domain(categories);
  
      dispatch("readyLegend", { categories, colorScale });
  
      drawTimeline();
    });
  
    function drawTimeline() {
      d3.select(container).selectAll("*").remove();
  
      const margin = { top: 40, bottom: 20 };
      const width  = container.clientWidth;
      const height = container.clientHeight - margin.top - margin.bottom;
  
      const svg = d3
        .select(container)
        .append("svg")
        .attr("width", width)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${width / 2},${margin.top})`);
  
      const minDate = d3.min(data, d => d.parsedDate);
      const maxDate = d3.max(data, d => d.parsedDate);
      const yScale  = d3
        .scaleTime()
        .domain([minDate, maxDate])
        .range([height, 0]);
  
      svg
        .append("line")
        .attr("x1", 0).attr("x2", 0)
        .attr("y1", 0).attr("y2", height)
        .attr("stroke", "#ccc")
        .attr("stroke-width", 2);
  
      svg
        .selectAll("circle")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", 0)
        .attr("cy", d => yScale(d.parsedDate))
        .attr("r", 8)
        .attr("fill", d => colorScale(d.category))
        .style("cursor", "pointer")
        .on("mouseover", (event, d) => {
          dispatch("hover", d);
        })
        .on("mouseout", () => {
          dispatch("hover", null);
        })
        .on("click", (event, d) => {
          event.stopPropagation();
          dispatch("select", d);
        });
  
      svg
        .selectAll("text.model-label")
        .data(data)
        .enter()
        .append("text")
        .attr("class", "model-label")
        .attr("x", 12)
        .attr("y", d => yScale(d.parsedDate) + 4)
        .text(d => `${d.name} (${d.year})`)
        .attr("font-size", "10px")
        .attr("fill", "#333")
        .style("user-select", "none");
    }
  </script>
  
  <style>
    .wrapper {
      width: 100%;
      height: 100%;
      position: relative;
    }
  
    .timeline-container {
      width: 100%;
      height: 100%;
    }
  
    .model-label {
      pointer-events: none;
    }
  </style>
  
  <div class="wrapper">
    <div class="timeline-container" bind:this={container}></div>
  </div>
  