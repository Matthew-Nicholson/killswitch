import React, { useEffect, useState } from 'react'
import { redirect, useNavigate, useParams } from 'react-router-dom'
import { Feature } from '../types'
import { api } from '../services/api'
import { Button } from '@nextui-org/button'
import { toast, ToastContainer } from 'react-toastify'; // Import Toastify
import 'react-toastify/dist/ReactToastify.css'; // Import Toastify CS

const EditFeature: React.FC = () => {
    const {id} = useParams<{id: string}>()
    const navigate = useNavigate();
    const [feature,setFeature] = useState<Feature>();
    const [isLoading,setIsLoading] = useState<boolean>(true)
    const [updateData,setUpdateData] = useState<Feature>();
    const [isEnabled, setIsEnabled] = useState<boolean>(false);
    useEffect(()=> {
        api
        .get<{data: Feature}>(`/feature/${id}`)
        .then((response)=> {
            const featureData = response.data.data; // Access the actual feature data
            if(!featureData)
            {
                navigate("/")
            }
            else{
                setFeature(featureData)
                setUpdateData(featureData)
                setIsEnabled(featureData.enabled == '1' ? true : false);
            }
        }).catch((error)=> {
            navigate("/")
            console.log(error)
        })
        setIsLoading(false)
    }, [id])

    if(isLoading)
    {
        return <p>Loading...</p>
    }

    // if(!feature)
    // {
    //     return redirect("/");
    // }

    
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if(updateData)
        {

            console.log(updateData)
            api
            .put(`/feature/${feature?.id}`, {updateData})
            .then((response)=> {
                const data = response.data
                console.log(data)
                toast.success(data.message, {
                    position: 'top-center'
                  });
            })
            .catch((error) => {
                console.error(error);
              });
        }

    }
    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const {name,value} = e.target;
        if(updateData)
        {
            setUpdateData({...updateData,[name]:value})
        }
    }

    const handleToggle = () => {
        const newEnabledState = !isEnabled;
        setIsEnabled(newEnabledState);
    
        // Update the enabled field in the updatedData object
        if (updateData) {
          setUpdateData({
            ...updateData,
            enabled: newEnabledState ? 'True' : 'False', 
          });
        }
      };

    
    return(
        <div>
            <Button onClick={()=> navigate("/")}>Back</Button>
            <h1>Edit Feature</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Title: </label>
                    <input
                    type="text"
                    name='title'
                    value={updateData?.title || ''}
                    onChange={handleInputChange}
                    />
                </div>
                <label>Description: </label>
                <div>
                    <textarea 
                    name="description"
                    value={updateData?.description || ''}
                    onChange={handleInputChange}
                    rows={4}
                    cols={40}
                    />
                </div>
                <div>
                    <label>Roll Out: </label>
                    <input
                    type='text'
                    name="roll_out"
                    value={updateData?.roll_out || ''}
                    onChange={handleInputChange}
                    />
                </div>

                <div>
                    <Button onClick={handleToggle} color={isEnabled ? 'success' : 'danger'}>
                        {isEnabled ? 'Enabled' : 'Disabled'}
                    </Button>
                </div>
                <Button type='submit' color='primary'>Save Changes</Button>
            </form>
            <ToastContainer />
        </div>
    )
    
}
export default EditFeature