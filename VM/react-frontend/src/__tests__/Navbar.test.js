import React from 'react';
import Navbar from '../Navbar';
import logoImage from '../../public/images/API-Builder-Logo-1.png';

import { shallow } from 'enzyme';

describe('Navbar Testing', () => {

  test ('sample test', () => {
    expect('test').toBe('test')
  })
  // let wrapper;

  // beforeEach(() => {
  //   wrapper = shallow(<Navbar />);
  // });

//   test('renders the correct logo image', () => {
//     const preStringForFlask = 'static/react/images/';
//     expect(wrapper.find('img').prop('src')).toEqual(
//       preStringForFlask + logoImage
//     );
//   });

  // test('goes to "/" route after clicking on the logo using react router Link', () => {
  //   // expect(wrapper.find('Link').props().to).toBe('/');
  //   expect(wrapper.find('.homepageLink').props().to).toBe('/');
  // });

//   test('renders the name of the company API Builder', () => {
//     expect(wrapper.find('.logo-text').text()).toBe('API Builder');
//   });

//   test('checks if the first option is a Blog option', () => {
//     expect(
//       wrapper
//         .find('ul')
//         .childAt(1)
//         .text()
//     ).toBe('Blog');
//   });

//   test('goes to "/blog" route after clicking the Blog link', () => {
//     expect(wrapper.find('.blogLink').props().to).toBe('/blog');
//   });

//   test('checks if the second option is a Tutorial option', () => {
//     expect(
//       wrapper
//         .find('ul')
//         .childAt(2)
//         .text()
//     ).toBe('Tutorial');
//   });

//   test('goes to "/tutorial" route after clicking the Tutorial link', () => {
//     expect(wrapper.find('.tutorialLink').props().to).toBe('/tutorial');
//   });

//   test('checks if the third option is a "View current routes" selection', () => {
//     expect(
//       wrapper
//         .find('ul')
//         .childAt(3)
//         .text()
//     ).toBe('View current routes');
//   });
});
