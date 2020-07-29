import React from 'react'
import AddApi from '../AddApi'
import {Label, TextField, PrimaryButton} from '@fluentui/react'

import {shallow} from 'enzyme'

describe('AddApi testing', ()=>{

    let wrapper;

    beforeEach(() => {
      wrapper = shallow(<AddApi />);
    });
    
    test('Renders the correct label of "Create a new API"', () => {
        expect(wrapper.find(Label).length).toEqual(1)
        expect(wrapper.find(Label).text()).toEqual('Create a new API')
    })

    test('Renders an input field with a placeholder value"', ()=>{
        expect(wrapper.find(TextField).length).toEqual(1)
        expect(wrapper.find(TextField).prop('placeholder').length).toBeGreaterThan(0)
    })

    test('Text field is required', () => {
        expect(wrapper.find(TextField).prop('required')).toBe(true)
    })

    test('Label is connected with TextField', () => {
        expect(wrapper.find(Label).prop('htmlFor')).toEqual(wrapper.find(TextField).prop('id'))
    })

    test('Renders a Button Component', ()=>{
        expect(wrapper.find(PrimaryButton).length).toEqual(1)
    })
})