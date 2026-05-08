import React, { useState } from "react";
import { api } from "../utils/api";

export default function Login() {

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
        const storedToken = localStorage.getItem("token");

      const response = await api(storedToken).post(
        "/auth/login",
        {
          email,
          password,
        }
      );

      const token = response.data.access_token;

      localStorage.setItem("token", token);

      alert("Login successful");

      console.log("TOKEN:", token);

    } catch (err) {

      console.error(err);

      alert("Login failed");
    }
  };

  return (
    <div>

      <h2>Login</h2>

      <form onSubmit={handleLogin}>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) =>
            setEmail(e.target.value)
          }
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />

        <button type="submit">
          Login
        </button>

      </form>

    </div>
  );
}