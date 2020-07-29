import React, {useState} from 'react'
import CurrentRouteGroupListItem from './CurrentRouteGroupsListItem'
import { PrimaryButton } from '@fluentui/react';
import { useBoolean } from '@uifabric/react-hooks';
import Modal from './Modal'
import './componentCss/CurrentRouteGroupsList.css'

export default ({onRouteGroupDelete, onRouteGroupNameChange, arrayOfRouteGroups}) => {
    const [isModalOpen, { setTrue: showModal, setFalse: hideModal }] = useBoolean(false);
    const [data, setData] = useState({})
    const [RGName, setRGName] = useState("");
    const [id, setId] = useState(-1);
    const [newRGCounter, setNewRGCounter] = useState(-1);

    
    const itemArrInfo = arrayOfRouteGroups.map(routeGroup => {
        return <CurrentRouteGroupListItem id={routeGroup.id} onRouteGroupDelete={onRouteGroupDelete} setId={setId} setRGName={setRGName} data={routeGroup.attributes} RGName={routeGroup.objectName} setData={setData} showModal={showModal}/>
    })
    const addAttributeButtonOnClick = () => {
        setRGName("");
        setData({})
        setId(newRGCounter);
        setNewRGCounter(newRGCounter - 1);
        showModal();
    }


    return (
        <div className="currentRouteGroupsListMainDiv">
            <ul className="currentRouteGroupsListUl">
                {itemArrInfo}
            </ul>
            <div className="currentRouteGroupsPrimaryButtonDiv">
                <PrimaryButton onClick={addAttributeButtonOnClick} className="currentRouteGroupsPrimaryButton"> + Route Group</PrimaryButton>
                <Modal id={id} onRouteGroupNameChange={onRouteGroupNameChange} data={data} RGName={RGName} showModal={showModal} hideModal={hideModal} isModalOpen={isModalOpen} />
            </div>
        </div>
    )
}