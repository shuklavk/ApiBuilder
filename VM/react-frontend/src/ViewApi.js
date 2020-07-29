import React from 'react'
import ViewApiHeader from './ViewApiHeader'
import ViewApiBody from './ViewApiBody'
import ViewApiFooter from './ViewApiFooter'


export default ({setApiNameOnClick, setApiName,onRouteGroupDelete, onRouteGroupNameChange,arrayOfRouteGroups, apiName}) => {
    return (
        <div>
            <ViewApiHeader setApiNameOnClick={setApiNameOnClick} setApiName={setApiName} apiName={apiName}/>
            <ViewApiBody onRouteGroupDelete={onRouteGroupDelete} onRouteGroupNameChange={onRouteGroupNameChange} arrayOfRouteGroups={arrayOfRouteGroups}/>
            <ViewApiFooter />
        </div>
    )
}