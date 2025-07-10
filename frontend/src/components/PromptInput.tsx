import { useState } from 'react';

interface Props {
  onSubmit: (kws: string[]) => void;
  onGenerate: () => void;
}

export default function PromptInput({ onSubmit, onGenerate }: Props) {
  const [text, setText] = useState('');

  return (
    <div>
      <textarea
        rows={3}
        placeholder="输入 3‑10 个中文印象词，用空格分隔…"
        value={text}
        onChange={e => setText(e.target.value)}
        style={{ width: '100%' }}
      />
      <button
        onClick={() => {
          const kws = text.split(/\s+/).filter(Boolean);
          onSubmit(kws);
          onGenerate();
        }}
        disabled={!text.trim()}
      >
        生成 Prompt
      </button>
    </div>
  );
}
