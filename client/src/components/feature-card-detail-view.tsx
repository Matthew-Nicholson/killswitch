import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { api } from "../services/api";
import { Feature } from "../types";
import { Button } from "@nextui-org/button";

function FeatureCardDetailView() {
  const { id } = useParams<{ id: string }>(); 
  const [feature, setFeature] = useState<Feature | null>(null);

  useEffect(() => {
    api
      .get<Feature>(`/feature/${id}`)
      .then((response) => setFeature(response.data))
      .catch((error) => console.error(error));
  }, [id]);

  if (!feature) {
    return <p>Loading feature details...</p>;
  }

  return (
    <div>
        <Link to='/'><Button>Back</Button></Link>
        <div>
        <h1>{feature.data.title}</h1>
        <p>{feature.data.description}</p>

        </div>
    </div>
  );
}

export default FeatureCardDetailView;
