import { useEffect, useState } from "react";
import "./App.css";
import { api } from "./services/api";

function App() {
  const [count, setCount] = useState(0);
  useEffect(() => {
    api
      .get("/count")
      .then((response) => {
        setCount(response.data.count);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <>
      <h1>{import.meta.env.VITE_HELLO}</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count} candy
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
    </>
  );
}

export default App;
