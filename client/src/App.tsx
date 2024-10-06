import { useEffect, useState } from "react";
import { api } from "./services/api";
import { Button } from "@nextui-org/button";

export function App() {
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
      <h1>Vite + React + NextUI + TypeScript + ESLint + Prettier</h1>
      <br />
      <section>
        <h2>Testing Vite env:</h2>
        <p>{import.meta.env.VITE_HELLO}</p>
      </section>
      <br />
      <section>
        <h2>Testing API:</h2>
        <p>Count should be 69420. Actual count: {count}</p>
        {count === 0 && "Something is wrong: Make sure the API is running"}
      </section>
      <br />
      <section>
        <h2>Testing NextUI:</h2>
        <Button>Click me!</Button>
      </section>
    </>
  );
}
