import React from 'react'
import AttributeListItem from './AttributeListItem'
import {PrimaryButton} from '@fluentui/react'
import './componentCss/Modal.css'

export default ({ attributeListItemArr, addAttributeButtonOnClick, deleteAttributeButtonOnClick, onChangeAttribute}) => {
    const attrArr = Object.keys(attributeListItemArr).map((attr) => {
        const name = attributeListItemArr[attr].name;
        const type = attributeListItemArr[attr].type; 
        return <AttributeListItem id={attr} name={name} type={type} onChangeAttribute={onChangeAttribute} deleteAttributeButtonOnClick = {deleteAttributeButtonOnClick} disabled={false}/> 
    })
    return (
        <div>
            <div style={{overflowY: "scroll", maxHeight:"300px"}}>
                <AttributeListItem name='id' type='number' disabled={true} />
                {attrArr}
            </div>
            <div className="modalAddNewAttributeButtonDiv">
                <PrimaryButton className="modalAddNewAttributeButton" onClick={addAttributeButtonOnClick}  text="+ Attribute" allowDisabledFocus />
          </div>
        </div>
    )
}