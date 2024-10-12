import React from 'react'
import { Feature } from '../types'
import FeatureCard from './feature-card';

interface FeatureCardListProps{
    features: Feature[];
}

const FeatureCardList: React.FC<FeatureCardListProps> = ({features}) => {
    return(
        <div>
            {features.map((feature) => (
                <FeatureCard key={feature.id} feature={feature} />
            ))}
        </div>
    )
}

export default FeatureCardList