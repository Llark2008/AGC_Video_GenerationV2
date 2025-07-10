interface Props {
  onClick: () => void;
  disabled?: boolean;
}
export default function ExportButton({ onClick, disabled }: Props) {
  return (
    <button onClick={onClick} disabled={disabled}>
      导出视频
    </button>
  );
}
