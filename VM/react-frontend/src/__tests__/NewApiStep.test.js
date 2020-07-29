import React from 'react'
import NewApiStep from '../NewApiStep'
import {Label, Image} from '@fluentui/react'
import addApi from '../AddApi'
import stepOneImage from '../../public/images/step_1.png'

import {shallow} from 'enzyme'

describe("NewApiStep testing", () => {
    let wrapper

    beforeEach(() => {
        wrapper = shallow(<NewApiStep />);
    });

    test('Renders a Title Label', ()=>{
        expect(wrapper.find(Label).length).toEqual(1);
    })

    test('Renders the step one image', ()=>{
        const preStringForFlask = 'static/react/images/';
        expect(wrapper.find(Image).prop('src')).toEqual(preStringForFlask + stepOneImage)
    })

    test('Renders addApi Component', () => {
        expect(wrapper.find(addApi).length).toEqual(1)
    })
})