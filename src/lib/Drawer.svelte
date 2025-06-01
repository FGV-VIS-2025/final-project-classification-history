<script>
  import { onMount } from 'svelte';

  const matrixSize = 28;
  const pointerSize = 1;
  export let canvasSize = 400;
  let canvasSizePx;
  $: canvasSizePx = canvasSize / matrixSize;

  export let pixelMatrix = Array(matrixSize).fill(null).map(() => Array(matrixSize).fill(0));

  const backgroundColor = 'black';
  const foregroundColor = 'white';

  let canvasElement;
  let ctx;

  onMount(() => {
    ctx = canvasElement.getContext('2d');
    clearCanvas();
  });

  function drawPixel(x, y, color) {
    if (ctx) {
      ctx.fillStyle = color;
      // Draw a square centered at (x, y) with side length pointerSize*2+1
      for (let dx = -pointerSize; dx <= pointerSize - 1; dx++) {
      for (let dy = -pointerSize; dy <= pointerSize - 1; dy++) {
        const px = x + dx;
        const py = y + dy;
        if (px >= 0 && px < matrixSize && py >= 0 && py < matrixSize) {
        ctx.fillRect(px, py, 1, 1);
        pixelMatrix[py][px] = (color === foregroundColor) ? 1 : 0;
        }
      }
      }
    }
  }

  function getMousePos(evt) {
    const rect = canvasElement.getBoundingClientRect();
    return {
      x: evt.clientX - rect.left,
      y: evt.clientY - rect.top
    };
  }

  let drawing = false;
  let erasing = false;

  function startDrawing(evt) {
    drawing = true;
    erasing = false;
  }

  function startErasing(evt) {
    erasing = true;
    drawing = false;
  }

  function stopActions() {
    drawing = false;
    erasing = false;
  }

  function draw(evt) {
    if (!drawing && !erasing) return;
    const pos = getMousePos(evt);
    const x = Math.floor(pos.x / (canvasSize / matrixSize));
    const y = Math.floor(pos.y / (canvasSize / matrixSize));
    drawPixel(x, y, erasing ? backgroundColor : foregroundColor);
  }

  function clearCanvas() {
    ctx.fillStyle = backgroundColor;
    ctx.fillRect(0, 0, canvasSize, canvasSize);
    pixelMatrix = Array(matrixSize).fill(null).map(() => Array(matrixSize).fill(0));
  }

</script>

<div class="drawer">
  <div class="drawer-container">
    <canvas
      bind:this={canvasElement}
      width={matrixSize}
      height={matrixSize}
      on:mousedown={e => { if (e.button === 0) startDrawing(e); }}
      on:mousemove={e => { if (e.buttons === 1 && drawing) draw(e); else if (e.buttons === 2 && erasing) draw(e); }}
      on:mouseup={stopActions}
      on:mouseleave={stopActions}
      on:contextmenu|preventDefault={startErasing}
      class="drawer-canvas"
      style="
        width: {canvasSize}px;
        height: {canvasSize}px;
        image-rendering: pixelated;
        image-rendering: -moz-crisp-edges; /* Firefox */
        image-rendering: crisp-edges; /* Old Chrome, Safari */
      "	
    ></canvas>
  </div>

  <div class="controls">
    <button on:click={clearCanvas} aria-label="Clear Drawing">
      <img src="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/icons/trash.svg" alt="Clear" width="20" height="20" style="vertical-align: middle;" />
    </button>
  </div>
</div>

<style>
  .drawer {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 10px;
  }

  .controls button {
    border: none;
    width: 40px;
    height: 40px;
    cursor: pointer;
  }

  .controls button img {
    width: 100%;
    height: 100%;
  }

  .drawer-container {
    display: inline-block;
    border: 1px solid #ccc;
  }

  .drawer-canvas {
    display: block;
  }
</style>