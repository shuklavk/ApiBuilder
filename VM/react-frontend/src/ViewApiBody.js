import React from 'react'
import CurrentRouteGroups from './CurrentRouteGroups'
import {Image} from "@fluentui/react" 
import './componentCss/ViewApiBody.css'

export default ({onRouteGroupDelete, onRouteGroupNameChange,arrayOfRouteGroups}) => {
    return (
        <div>
            <div className="viewApiRGImageDiv">
                <Image 
                    src="static/react/images/step_2.png"
                    alt="Step Two"
                    width={'432px'}
                    height={'576px'} 
                />
                <div className="viewApiRGDiv">
                    <CurrentRouteGroups  onRouteGroupDelete={onRouteGroupDelete} onRouteGroupNameChange={onRouteGroupNameChange} arrayOfRouteGroups={arrayOfRouteGroups} />
                </div>
            </div>
        </div>
    )
}