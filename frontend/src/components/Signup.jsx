import React, { useState } from "react";
import { api } from "../utils/api";

export default function Signup() {

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignup = async (e) => {

    e.preventDefault();

    try {
        const storedToken = localStorage.getItem("token");

      await api(storedToken).post(
        "/auth/signup",
        {
          email,
          password,
        }
      );

      alert("Signup successful");

    } catch (err) {

      console.error(err);

      alert("Signup failed");
    }
  };

  return (
    <form onSubmit={handleSignup}>

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
        Signup
      </button>

    </form>
  );
}