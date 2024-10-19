import { useEffect, useState } from "react";
import { api } from "./services/api";
import { Feature } from "./types";
import FeatureCardList from "./components/feature-card-list";
import { Route, Routes } from "react-router-dom";
import FeatureCardDetailView from "./components/feature-card-detail-view";
import EditFeature from "./components/edit-feature";

interface FeaturesApiResponse {
  [key: string]: Feature;
}

export function App() {
  const [features, setFeatures] = useState<Feature[]>([]);
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
    <Routes>
      <Route
      path="/"
      element={
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
              <FeatureCardList 
              features={features}
              />
            </ul>
          ) : (
            <p>No features available.</p>
          )}
        </section>
      </>
      }
      />

      <Route path="/feature/:id" element={<FeatureCardDetailView />} />
      <Route path="/feature/:id/edit" element={<EditFeature/>}/>
      
    </Routes>
  );
}

