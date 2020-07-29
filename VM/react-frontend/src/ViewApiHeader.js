import React from 'react'
import {Label, IconButton, initializeIcons} from "@fluentui/react" 
import {variableHandling} from './utils'
import './componentCss/viewApiHeader.css'

export default ({setApiNameOnClick,setApiName, apiName}) => {

    initializeIcons('https://static2.sharepointonline.com/files/fabric/assets/icons/')

    const emojiIcon = { iconName: 'Edit' };

    const viewApiHeaderIconStyles = {
        root: {
            marginTop:'auto',
            marginLeft: "10px"
        },
        icon: {
            fontSize: "30px"
        }
    };

    const changeAPINameOnClick = () => {
        const newApiName = prompt("New Api Name");
        if(newApiName !== null){
            const modifiedNewApiName = variableHandling(newApiName);
            setApiName(modifiedNewApiName);
            setApiNameOnClick(modifiedNewApiName);
        }
    }
    return(
        <header className="viewApiHeader">
            <div className="viewApiHeadDiv">
                <Label className="viewApiHeaderLabel"><span className="viewApiHeaderLabelSpan">{apiName}</span></Label>
                <IconButton styles={viewApiHeaderIconStyles} iconProps={emojiIcon} title="Edit" onClick={changeAPINameOnClick} ariaLabel="Edit"/>
            </div>
        </header>
    )
}