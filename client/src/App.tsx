import { useEffect, useState } from "react";
import { api } from "./services/api";
import { Feature } from "./types";
import FeatureCardList from "./components/feature-card-list";
import { Route, Routes, useNavigate } from "react-router-dom";
import FeatureCardDetailView from "./components/feature-card-detail-view";

// Define the structure of the API response
interface FeaturesApiResponse {
  [key: string]: Feature; // The keys will be "feature:<id>", and the value will be the Feature object
}

export function App() {
  const [features, setFeatures] = useState<Feature[]>([]); // Features state is an array of Feature objects
  const navigate = useNavigate();

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

  const handleFeatureClick = (id: string) => {
    navigate(`/features/${id}`);
  };


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
              onFeatureClick={handleFeatureClick}
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
      
    </Routes>
  );
}

