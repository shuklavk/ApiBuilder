import React, {useState} from 'react'
import { PrimaryButton, ChoiceGroup, initializeIcons } from '@fluentui/react';
import {generateFullAPI} from './utils'
import './componentCss/ViewApiFooter.css'

export default () => {
    initializeIcons('https://static2.sharepointonline.com/files/fabric/assets/icons/')
    const options = [
        { key: 'flask', text: 'Flask', iconProps: { iconName: 'PythonLanguage' } },
        { key: 'node', text: 'Node', iconProps: { iconName: 'JavaScriptLanguage' } },
    ];

    const [output, setOutput] = useState("flask")
    
    const generateApiOnClick = () => {
        generateFullAPI(output)
    }

    return (
        <footer className="ViewApiFooter">
            <div>
                <ChoiceGroup className="ViewApiFooterChoiceField" defaultSelectedKey="flask" options={options} onChange={(e, option) => {setOutput(option.key)}} />
            </div>
            <PrimaryButton className="ViewApiFooterPrimaryButton" onClick={generateApiOnClick}> Generate Full API </PrimaryButton>
        </footer>
    )
}