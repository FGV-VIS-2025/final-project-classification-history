<script>
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
</style>
