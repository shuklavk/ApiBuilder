import React from 'react';
import './componentCss/Navbar.css';

export default () => {
    const onBlogClick = () => {
        alert('Blog coming soon!')
    }
    return (
        <li className="navbarLi" onClick={onBlogClick}><a className="navbarA" href="#" id="blog-link">Blog</a></li>
    )
};

