import React from 'react';
import {Label, PrimaryButton} from '@fluentui/react'
import CurrentApisList from './CurrentApisList'
import './componentCss/CurrentApis.css'

export default () => {
    return (
        <div className="currentApisContainerDiv">
            <div className="currentApisButtonDiv">
                <Label className="currentApisLabel">APIs</Label>
                <PrimaryButton className="currentApisPrimaryButton" text="+ New API"/>
            </div>
            <div>
                <CurrentApisList />
            </div>
        </div>
    )
}