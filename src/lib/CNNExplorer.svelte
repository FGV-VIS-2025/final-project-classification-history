<!-- <script>
  // Components
  import Drawer from "$lib/components/Drawer.svelte";
  import CNNExplorer from "$lib/charts/CNNExplorer.svelte";

  let pixelMatrix;
</script>

<div class="cnn-explorer">
  <CNNExplorer bind:pixelMatrix/>
  <Drawer bind:pixelMatrix />
</div>

<style>
  .cnn-explorer {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
  }
</style> -->




<!-- <script>
  // Components
  import Drawer from "$lib/components/Drawer.svelte";
  import CNNArchViz from "$lib/charts/CNNArchViz.svelte";

  // This variable is the bridge between the two components
  let pixelMatrix;
</script>

<div class="interface-container">
  <div class="drawer-panel">
    <div class="panel-header">
      <h2>1. Draw a Digit</h2>
      <p>Draw a single number from 0 to 9 in the box below. The model will try to guess what you drew.</p>
    </div>
    <Drawer bind:pixelMatrix />
  </div>

  <div class="viz-panel">
     <div class="panel-header">
      <h2>2. See the Network Think</h2>
      <p>Follow your drawing as it's processed through the network layers.</p>
    </div>
    <CNNArchViz bind:pixelMatrix/>
  </div>
</div>

<style>
  .interface-container {
    display: flex;
    flex-direction: row;
    gap: 2rem;
    width: 100%;
    height: 100%;
    padding: 1rem;
    align-items: stretch; /* Makes panels equal height */
  }

  .drawer-panel {
    flex: 0 0 320px; /* Fixed width for the drawing panel */
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .viz-panel {
    flex: 1 1 auto; /* The visualization panel takes the rest of the space */
    display: flex;
    flex-direction: column;
    gap: 1rem;
    min-width: 0; /* Important for flexbox to allow shrinking */
  }

  .panel-header {
    padding: 1rem;
    background: rgba(0, 170, 255, 0.05);
    border: 1px solid rgba(0, 170, 255, 0.1);
    border-radius: 8px;
    color: var(--color-text);
  }

  .panel-header h2 {
    margin: 0 0 0.5rem 0;
    font-size: 1.2rem;
    color: var(--color-primary);
  }
  
  .panel-header p {
    margin: 0;
    font-size: 0.9rem;
    line-height: 1.4;
    text-indent: 0;
    color: var(--color-text);
    opacity: 0.9;
  }
</style> -->

<script>
  import Drawer from "$lib/components/Drawer.svelte";
  // Correctly import the visualization from its new path
  import CNNExplorer from "$lib/charts/CNNArchviz.svelte";

  let pixelMatrix;
</script>

<div class="interface-container">
  <div class="drawer-panel">
    <div class="panel-header">
      <h2>1. Draw a Digit</h2>
      <p>Draw a single number from 0 to 9. The model will try to guess what it is after you pause.</p>
    </div>
    <Drawer bind:pixelMatrix />
  </div>

  <div class="viz-panel">
     <div class="panel-header">
      <h2>2. See the Network Think</h2>
      <p>Follow your drawing as it's processed through the network's layers.</p>
    </div>
    <CNNExplorer bind:pixelMatrix/>
  </div>
</div>

<style>
  .interface-container {
    display: flex;
    flex-direction: row;
    gap: 2rem;
    width: 100%;
    height: 100%;
    padding: 1rem;
    align-items: stretch;
  }

  .drawer-panel {
    flex: 0 0 320px; /* Give the drawer a fixed width */
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .viz-panel {
    flex: 1 1 auto; /* Let the visualization panel grow to fill the space */
    display: flex;
    flex-direction: column;
    gap: 1rem;
    min-width: 0;
  }

  .panel-header {
    padding: 1rem;
    background: rgba(0, 170, 255, 0.05);
    border: 1px solid rgba(0, 170, 255, 0.1);
    border-radius: 8px;
    color: var(--color-text);
    flex-shrink: 0;
  }

  .panel-header h2 { margin: 0 0 0.5rem 0; font-size: 1.2rem; color: var(--color-primary); }
  .panel-header p { margin: 0; font-size: 0.9rem; line-height: 1.4; text-indent: 0; color: var(--color-text); opacity: 0.9; }

  /* Ensure the child components inside the panel take up available space */
  :global(.viz-panel > *) {
    flex-grow: 1;
    min-height: 0;
  }
</style>