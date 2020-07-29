import React from 'react';
import './componentCss/Navbar.css';

export default () => {
    const allApisClick = () => {
        alert('All APIs Page coming soon!')
    }
  return (
    <li className="navbarLi" onClick={allApisClick}><a className="navbarA" href="#" id="apis-link">APIs</a></li>
)};

