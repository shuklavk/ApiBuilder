import React, {useState} from 'react';
import { Label, PrimaryButton } from '@fluentui/react';
import { useId } from '@uifabric/react-hooks';
import {variableHandling} from './utils'
import './componentCss/AddApi.css'

export default ({apiName ,setApiName, setApiNameOnClick}) => {
    const textFieldId = useId('addApi');
    const [newApiName, setNewApiName] = useState("")

    const startBuildingOnClick = () => {
        const modifiedVariable = variableHandling(newApiName)
        setApiName(modifiedVariable);
        setApiNameOnClick(modifiedVariable) 
    }
    return (
        <div className='addApi'>
            <Label className='addApiLabel' htmlFor={textFieldId}>Create a new API</Label>
            <input id={textFieldId} className='addApiTextfield' value={newApiName} onChange={(e) => {setNewApiName(e.target.value)}} placeholder="Enter your API name" required />
            <PrimaryButton className='addApiButton' onClick={startBuildingOnClick}> Start Building </PrimaryButton>
        </div>
    );
};
