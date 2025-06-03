// src/lib/data/loadMnistAssets.js
import * as tf from '@tensorflow/tfjs';

export async function loadModel() {
  // “/” keeps it working after SvelteKit prerender / adapter-static
  return tf.loadLayersModel('/models/mnist_model_tfjs_tiny/model.json');
}

export async function loadResume() {
  const res = await fetch('/data/mnist/resume_copy.json');
  if (!res.ok) throw new Error('Cannot fetch resume_copy.json');
  return res.json();                     // → array of {filename,label,filepath}
}

/** png → 28×28 float32 tensor in [0,1] */
export async function pngToTensor(url) {
  const img = new Image();
  img.crossOrigin = 'anonymous';
  img.src = url;
  await img.decode();

  // put into hidden canvas, read pixels, reshape
  const cvs = document.createElement('canvas');
  cvs.width = cvs.height = 28;
  const ctx = cvs.getContext('2d');
  ctx.drawImage(img, 0, 0, 28, 28);
  const { data } = ctx.getImageData(0, 0, 28, 28);
  // keep only red channel (grayscale source)
  const vals = Float32Array.from({ length: 28 * 28 }, (_, i) => data[i * 4] / 255);
  return tf.tensor(vals, [1, 28, 28, 1]);           // NHWC
}
