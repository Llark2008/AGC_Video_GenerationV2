interface Props {
  prompts: string[];
}
export default function PromptList({ prompts }: Props) {
  return (
    <ul>
      {prompts.map(p => (
        <li key={p}>{p}</li>
      ))}
    </ul>
  );
}
