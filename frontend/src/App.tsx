import { useState } from 'react';
import { postPrompts, postImages, postMusic, postRender, listLora } from './api';
import PromptInput from './components/PromptInput';
import PromptList from './components/PromptList';
import ImageGallery from './components/ImageGallery';
import MusicPlayer from './components/MusicPlayer';
import ExportButton from './components/ExportButton';

export default function App() {
  const [keywords, setKeywords] = useState<string[]>([]);
  const [prompts, setPrompts] = useState<string[]>([]);
  const [images, setImages] = useState<string[]>([]);
  const [music, setMusic] = useState<string | null>(null);
  const [video, setVideo] = useState<string | null>(null);
  const [loraOpts, setLoraOpts] = useState<string[]>([]);

  async function handleGeneratePrompts() {
    setPrompts(await postPrompts(keywords));
  }

  async function handleGenerateImages() {
    if (prompts.length) {
      if (!loraOpts.length) setLoraOpts(await listLora());
      setImages(await postImages(prompts.slice(0, 10)));
    }
  }

  async function handleGenerateMusic() {
    setMusic(await postMusic('cinematic', 60));
  }

  async function handleRender() {
    if (images.length && music) {
      setVideo(await postRender(images, music, 'My AI Video', 'Me'));
    }
  }

  return (
    <div className="container" style={{ maxWidth: '960px', margin: 'auto' }}>
      <h1>AI 二创视频自动生成</h1>
      <PromptInput onSubmit={setKeywords} onGenerate={handleGeneratePrompts} />
      <PromptList prompts={prompts} />
      <button onClick={handleGenerateImages} disabled={!prompts.length}>
        生成图片
      </button>
      <ImageGallery urls={images} />
      <button onClick={handleGenerateMusic}>生成 BGM</button>
      {music && <MusicPlayer url={music} />}
      <ExportButton onClick={handleRender} disabled={!images.length || !music} />
      {video && (
        <video src={video} controls style={{ width: '100%' }}>
          您的浏览器不支持视频播放。
        </video>
      )}
    </div>
  );
}
