import React from 'react'
import CurrentRouteGroupsList from './CurrentRouteGroupsList';
import { Label } from '@fluentui/react';
import './componentCss/CurrentRouteGroups.css'

export default ({onRouteGroupDelete,onRouteGroupNameChange,arrayOfRouteGroups}) => {
    return(
        <div className="currentRouteGroupsMainDiv">
            <header>
                <Label className="currentRouteGroupsLabel">Route Groups</Label>
            </header>
            <div>
                <CurrentRouteGroupsList  onRouteGroupDelete={onRouteGroupDelete} onRouteGroupNameChange={onRouteGroupNameChange} arrayOfRouteGroups={arrayOfRouteGroups}/>
            </div>
        </div>
    )
}