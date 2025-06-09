<script>
  import { fly } from 'svelte/transition';
  export let data = [];
  
  // Find the index of the max probability
  $: maxIdx = data.length ? data.indexOf(Math.max(...data)) : -1;
  
  // For display, format as percentage
  function formatProb(p) {
    return (p * 100).toFixed(1) + '%';
  }
</script>

<style>
.chart {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.bar-row {
  display: flex;
  align-items: center;
  gap: 8px;
}
.label {
  width: 24px;
  text-align: right;
  font-weight: bold;
  color: #444;
}
.bar-container {
  flex: 1;
  background: #f0f0f0;
  border-radius: 6px;
  overflow: hidden;
  height: 28px;
  position: relative;
}
.bar {
  height: 100%;
  background: #4f8ef7;
  border-radius: 6px 0 0 6px;
  transition: width 0.5s cubic-bezier(0.4,0,0.2,1);
}
.bar.highlight {
  background: #f7b84f;
  box-shadow: 0 0 8px #f7b84f88;
}
.value {
  min-width: 48px;
  text-align: left;
  font-size: 0.95em;
  color: #222;
  margin-left: 8px;
}
</style>

<div class="chart">
  {#each data as prob, i}
    <div class="bar-row">
      <span class="label">{i}</span>
      <div class="bar-container">
        <div
          class="bar {i === maxIdx ? 'highlight' : ''}"
          style="width: {Math.max(0, prob * 100)}%"
          transition:fly|local={{ x: -20, duration: 300 }}
        ></div>
      </div>
      <span class="value">{formatProb(prob)}</span>
    </div>
  {/each}
</div>
