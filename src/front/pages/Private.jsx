import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export const Private = () => {
  const [user, setUser] = useState(null);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const token = sessionStorage.getItem("token");

    if (!token) {
      navigate("/login");
      return;
    }

    const getProfile = async () => {
      const response = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/api/profile`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        sessionStorage.removeItem("token");
        navigate("/login");
        return;
      }

      setUser(data.user);
      setMessage(data.msg);
    };

    getProfile();
  }, []);

  const logout = () => {
    sessionStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="container mt-5">
      <h1>Private</h1>

      {message && <p>{message}</p>}

      {user && (
        <div>
          <p>Email: {user.email}</p>
          <p>Name: {user.name}</p>
        </div>
      )}

      <button className="btn btn-danger" onClick={logout}>
        Logout
      </button>
    </div>
  );
};