import React from "react"
import { Button } from "@nextui-org/button";
import { Feature } from "../types";

interface FeatureCardProps {
feature: Feature;
}

const FeatureCard: React.FC<FeatureCardProps> = ({feature}) => {
    const {title,description,enabled,roll_out} = feature;
    return(
        <div className="feature-card">
            <h3>{title}</h3>
            <p>{description}</p>
            <p>Roll Out: {roll_out}%</p>
            <Button>{enabled == '1' ? 'Enabled' : 'Disabled'}</Button>
            <Button>Edit</Button>
        </div>
    )
}

export default FeatureCard