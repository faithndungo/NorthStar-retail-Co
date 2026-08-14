export default function ErrorNotice({ message }) {
  if (!message) return null;
  return (
    <div className="notice error" role="alert">
      {message}
    </div>
  );
}