import { useEffect, useState } from "react";
import { api } from "./services/api";
import { Button } from "@nextui-org/button";
import { Feature } from "./types";
import FeatureCardList from "./components/feature-card-list";

// Define the structure of the API response
interface FeaturesApiResponse {
  [key: string]: Feature; // The keys will be "feature:<id>", and the value will be the Feature object
}

export function App() {
  const [features, setFeatures] = useState<Feature[]>([]); // Features state is an array of Feature objects
  useEffect(() => {
    api
    .get<FeaturesApiResponse>("/features")
    .then((response) => {
      const featuresArray: Feature[] = Object.values(response.data);
      setFeatures(featuresArray);

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
        <h2>Features List</h2>
        {features.length > 0 ? (
          <ul>
            <FeatureCardList features={features}/>
          </ul>
        ) : (
          <p>No features available.</p>
        )}
      </section>
    </>
  );
}

