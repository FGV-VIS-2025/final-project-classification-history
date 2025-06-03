<script>
  import { onMount, onDestroy } from "svelte";
  import { base } from "$app/paths";
  let images = [];
  const gridSize = 5;
  let cells = [];
  const minInterval = 2000;
  const maxInterval = 4000;

  function getRandomImage() {
    if (images.length === 0) return null;
    return images[Math.floor(Math.random() * images.length)];
  }

  function getRandomDelay() {
    return Math.floor(Math.random() * (maxInterval - minInterval + 1)) + minInterval;
  }

  function startCellInterval(cell, idx) {
    if (cell.intervalId) clearInterval(cell.intervalId);
    const update = () => {
      cell.img = getRandomImage();
      cells = [...cells];
    };
    const delay = getRandomDelay();
    cell.intervalId = setInterval(() => {
      update();
      clearInterval(cell.intervalId);
      startCellInterval(cell, idx);
    }, delay);
  }

  async function loadImages() {
    const res = await fetch(`${base}/data/mnist/resume_copy.json`);
    images = await res.json();
    cells = Array.from({ length: gridSize * gridSize }, () => ({ img: getRandomImage(), intervalId: null }));
    cells.forEach((cell, idx) => startCellInterval(cell, idx));
  }

  onMount(() => {
    loadImages();
  });

  onDestroy(() => {
    cells.forEach(cell => cell.intervalId && clearInterval(cell.intervalId));
  });
</script>

<div class="grid">
  {#each cells as cell}
    <div class="cell">
      {#if cell.img}
        <img src={cell.img.filepath.replace("static/", "/")} alt={cell.img.filename} />
      {/if}
    </div>
  {/each}
</div>

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(5, max-content);
    justify-items: center;
    align-items: center;
  }
  .cell {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  img {
    width: calc(28 * 4px);
    aspect-ratio: 1 / 1;
    object-fit: contain;
    background: #fff;
  }
</style>
