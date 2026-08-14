export default function FakeQr({ value }) {
  const size = 21;
  let hash = 0;

  String(value).split('').forEach((ch) => {
    hash = (hash * 31 + ch.charCodeAt(0)) % 233280;
  });

  const cells = [];
  for (let i = 0; i < size * size; i += 1) {
    hash = (hash * 1103515245 + 12345) % 2147483648;
    cells.push(hash % 3 !== 0);
  }

  return (
    <svg className="qr" viewBox={`0 0 ${size} ${size}`} role="img" aria-label={`QR for ${value}`}>
      {cells.map((filled, i) =>
        filled ? (
          <rect key={i} x={i % size} y={Math.floor(i / size)} width="1" height="1" />
        ) : null
      )}
    </svg>
  );
}