import React, {useState, useEffect} from 'react'
import {Dropdown, IconButton, initializeIcons} from '@fluentui/react'
import './componentCss/AttributeListItem.css'

export default ({id, name, type, deleteAttributeButtonOnClick, onChangeAttribute, disabled}) => {
    initializeIcons('https://static2.sharepointonline.com/files/fabric/assets/icons/')
    const [inputVal, setInputVal] = useState(name)
    const [inputType, setInputType] = useState(type)

    useEffect( () => {
        setInputVal(name)
    }, [name])

    const options = [
        { key: 'number', text: 'number' },
        { key: 'decimal', text: 'decimal' },
        { key: 'word(s)', text: 'word(s)'},
        { key: 'true / false', text: 'true / false' },
        { key: 'date and time', text: 'date and time' },
    ];

    let defaultProps = {
        defaultSelectedKey : type
    }
    if(type === ''){
        defaultProps = {}
    }

    const deleteIcon = { iconName: 'Delete' };

    const iconStyles = {
        icon: {
          fontSize: "20px",
        },
      };
    const dropdownStyles = {
        dropdown: { width: 300, fontSize:"20px" },
    };

    return (
        <div className="attributeListItemMainDiv">
            <input type="text" className="attributeListItemInput" name="attributeName" disabled={disabled} placeholder="Enter Attribute Name" value={inputVal} onChange= {(e) => {
                setInputVal(e.target.value)
                onChangeAttribute(id, e.target.value, inputType)}
                } />
            <div className="attributeListItemDropdownDiv">
                <Dropdown
                    placeholder="Type"
                    {...defaultProps}
                    options={options}
                    styles={dropdownStyles}
                    onChange={(e, selectedKey) => {
                        setInputType(selectedKey.key)
                        onChangeAttribute(id, inputVal,selectedKey.key)
                    }}
                    disabled={disabled}
                />
                <IconButton iconProps={deleteIcon} styles={iconStyles} title="Delete" ariaLabel="Delete" disabled={disabled} onClick={(e) => {deleteAttributeButtonOnClick(id)}}/>
            </div>
        </div>
    )
}