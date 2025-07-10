interface Props {
  url: string;
}
export default function MusicPlayer({ url }: Props) {
  return <audio src={url} controls style={{ width: '100%' }} />;
}
