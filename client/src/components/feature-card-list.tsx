import React from 'react'
import { Feature } from '../types'
import FeatureCard from './feature-card';
import { Link } from 'react-router-dom';
import { Button } from '@nextui-org/button';

interface FeatureCardListProps{
    features: Feature[];
}

const FeatureCardList: React.FC<FeatureCardListProps> = ({features}) => {
    return(
        <div>
            {features.map((feature) => (
                <div className="feature-card">
                    <FeatureCard feature={feature} />
                    <Link key={feature.id} to={`feature/${feature.id}/edit`}>
                        <Button>Edit</Button>
                    </Link>
                </div>
            ))}
        </div>
    )
}

export default FeatureCardList