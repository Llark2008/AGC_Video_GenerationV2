interface Props {
  urls: string[];
}
export default function ImageGallery({ urls }: Props) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 8 }}>
      {urls.map(u => (
        <img key={u} src={u} style={{ width: '100%' }} />
      ))}
    </div>
  );
}
