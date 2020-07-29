import React from 'react';
import {Label, Image} from "@fluentui/react"
import AddApi from './AddApi'
import './componentCss/NewApiStep.css'

export default ({apiName, setApiName, setApiNameOnClick}) => {
    return(
        <div>
            <header className="stepOneHeader">
                <Label className="stepOneLabel">Welcome to API Builder</Label>
            </header>
            <div className="stepOne">
                <Image 
                    src="static/react/images/step_1.png"
                    alt="Step One"
                    width={'30%'} 
                />
                <div className="stepOneAddApi">
                    <AddApi apiName={apiName} setApiName={setApiName} setApiNameOnClick={setApiNameOnClick}/>
                </div>
            </div>
        </div>
    )
}