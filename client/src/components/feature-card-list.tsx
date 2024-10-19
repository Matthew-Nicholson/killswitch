import React from 'react'
import { Feature } from '../types'
import FeatureCard from './feature-card';
import { Link } from 'react-router-dom';
import { Button } from '@nextui-org/button';

interface FeatureCardListProps{
    features: Feature[];
    onFeatureClick: (id: string) => void; // Function to handle click event
}

const FeatureCardList: React.FC<FeatureCardListProps> = ({features}) => {
    return(
        <div>
            {features.map((feature) => (
                <div className="feature-card">
                    <FeatureCard feature={feature} />
                    <Link key={feature.id} to={`feature/${feature.id}`}>
                        <Button>Edit</Button>
                    </Link>
                </div>
            ))}
        </div>
    )
}

export default FeatureCardList