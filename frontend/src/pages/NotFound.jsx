import { Link } from "react-router-dom";

function NotFound() {
  return (
    <div className="not-found">
      <h1>404</h1>
      <p>This page doesn't exist.</p>
      <Link to="/" className="btn-primary">Go back home</Link>
    </div>
  );
}

export default NotFound;
