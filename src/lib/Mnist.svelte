<script>
  import { onMount } from "svelte";
  import { base } from "$app/paths";
  let images = [];
  const gridSize = 5;
  let cells = [];

  let digitImages = Array(10).fill([]);
  let selectorImages = Array(10).fill(null);
  let selectedDigit = 0;

  async function loadImages() {
    const res = await fetch(`${base}/data/mnist/resume.json`);
    images = await res.json();
    digitImages = Array(10)
      .fill()
      .map((_, d) => images.filter((img) => img.label === d));
    selectorImages = digitImages.map((imgs) => imgs[0]);
  }

  onMount(() => {
    loadImages();
  });
</script>

<div class="mnist">
  <div class="mnist-selector">
    {#each selectorImages as img, d}
      {#if img}
        <img
          src={`${base}/${img.filepath}`}
          alt={`Digit ${d}`}
          class:selected={selectedDigit === d}
          on:click={() => (selectedDigit = d)}
          style="cursor:pointer;margin:2px;border-radius:4px;border:2px solid {selectedDigit === d ? '#007bff' : '#ccc'};background:#fff;"
          aria-hidden="true"
        />
      {/if}
    {/each}
  </div>
  {#if selectedDigit !== null}
    <div class="mnist-examples">
      {#each digitImages[selectedDigit] as img}
        <img
          src={`${base}/${img.filepath}`}
          alt={img.filename}
          width="56"
          height="56"
          style="margin:4px;border-radius:4px;background:#fff;border:1px solid #ccc;"
        />
      {/each}
    </div>
  {/if}
</div>

<style>
  .mnist {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 1rem auto;
    max-width: 800px;
  }
  .mnist-selector {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 1rem;
    gap: 4px;
  }
  .mnist-selector img {
    width: 56px;
    height: 56px;
    border-radius: 10px;
    border: 4px solid;
    cursor: pointer;
    transition: border-color 0.3s, box-shadow 0.3s;
  }
  .mnist-selector img.selected {
    border-color: #007bff;
    box-shadow: 0 0 4px #007bff88;
  }

  .mnist-examples {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-template-rows: repeat(2, 1fr);
  }

  .mnist-examples img {
    width: 150px;
    height: 150px;
    aspect-ratio: 1 / 1;
  }
</style>
