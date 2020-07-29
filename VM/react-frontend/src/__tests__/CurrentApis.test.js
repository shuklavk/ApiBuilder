import React from 'react';
import CurrentApis from '../CurrentApis';
import {Label} from '@fluentui/react'

import {shallow} from 'enzyme'

describe('CurrentApis testing', () => {
    let wrapper;
    beforeEach(() => {
        wrapper = shallow(<CurrentApis/>)
    })

    test('Renders a title label', () => {
        expect(wrapper.find(Label).length).toEqual(1);
    })
})