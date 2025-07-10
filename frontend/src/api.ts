import axios from 'axios';

export async function postPrompts(keywords: string[]) {
  const { data } = await axios.post('/prompts', { keywords });
  return data.prompts as string[];
}

export async function postImages(prompts: string[], lora?: string) {
  const { data } = await axios.post('/images', { prompts, lora });
  return data.urls as string[];
}

export async function postMusic(mood: string, duration: number) {
  const { data } = await axios.post('/music', { mood, duration_sec: duration });
  return data.url as string;
}

export async function postRender(images: string[], music: string, title: string, author: string) {
  const { data } = await axios.post('/render', { images, music, title, author });
  return data.url as string;
}

export async function listLora() {
  const { data } = await axios.get('/lora/list');
  return data as string[];
}
